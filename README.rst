django-recommends
======================================

A django app that build item-based suggestions for users.

Requires Celery.


Usage
----

In order to compute and retrieve similarities and recommendations, you must register a ``RecommendationProvider``.

A ``RecommendationProvider`` is a class that specifies how to retrieve various informations (items, users, votes)
necessary for computing recommendation and similarities for a set of objects.

Subclasses override methods in order to determine what constitutes voted items, a vote,
its score, and user.

A basic algorithm to calculate similarities and recommendations is provided by default, but subclasses can use their own by overriding the ``calculate_similarities`` and ``calculate_recommendations`` methods.

Example::

    # models.py
    from django.db import models
    from django.contrib.auth.models import User
    from django.contrib.sites.models import Site
    from recommends.providers import recommendation_registry, DjangoRecommendationProvider


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


    class ProductRecommendationProvider(DjangoRecommendationProvider):
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

    recommendation_registry.register(Product, ProductRecommendationProvider)

Template Tags & Filters
----------------------

To use the included template tags and filters, load the library in your templates by using ``{% load recommends %}``.

Filters
~~~~~~~

The available filters are:

``similar:<limit>``: returns a list of SimilarityResult, representing how much an object is similar to the given one. The ``limit`` argument is optional and defaults to ``5``::

    {% for similarities in myobj|similar:5 %}
        {{ similarities.get_object }}
    {% endfor %}

Tags
~~~~

The available tags are:

``{% suggested as <varname> [limit <limit>] %}``: Returns a list of Recommendation (suggestions of objects) for the current user. ``limit`` is optional and defaults to ``5``::

    {% suggested as suggestions [limit 5]  %}
    {% for suggested in suggestions %}
        {{ suggested.get_object }}
    {% endfor %}

Settings
---------

Celery Task
~~~~~~~~~~~

Computations are done by a scheduled celery task. The task is run every 24 hours by default, but can be overridden by the ``RECOMMENDS_TASK_CRONTAB`` setting::
    
    RECOMMENDS_TASK_CRONTAB = {'hour': '*/24'}

``RECOMMENDS_TASK_CRONTAB`` must be a dictionary of kwargs acceptable by celery.schedulers.crontab.

Templatetags Cache
~~~~~~~~~~~~~~~~~~

By default, the templatetags provided by django-recommends will cache their result for 60 seconds.
This time can be overridden via the ``RECOMMENDS_CACHE_TEMPLATETAGS_TIMEOUT``.


Storage backends
~~~~~~~~~~~~~~~~

Results of the computation are stored according to the storage backend defined in ``RECOMMENDS_STORAGE_BACKEND`` (default to ``'recommends.storages.DjangoOrmStorage'``). A storage backend defines how de/serialize and store/retrieve objects and results.

A storage backend can be any class extending ``recommends.storages.RecommendationStorage`` that implements the following methods:

* ``get_identifier(self, obj, *args, **kwargs)``
* ``resolve_identifier(self, identifier)``
* ``get_similarities_for_object(self, obj, limit)``
* ``get_recommendations_for_user(self, user, limit)``
* ``store_similarities(self, itemMatch)``
* ``store_recommendations(self, user, recommendations)``
