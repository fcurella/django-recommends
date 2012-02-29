from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from recommends.providers import recommendation_registry, RecommendationProvider
from recommends.storages.mongodb.storage import MongoStorage
from recommends.storages.redis.storage import RedisStorage
from recommends.algorithms.pyrecsys import RecSysAlgorithm


# Create your models here.
class Movie(models.Model):
    title = models.CharField(blank=True, max_length=100)
    sites = models.ManyToManyField(Site)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('movie_detail', [self.id])

    def sites_str(self):
        return u', '.join([s.name for s in self.sites.all()])
    sites_str.short_description = 'sites'


class Rating(models.Model):
    """A Vote on a Product"""
    user = models.ForeignKey(User, related_name='ratings')
    movie = models.ForeignKey(Movie, related_name='reviews')
    site = models.ForeignKey(Site)
    score = models.FloatField()

    def __unicode__(self):
        return u"Rating"


class MovieRecommendationProvider(RecommendationProvider):
    #storage = RedisStorage(settings=settings)
    #algorithm = RecSysAlgorithm()

    def get_users(self):
        return User.objects.filter(is_active=True, ratings__isnull=False).distinct()

    def get_items(self):
        return Movie.objects.filter(reviews__isnull=False).distinct().iterator()

    def get_ratings(self, obj):
        return Rating.objects.filter(movie=obj).iterator()

    def get_rating_score(self, rating):
        return rating.score

    def get_rating_site(self, rating):
        return rating.site

    def get_rating_user(self, rating):
        return rating.user

    def get_rating_item(self, rating):
        return rating.movie

recommendation_registry.register(Rating, [Movie], MovieRecommendationProvider)
