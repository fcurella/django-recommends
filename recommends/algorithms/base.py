class BaseAlgorithm(object):
    """
    """

    _cache = {}

    def clear_cache(self):
        self._cache = {}

    @property
    def cache(self):
        return self._cache

    def calculate_similarities(self, vote_list, verbose=0):
        """
        Must return an dict of similarities for every object:

        Accepts a vote matrix representing votes with the following schema:

        ::

            [
                (<user1>, "<object_identifier1>", <score>),
                (<user1>, "<object_identifier2>", <score>),
            ]

        Output must be a dictionary with the following schema:

        ::

            [
                ("<object_identifier1>", [
                                ("<related_object_identifier2>", <score>),
                                ("<related_object_identifier3>", <score>),
                ]),
                ("<object_identifier2>", [
                                ("<related_object_identifier1>", <score>),
                                ("<related_object_identifier3>", <score>),
                ]),
            ]

        """
        raise NotImplemented

    def calculate_recommendations(self, vote_list, itemMatch):
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
        raise NotImplemented
