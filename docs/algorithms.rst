.. ref-algorithms:

Recommendation Algorithms
=========================

A Recommendation Algorithm is a subclass of ``recommends.algorithms.base.BaseAlgorithm`` that implements methods for calculating similarities and recommendations.

Subclasses must implement this methods:

    * ``calculate_similarities(self, vote_list)``
        
        Must return an dict of similarities for every object:

        Accepts a list of votes with the following schema:

        ::

            [
                ("<user1>", "<object_identifier1>", <score>),
                ("<user1>", "<object_identifier2>", <score>),
            ]

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

        

    * ``calculate_recommendations(self, vote_list, itemMatch)``
        
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

NaiveAlgorithm
--------------

This class implement a basic algorithm (adapted from: Segaran, T: Programming Collective Intelligence) that doesn't require any dependency at the expenses of performances.

Properties
~~~~~~~~~~
    
    * ``similarity``
        
        A callable that determines the similiarity between two elements.

        Functions for Euclidean Distance and Pearson Correlation are provided for convenience at ``recommends.similarities.sim_distance`` and ``recommends.similarities.sim_pearson``.

        Defaults to ``recommends.similarities.sim_distance``

RecSysAlgorithm
----------------

This class implement a SVD algorithm. Requires ``python-recsys`` (available at https://github.com/ocelma/python-recsys).

``python-recsys`` in turn requires ``SciPy``, ``NumPy``, and other python libraries.
