Recommendation Providers
========================

In order to compute and retrieve similarities and recommendations, you must create a ``RecommendationProvider`` and register it with a model that represents the rating.


A ``RecommendationProvider`` is a class that specifies how to retrieve various informations (items, users, votes) necessary for computing recommendation and similarities for a set of objects.

Subclasses override properties amd methods in order to determine what constitutes rated items, a rating, its score, and user.

A basic algorithm to calculate similarities and recommendations is provided by default, but subclasses can use their own by overriding the ``calculate_similarities`` and ``calculate_recommendations`` methods.

Properties
----------
    * ``signals``

        This property define to hat signals connect the ``on_signal`` function.

        Defaults to ``['django.db.models.post_save', 'django.db.models.pre_delete']``
    
    * ``similarity``
        
        A callable that determines the similiarity between two elements.

        Functions for Euclidean Distance and Pearson Correlation are provided for convenience at ``recommends.similarities.sim_distance`` and ``recommends.similarities.sim_pearson``.

        Defaults to ``recommends.similarities.sim_distance``

Methods
-------

    * ``get_items(self)``

        This method must returb items that have been voted

    * ``get_ratings(self, obj)``

        Returns all ratings for given item

    * ``get_rating_user(self, rating)``

        Returns the user who performed the rating

    * ``get_rating_score(self, rating)``

        Returns the score of the rating

    * ``get_rating_item(self, rating)``

        Returns the rated object

    * ``get_rating_site(self, rating)``

        Returns the site of the rating

    * ``is_rating_active(self, rating)``

        Returns if the rating is active

    * ``pre_delete(self, sender, instance, **lwargs)``

        This function gets called when a signal a pre_delete is fired from the rating model.

        Overriding this method is optional. The default method removes the suggestion for the rated instance for the user that just rated, via a celery task.

    * ``on_signal(self, sender, instance, **kwargs)``
        
        This function gets called as a fallback when a signal in ``self.signals`` is fired from the rating model, but the provider doesn't have a corresponding funcion declared.
        
        See :doc:`signals`.

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
