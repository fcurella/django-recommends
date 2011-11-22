Recommendation Providers
========================

In order to compute and retrieve similarities and recommendations, you must create a ``RecommendationProvider`` and register it with a model that represents the rating.


A ``RecommendationProvider`` is a class that specifies how to retrieve various informations (items, users, votes) necessary for computing recommendation and similarities for a set of objects.

Subclasses override properties amd methods in order to determine what constitutes rated items, a rating, its score, and user.

A basic algorithm to calculate similarities and recommendations is provided by default, but subclasses can use their own by overriding the ``calculate_similarities`` and ``calculate_recommendations`` methods.

Properties
----------
    * ``rate_signals``

        This property define to hat signals connect the ``on_signal`` function.

        Defaults to ``[post_save]``
    
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

    * ``on_signal(self, sender, instance, **kwargs)``
        
        This function gets called when a signal in ``self.signals`` is called from the rating model (defaults to ``[post_save]``.
        
        Overriding this method is optional. The default method removes the suggestion for the rated instance for the user that just rated, via a celery task.

        if self.is_rating_active(instance)``
            user = self.get_rating_user(instance)
            obj = self.get_rating_item(instance)
            remove_suggestion.delay(user_id=user.id, rating_model=model_path(sender), model_path=model_path(obj), object_id=obj.id)

        See :doc:`signals`.

    * ``calculate_similarities(self, prefs)``
        
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

            {
                "<object_identifier1>": [
                                (<score>, <related_object_identifier2>),
                                (<score>, <related_object_identifier3>),
                ],
                "<object_identifier2>": [
                                (<score>, <related_object_identifier1>),
                                (<score>, <related_object_identifier3>),
                ],
            }

        

    * ``calculate_recommendations(self, prefs, itemMatch)``
        
        Returns a list of recommendations:

        ::

            [
                (<user1>, [
                    (<score>, "<object_identifier1>"),
                    (<score>, "<object_identifier2>"),
                ]),
                (<user2>, [
                    (<score>, "<object_identifier2>"),
                    (<score>, "<object_identifier3>"),
                ]),
            ]
