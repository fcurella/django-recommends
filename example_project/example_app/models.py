from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from recommends.providers import recommendation_registry, RecommendationProvider
from recommends.algorithms.pyrecsys import RecSysAlgorithm


# Create your models here.
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
