.. ref-providers:

Recommendation Providers
========================

In order to compute and retrieve similarities and recommendations, you must create a ``RecommendationProvider`` and register it with the model that represents the rating and a list of the models that will receive the votes.

A ``RecommendationProvider`` is a class that specifies how to retrieve various informations (items, users, votes) necessary for computing recommendation and similarities for a set of objects.

Subclasses override properties amd methods in order to determine what constitutes rated items, a rating, its score, and user.

A basic algorithm to calculate similarities and recommendations is provided by default, but subclasses can use their own by overriding the ``calculate_similarities`` and ``calculate_recommendations`` methods.

Example::

    # models.py
    from django.db import models
    from django.contrib.auth.models import User
    from django.contrib.sites.models import Site
    from recommends.providers import recommendation_registry, RecommendationProvider


    class Product(models.Model):
        """A generic Product"""
        name = models.CharField(blank=True, max_length=100)
        sites = models.ManyToManyField(Site)

        def __unicode__(self):
            return self.name

        @models.permalink
        def get_absolute_url(self):
            return ('product_detail', [self.id])

        def sites_str(self):
            return u', '.join([s.name for s in self.sites.all()])
        sites_str.short_description = 'sites'


    class Vote(models.Model):
        """A Vote on a Product"""
        user = models.ForeignKey(User, related_name='votes')
        product = models.ForeignKey(Product)
        site = models.ForeignKey(Site)
        score = models.FloatField()

        def __unicode__(self):
            return u"Vote"


    class ProductRecommendationProvider(RecommendationProvider):
        def get_users(self):
            return User.objects.filter(is_active=True, votes__isnull=False).distinct()

        def get_items(self):
            return Product.objects.all()

        def get_ratings(self, obj):
            return Vote.objects.filter(product=obj)

        def get_rating_score(self, rating):
            return rating.score

        def get_rating_site(self, rating):
            return rating.site

        def get_rating_user(self, rating):
            return rating.user

        def get_rating_item(self, rating):
            return rating.product

    recommendation_registry.register(Vote, [Product], ProductRecommendationProvider)

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

    * ``pre_delete(self, sender, instance, **kwargs)``

        This function gets called when a signal a pre_delete is fired from one of the rated models.

        Overriding this method is optional. The default method removes the suggestion for the rated instance for the user that just rated, via a celery task.
        
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
