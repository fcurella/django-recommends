from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from .models import SimilarityResult
from .converters import resolve_identifier, get_identifier, convert_iterable_to_prefs, similary_results_to_itemMatch
from .filtering import calculate_similar_items, get_recommended_items
from .utils import store_calculated_similar_items, store_recommended_items


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
    def get_identifier(self, obj, site=None, rating=None):
        raise NotImplemented

    def resolve_identifier(self, identifier):
        raise NotImplemented

    def get_items(self):
        raise NotImplemented

    def get_ratings(self, obj):
        """Returns all ratings for given item"""
        raise NotImplemented

    def get_rating_user(self, rating):
        raise NotImplemented

    def get_rating_rate(self, rating):
        raise NotImplemented

    def _convert_iterable_to_prefs(self, iterable):
        return convert_iterable_to_prefs(iterable)
    
    def prefs(self):
        iterable = []
        for item in self.get_items():
            for rating in self.get_ratings():
                user = self.get_rating_user(rating)
                rate = self.get_rating_rate(rating)
                identifier = self.get_identifier(item)
                iterable.append((user, identifier, rate))
        return self._convert_iterable_to_prefs(iterable)

    def precompute(self, prefs):
        raise NotImplemented


class DjangoRecommendationProvider(RecommendationProvider):
    """
    Usage::

        class MyRecommendationProvider(DjangoRecommendationProvider):
            def get_items(self):
                return MyObject.objects.all()

            def get_ratings(self, obj):
                \"\"\"Returns all the rates for a given object.\"\"\"
                return Vote.objects.filter(object=obj)

            def get_rating_user(self, rating):
                return rating.user

            def get_rating_rate(self, rating):
                return rating.rate
    
            def precompute(self, prefs):
                \"\"\"
                This function will be called by the task manager in order
                to compile and store the results
                \"\"\"
    """
    def get_identifier(self, obj, site=None, rating=None):
        return get_identifier(obj)

    def resolve_identifier(self, identifier):
        return resolve_identifier(identifier)

    def precompute(self, prefs):
        itemMatch = calculate_similar_items(prefs)
        store_calculated_similar_items(itemMatch, self)

        similarities = SimilarityResult.objects.all()
        itemMatch = similary_results_to_itemMatch(similarities, self)
        for user in User.objects.filter(is_active=True):
            rankings = get_recommended_items(prefs, itemMatch, user)
            store_recommended_items(user, rankings, self)


class DjangoSitesRecommendationProvider(DjangoRecommendationProvider):
    """
    Usage::

        class MyRecommendationProvider(DjangoSitesRecommendationProvider):
            def get_items(self):
                return MyObject.objects.all()

            def get_ratings(self, obj):
                \"\"\"Returns all the rates for a given object.\"\"\"
                return Vote.objects.filter(object=obj)

            def get_rating_user(self, rating):
                return rating.user

            def get_rating_rate(self, rating):
                return rating.rate

            def get_rating_site(self, rating):
                return rate.site

    """
    def get_identifier(self, obj, site=None, rating=None):
        if rating is not None:
            site = self.get_rating_site(rating)
        if site is None:
            site = Site.objects.get_current()
        return get_identifier(obj, site)

    def resolve_identifier(self, identifier):
        return resolve_identifier(identifier)

    def get_rating_site(self, rating):
        raise NotImplemented
