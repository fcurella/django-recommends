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
    from recommends.providers import recommendation_registry, DjangoSitesRecommendationProvider


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


    class ProductRecommendationProvider(DjangoSitesRecommendationProvider):
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

    recommendation_registry.register(ProductRecommendationProvider)


Computations are done by a scheduled celery task. The task is run every 24 hours by default, but can be overridden by the RECOMMENDS_TASK_CRONTAB setting::
    
    RECOMMENDS_TASK_CRONTAB = {'hour': '*/24'}

``RECOMMENDS_TASK_CRONTAB`` must be a dictionary of kwargs acceptable by celery.schedulers.crontab.
