from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from recommends.providers import recommendation_registry, DjangoSitesRecommendationProvider


# Create your models here.
class Product(models.Model):
    """A generic Product"""
    name = models.CharField(blank=True, max_length=100)
    sites = models.ManyToManyField(Site)

    def __unicode__(self):
        return self.name


class Vote(models.Model):
    """(Vote description)"""
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    site = models.ForeignKey(Site)
    score = models.FloatField()

    def __unicode__(self):
        return u"Vote"


class ProductRecommendationProvider(DjangoSitesRecommendationProvider):
    def get_items(self):
        return Product.objects.all()

    def get_ratings(self, obj):
        return Vote.objects.filter(product=obj)

    def get_rating_rate(self, rating):
        return rating.vote

    def get_rating_site(self, rating):
        return rating.site

recommendation_registry.register(ProductRecommendationProvider)
