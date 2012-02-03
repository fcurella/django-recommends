from recommends.converters import IdentifierManager


class BaseRecommendationStorage(object):
    def __init__(self, settings=None):
        self.identifier_manager = IdentifierManager()
        self.settings = settings

    def get_identifier(self, obj, site_id=None, rating=None, *args, **kwargs):
        """Given an object and optional parameters, returns a string identifying the object uniquely"""
        if rating is not None:
            site_id = self.get_rating_site(rating).id
        if site_id is None:
            site_id = self.settings.SITE_ID
        return self.identifier_manager.get_identifier(obj, site_id)

    def resolve_identifier(self, identifier):
        """Returns an object corresponding to an identifier in the format returned by ``get_identifier``"""
        return self.identifier_manager.resolve_identifier(identifier)

    def get_similarities(self, limit):
        raise NotImplementedError

    def get_similarities_for_object(self, obj, limit):
        raise NotImplementedError

    def get_recommendations(self, limit):
        raise NotImplementedError

    def get_recommendations_for_user(self, user, limit):
        raise NotImplementedError

    def store_similarities(self, itemMatch):
        raise NotImplementedError

    def store_recommendations(self, recommendations):
        """
        ``recommendations`` is an iterable with the following schema:

        ::

            (
                (
                    <user>,
                    (
                        (<object_identifier>, <score>),
                        (<object_identifier>, <score>)
                    ),
                )
            )
        """
        raise NotImplementedError

    def get_votes(self):
        """
        Retrieves the vote matrix saved by ``store_votes``.

        You won't usually need to implement this method, because you want to use fresh data.
        But it might be useful if you want some kind of caching, maybe for testing purposes.
        """
        raise NotImplementedError

    def store_votes(self, iterable):
        """
        Saves the vote matrix.

        The matrix is a list of tuples with the following schema:

        ::

            [
                ("<user_id1>", "<object_identifier1>", <score>),
                ("<user_id1>", "<object_identifier2>", <score>),
                ("<user_id2>", "<object_identifier1>", <score>),
                ("<user_id2>", "<object_identifier2>", <score>),
            ]
        """
        raise NotImplementedError

    def remove_recommendation(self, user, obj):
        raise NotImplementedError

    def remove_similarity(self, obj):
        raise NotImplementedError
