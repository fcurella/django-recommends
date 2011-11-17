from django.contrib.auth.models import User
from django.utils import importlib
from .converters import convert_iterable_to_prefs
from .filtering import calculate_similar_items, get_recommended_items
from .settings import RECOMMENDS_STORAGE_BACKEND


class RecommendationProviderRegistry(object):
    providers = []

    def __init__(self):
        storage_module = '.'.join(RECOMMENDS_STORAGE_BACKEND.split('.')[:-1])
        storage_class_name = RECOMMENDS_STORAGE_BACKEND.split('.')[-1]
        StorageClass = getattr(importlib.import_module(storage_module), storage_class_name)
        self.storage = StorageClass()

    def register(self, provider):
        self.providers.append(provider)

recommendation_registry = RecommendationProviderRegistry()


class Rating(object):
    def __init__(self, user, rated_object, rating):
        self.user = user
        self.rated_object = rated_object
        self.rating = rating


class RecommendationProvider(object):
    """
    A ``RecommendationProvider`` specifies how to retrieve various informations (items, users, votes)
    necessary for computing recommendation and similarities for a set of objects.

    Subclasses override methods in order to determine what constitutes voted items, a vote,
    its score, and user.
    """
    def __init__(self):
        self.storage = recommendation_registry.storage

    def get_items(self):
        """Return items that have been voted"""
        raise NotImplementedError

    def get_ratings(self, obj):
        """Returns all ratings for given item"""
        raise NotImplementedError

    def get_rating_user(self, rating):
        """Returns the user who performed the rating"""
        raise NotImplementedError

    def get_rating_score(self, rating):
        """Returns the score of the rating"""
        raise NotImplementedError

    def _convert_iterable_to_prefs(self, iterable):
        return convert_iterable_to_prefs(iterable)

    def prefs(self):
        """
        Returns a dictionary of votes, with the following schema::

            {
                "<user_id1>": {
                    "<object_identifier1>": <score>,
                    "<object_identifier2>": <score>,
                },
                "<user_id2>": {
                    "<object_identifier1>": <score>,
                    "<object_identifier2>": <score>,
                },
            }

        """
        iterable = []
        for item in self.get_items():
            for rating in self.get_ratings(item):
                user = self.get_rating_user(rating)
                score = self.get_rating_score(rating)
                identifier = self.storage.get_identifier(item)
                iterable.append((user, identifier, score))
        return self._convert_iterable_to_prefs(iterable)

    def calculate_similarities(self, prefs):
        """
        Must return an dict of similarities for every object:

        Accepts a dictionary representing votes with the following schema::

            {
                "<user1>": {
                    "<object_identifier1>": <score>,
                    "<object_identifier2>": <score>,
                }
            }

        Output must be a dictionary with the following schema::

        {
            "<object_identifier1>": [
                            (<score>, <related_object_identifier2>),
                            (<score>, <related_object_identifier3>),
            ],
            "<object_identifier2>": [
                            (<score>, <related_object_identifier1>),
                            (<score>, <related_object_identifier3>),
            ],
        }

        """
        raise NotImplementedError

    def calculate_recommendations(self, prefs, itemMatch):
        """
        Returns a list of recommendations::

        [
            (<user1>, [
                (<score>, "<object_identifier1>"),
                (<score>, "<object_identifier2>"),
            ]),
            (<user2>, [
                (<score>, "<object_identifier2>"),
                (<score>, "<object_identifier3>"),
            ]),
        ]

        """
        raise NotImplementedError

    def precompute(self, prefs):
        """
        This function will be called by the task manager in order
        to compile and store the results.
        """
        itemMatch = self.calculate_similarities(prefs)
        self.storage.store_similarities(itemMatch)

        self.storage.store_recommendations(self.calculate_recommendations(prefs, itemMatch))


class DjangoRecommendationProvider(RecommendationProvider):
    """
    Convenience provider for Django models.
    """

    def get_users(self):
        """Returns all users who have voted something"""
        return User.objects.filter(is_active=True)

    def calculate_similarities(self, prefs):
        return calculate_similar_items(prefs)

    def calculate_recommendations(self, prefs, itemMatch):
        recommendations = []
        for user in self.get_users():
            rankings = get_recommended_items(prefs, itemMatch, user)
            recommendations.append((user, rankings))
        return recommendations


class DjangoSitesRecommendationProvider(DjangoRecommendationProvider):
    """
    Convenience provider for Django models that use sites.

    Subclass and override the ``get_rating_site`` method to specify how to determine
    the site a particular vote was performed on.
    """

    def get_rating_site(self, rating):
        """
        Returns the site a particular vote was performed on.
        """
        raise NotImplementedError
