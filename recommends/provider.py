from .converters import resolve_identifier, get_identifier, convert_iterable_to_prefs


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
    def get_identifier(self, obj, *args, **kwargs):
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


class DjangoRecommendationProvider(RecommendationProvider):
    """
    Usage::

        class MyRecommendationProvider(DjangoRecommendationProvider):
            def get_items(self):
                return MyObject.objects.all()

            def get_ratings(self, obj):
                return Vote.objects.filter(object=obj)

            def get_rating_user(self, rating):
                return rating.user

            def get_rating_rate(self, rating):
                return rating.rate

    """
    def get_identifier(self, obj):
        return get_identifier(obj)

    def resolve_identifier(self, identifier):
        return resolve_identifier(identifier)


class DjangoSitesRecommendationProvider(DjangoRecommendationProvider):
    """
    Usage::

        class MyRecommendationProvider(DjangoSitesRecommendationProvider):
            def get_items(self):
                return MyObject.objects.all()

            def get_ratings(self, obj):
                return Vote.objects.filter(object=obj)

            def get_rating_user(self, rating):
                return rating.user

            def get_rating_rate(self, rating):
                return rating.rate

            def get_site(self, rating):
                return rate.site

    """
    def get_identifier(self, obj, site):
        return get_identifier(obj, site)

    def resolve_identifier(self, identifier):
        return resolve_identifier(identifier)

    def get_site(self, rating):
        raise NotImplemented

    def prefs(self):
        iterable = []
        for item in self.get_items():
            for rating in self.get_ratings():
                user = self.get_rating_user(rating)
                rate = self.get_rating_rate(rating)
                site = self.get_site(rating)
                identifier = self.get_identifier(item, site)
                iterable.append((user, identifier, rate))
        return self._convert_iterable_to_prefs(iterable)
