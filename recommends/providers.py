from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from .converters import resolve_identifier, get_identifier, convert_iterable_to_prefs, similary_results_to_itemMatch
from .filtering import calculate_similar_items, get_recommended_items
from .storages import DummyStorage, DjangoOrmStorage


class RecommendationProviderRegisty(object):
    providers = []

    def register(self, provider):
        self.providers.append(provider)

recommendation_registry = RecommendationProviderRegisty()


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

    storage = DummyStorage

    def __init__(self):
        self.storage.provider = self

    def get_identifier(self, obj, *args, **kwargs):
        """Given an object and optional parameters, returns a string identifying the object uniquely"""
        raise NotImplementedError

    def resolve_identifier(self, identifier):
        """Returns an object corresponding to an identifier in the format returned by ``get_identifier``"""
        raise NotImplementedError

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
        iterable = []
        for item in self.get_items():
            for rating in self.get_ratings(item):
                user = self.get_rating_user(rating)
                score = self.get_rating_score(rating)
                identifier = self.get_identifier(item)
                iterable.append((user, identifier, score))
        return self._convert_iterable_to_prefs(iterable)

    def precompute(self, prefs):
        """
        This function will be called by the task manager in order
        to compile and store the results.
        """
        raise NotImplementedError


class DjangoRecommendationProvider(RecommendationProvider):
    """
    Convenience provider for Django models. Uses Django ORM as storage.
    """
    storage = DjangoOrmStorage()

    def get_identifier(self, obj, *args, **kwargs):
        return get_identifier(obj)

    def resolve_identifier(self, identifier):
        return resolve_identifier(identifier)

    def get_users(self):
        """Returns all users who have voted something"""
        return User.objects.filter(is_active=True)

    def precompute(self, prefs):
        itemMatch = calculate_similar_items(prefs)
        self.storage.store_similarities(itemMatch)

        similarities = self.storage.get_similarities()
        itemMatch = similary_results_to_itemMatch(similarities, self)
        for user in self.get_users():
            rankings = get_recommended_items(prefs, itemMatch, user)
            self.storage.store_user_recommendations(user, rankings)


class DjangoSitesRecommendationProvider(DjangoRecommendationProvider):
    """
    Convenience provider for Django models that use sites. Uses Django ORM as storage.

    Subclass and override the ``get_rating_site`` method to specify how to determine
    the site a particular vote was performed on.
    """
    def get_identifier(self, obj, site=None, rating=None, *args, **kwargs):
        if rating is not None:
            site = self.get_rating_site(rating)
        if site is None:
            site = Site.objects.get_current()
        return get_identifier(obj, site)

    def resolve_identifier(self, identifier):
        return resolve_identifier(identifier)

    def get_rating_site(self, rating):
        """
        Returns the site a particular vote was performed on.
        """
        raise NotImplementedError
