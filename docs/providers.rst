.. ref-providers:

Recommendation Providers
========================

In order to compute and retrieve similarities and recommendations, you must create a ``RecommendationProvider`` and register it with the model that represents the rating and a list of the models that will receive the votes.

A ``RecommendationProvider`` is a class that specifies how to retrieve various informations (items, users, votes) necessary for computing recommendation and similarities for a set of objects.

Subclasses override properties amd methods in order to determine what constitutes rated items, a rating, its score, and user.

The algorithm to use for computing is specified by the ``algorithm`` property.

A basic algorithm class is provided for convenience at ``recommends.algorithms.naive.NaiveAlgorithm``, but users can implement their own solutions. See :doc:`algorithms`.

Example::

    # models.py
    from __future__ import unicode_literals
    from django.db import models
    from django.contrib.auth.models import User
    from django.contrib.sites.models import Site
    from django.urls import reverse


    class Product(models.Model):
        """A generic Product"""
        name = models.CharField(blank=True, max_length=100)
        sites = models.ManyToManyField(Site)

        def __str__(self):
            return self.name

        def get_absolute_url(self):
            return reverse('product_detail', args=[self.id])

        def sites_str(self):
            return ', '.join([s.name for s in self.sites.all()])
        sites_str.short_description = 'sites'


    class Vote(models.Model):
        """A Vote on a Product"""
        user = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE)
        product = models.ForeignKey(Product)
        site = models.ForeignKey(Site)
        score = models.FloatField()

        def __str__(self):
            return "Vote"


Create a file called ``recommendations.py`` inside your app::

    # recommendations.py

    from django.contrib.auth.models import User
    from recommends.providers import RecommendationProvider
    from recommends.providers import recommendation_registry

    from .models import Product, Vote

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

All files called ``recommendations.py`` will be autodiscovered and loaded by
``django-recommends``. You can change the default module name, or disable
autodiscovery by tweaking the ``RECOMMENDS_AUTODISCOVER_MODULE`` setting (see
:doc:`settings`), or you could manually import your module in your app's
``AppConfig.ready``::

    # apps.py

    from django.apps import AppConfig


    class MyAppConfig(AppConfig):
        name = 'my_app'

        def ready(self):
            from .myrecs import *

Properties
----------
    * ``signals``

        This property define to which signals the provider should listen to.
        A method of the same name will be called on the provider when the 
        corresponding signal is fired from one of the rated model.

        See :doc:`signals`.

        Defaults to ``['django.db.models.pre_delete']``
    
    * ``algorithm``
        
        Defaults to ``recommends.algorithms.naive.NaiveAlgorithm``

Methods
-------

    * ``get_items(self)``

        This method must return items that have been voted.

    * ``items_ignored(self)``

        Returns user ignored items.
        User can delete items from the list of recommended.

        See recommends.converters.IdentifierManager.get_identifier for help.

    * ``get_ratings(self, obj)``

        Returns all ratings for given item.

    * ``get_rating_user(self, rating)``

        Returns the user who performed the rating.

    * ``get_rating_score(self, rating)``

        Returns the score of the rating.

    * ``get_rating_item(self, rating)``

        Returns the rated object.

    * ``get_rating_site(self, rating)``

        Returns the site of the rating. Can be a ``Site`` object or its ID.

        Defaults to ``settings.SITE_ID``.

    * ``is_rating_active(self, rating)``

        Returns if the rating is active.

    * ``pre_store_similarities(self, itemMatch)``

        Optional. This method will get called right before passing the similarities to the storage.

        For example, you can override this method to do some stats or visualize the data.

    * ``pre_delete(self, sender, instance, **kwargs)``

        This function gets called when a signal in ``self.rate_signals`` is
        fired from one of the rated models.

        Overriding this method is optional. The default method removes the
        suggestions for the deleted objected.
        
        See :doc:`signals`.
