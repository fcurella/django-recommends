from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import importlib
from .converters import convert_iterable_to_prefs, model_path
from .similarities import sim_distance
from .filtering import calculate_similar_items, get_recommended_items
from .settings import RECOMMENDS_STORAGE_BACKEND
from .tasks import remove_suggestion


class RecommendationProviderRegistry(object):
    providers = {}

    def __init__(self):
        storage_module = '.'.join(RECOMMENDS_STORAGE_BACKEND.split('.')[:-1])
        storage_class_name = RECOMMENDS_STORAGE_BACKEND.split('.')[-1]
        StorageClass = getattr(importlib.import_module(storage_module), storage_class_name)
        self.storage = StorageClass()

    def register(self, model, Provider):
        provider_instance = Provider()
        self.providers[model_path(model)] = provider_instance
        for signal in provider_instance.rate_signals:
            signal.connect(provider_instance.on_signal, sender=model)

    def provider_for_model(self, model):
        return self.providers[model_path(model)]

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
    rate_signals = [post_save]
    similarity = sim_distance

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

    def get_rating_item(self, rating):
        """Returns the rated object"""
        raise NotImplementedError

    def get_rating_site(self, rating):
        """Returns the site of the rating"""
        return None

    def is_rating_active(self, rating):
        """Returns if the rating is active"""
        return True

    def on_signal(self, sender, instance, **kwargs):
        """
        This function gets called when a signal in ``self.signals`` is called from the rating model.
        """
        if self.is_rating_active(instance):
            user = self.get_rating_user(instance)
            obj = self.get_rating_item(instance)
            remove_suggestion.delay(user_id=user.id, rating_model=model_path(sender), model_path=model_path(obj), object_id=obj.id)

    def _convert_iterable_to_prefs(self, iterable):
        return convert_iterable_to_prefs(iterable)

    def prefs(self):
        """
        Returns a dictionary of votes, with the following schema:

        ::

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
                site = self.get_rating_site(rating)
                identifier = self.storage.get_identifier(item, site)
                iterable.append((user, identifier, score))
        return self._convert_iterable_to_prefs(iterable)

    def precompute(self, prefs):
        """
        This function will be called by the task manager in order
        to compile and store the results.
        """
        itemMatch = self.calculate_similarities(prefs)
        self.storage.store_similarities(itemMatch)

        self.storage.store_recommendations(self.calculate_recommendations(prefs, itemMatch))

    def get_users(self):
        """Returns all users who have voted something"""
        return User.objects.filter(is_active=True)

    def calculate_similarities(self, prefs):
        """
        Must return an dict of similarities for every object:

        Accepts a dictionary representing votes with the following schema:

        ::

            {
                "<user1>": {
                    "<object_identifier1>": <score>,
                    "<object_identifier2>": <score>,
                }
            }

        Output must be a dictionary with the following schema:

        ::

            [
                ("<object_identifier1>", [
                                (<related_object_identifier2>, <score>),
                                (<related_object_identifier3>, <score>),
                ]),
                ("<object_identifier2>", [
                                (<related_object_identifier2>, <score>),
                                (<related_object_identifier3>, <score>),
                ]),
            ]

        """
        return calculate_similar_items(prefs, similarity=self.similarity)

    def calculate_recommendations(self, prefs, itemMatch):
        """
        ``itemMatch`` is supposed to be the result of ``calculate_similarities()``

        Returns a list of recommendations:

        ::

            [
                (<user1>, [
                    ("<object_identifier1>", <score>),
                    ("<object_identifier2>", <score>),
                ]),
                (<user2>, [
                    ("<object_identifier1>", <score>),
                    ("<object_identifier2>", <score>),
                ]),
            ]

        """
        recommendations = []
        for user in self.get_users():
            rankings = get_recommended_items(prefs, itemMatch, user)
            recommendations.append((user, rankings))
        return recommendations
