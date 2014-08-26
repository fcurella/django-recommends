from recommends.converters import IdentifierManager


class BaseRecommendationStorage(object):
    threshold_similarities = 0
    threshold_recommendations = 0

    can_lock = False

    def __init__(self, settings=None):
        self.identifier_manager = IdentifierManager()
        self.settings = settings

    def get_identifier(self, obj, site_id=None, rating=None, *args, **kwargs):
        """
        Given an object and optional parameters, returns a string identifying the object uniquely.
        """
        if rating is not None:
            site_id = self.get_rating_site(rating).id
        if site_id is None:
            site_id = self.settings.SITE_ID
        return self.identifier_manager.get_identifier(obj, site_id)

    def resolve_identifier(self, identifier):
        """
        This method is the opposite of ``get_identifier``.
        It resolve the object's identifier to an actual model.
        """
        return self.identifier_manager.resolve_identifier(identifier)

    def get_similarities_for_object(self, obj, limit, raw_id=False):
        """
        if raw_id = False:
            Returns a list of ``Similarity`` objects for given ``obj``, ordered by score.
        else:
            Returns a list of similar ``model`` ids[pk] for given ``obj``, ordered by score.

            Example:

        ::

            [
                {
                    "related_object_id": XX, "contect_type_id": XX
                },
                ..
            ]
        """
        raise NotImplementedError

    def get_recommendations_for_user(self, user, limit, raw_id=False):
        """
        if raw_id = False:
            Returns a list of ``Recommendation`` objects for given ``user``, ordered by score.
        else:
            Returns a list of recommended ``model`` ids[pk] for given ``user``, ordered by score.

            Example:

        ::
            [
                {
                    "object_id": XX, "contect_type_id": XX
                },
                ..
            ]
        """
        raise NotImplementedError

    def store_similarities(self, itemMatch):
        raise NotImplementedError

    def store_recommendations(self, recommendations):
        """
        Stores all the recommendations.

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
        Optional.

        Retrieves the vote matrix saved by ``store_votes``.

        You won't usually need to implement this method, because you want to use fresh data.
        But it might be useful if you want some kind of heavy caching, maybe for testing purposes.
        """
        raise NotImplementedError

    def store_votes(self, iterable):
        """
        Optional.

        Saves the vote matrix.

        You won't usually need to implement this method, because you want to use fresh data.
        But it might be useful if you want to dump the votes on somewhere, maybe for testing purposes.

        ``iterable`` is the vote matrix, expressed as a list of tuples with the following schema:

        ::

            [
                ("<user_id1>", "<object_identifier1>", <score>),
                ("<user_id1>", "<object_identifier2>", <score>),
                ("<user_id2>", "<object_identifier1>", <score>),
                ("<user_id2>", "<object_identifier2>", <score>),
            ]
        """
        raise NotImplementedError

    def remove_recommendation(self, obj):
        """
        Deletes all recommendations for object ``obj``.
        """
        raise NotImplementedError

    def remove_similarity(self, obj):
        """
        Deletes all similarities that have object ``obj`` as source or target.
        """
        raise NotImplementedError

    def get_lock(self):
        """
        Acquire a storage-specific lock
        """
        raise NotImplementedError

    def release_lock(self):
        """
        Release a storage-specific lock
        """
        raise NotImplementedError
