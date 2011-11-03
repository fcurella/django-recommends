from .converters import resolve_identifier, get_identifier, convert_iterable_to_prefs


class RecommendationProviderRegisty(object):
    providers = []

    def register(self, provider):
        self.providers.append(provider)

recommendation_registry = RecommendationProviderRegisty()


class RecommendationProvider(object):
    def get_identifier(self, obj):
        raise NotImplemented

    def resolve_identifier(self, identifier):
        raise NotImplemented

    def get_items(self):
        raise NotImplemented

    def get_users(self, item):
        """Returns all the users who rated a particular item"""
        raise NotImplemented

    def get_rating(self, obj, user):
        """Return what rating a given user gave to a given item"""
        raise NotImplemented

    def _convert_iterable_to_prefs(self, iterable):
        return convert_iterable_to_prefs(iterable)

    def prefs(self):
        iterable = []
        for item in self.get_items():
            users = self.get_users(item)
            identifier = self.get_identifier(item)
            for user in users:
                rating = self.get_rating(item, user)
                iterable.append((user, identifier, rating))

        return self._convert_iterable_to_prefs(iterable)


class DjangoRecommendationProvider(RecommendationProvider):
    """
    Usage::

        class MyRecommendationProvider(DjangoRecommendationProvider):
            queryset = MyObject.objects.all()

            def get_users(self, item):
                return User.objects.filter(voted_on=item)

            def get_ratings(self, obj, user):
                return Vote.objects.filter(object=obj, user=user).rating
    """
    def get_identifier(self, obj):
        return get_identifier(obj)

    def resolve_identifier(self, identifier):
        raise resolve_identifier(identifier)

    def get_items(self):
        if not hasattr(self, 'queryset'):
            raise NotImplemented
        return self.queryset
