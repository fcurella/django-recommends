from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from .converters import get_identifier
from .managers import RecommendsManager, RatingManager, SimilarityResultManager, RecommendationManager


class RecommendsBaseModel(models.Model):
    """(RecommendsBaseModel description)"""
    object_ctype = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    site = models.ForeignKey(Site)

    objects = RecommendsManager()

    class Meta:
        abstract = True
        unique_together = ('object_ctype', 'object_id', 'site')

    def __unicode__(self):
        return u"RecommendsBaseModel"

    def _object_identifier(self, ctype, object_id):
        obj = ctype.get_object_for_this_type(pk=object_id)
        return get_identifier(obj)

    def object_identifier(self):
        return self._object_identifier(self.object_ctype, self.object_id)


class Rating(RecommendsBaseModel):
    """
    This is a convenience model to represents Vote.
    You don't have to use this model, you can use your own.
    """
    user = models.ForeignKey(User)
    rating = models.FloatField(null=True, blank=True, default=None)

    objects = RatingManager()

    def __unicode__(self):
        return u"Rating"


class SimilarityResult(RecommendsBaseModel):
    """How much an object is similar to another"""

    score = models.FloatField(null=True, blank=True, default=None)

    related_object_ctype = models.ForeignKey(ContentType)
    related_object_id = models.PositiveIntegerField()

    objects = SimilarityResultManager()

    class Meta:
        unique_together = ('object_ctype', 'object_id', 'related_object_ctype', 'related_object_id')
        ordering = ['-score']

    def __unicode__(self):
        return u"Result"

    def related_object_identifier(self):
        return self._object_identifier(self.related_object_ctype, self.related_object_id)


class Recommendation(RecommendsBaseModel):
    """Recommended objects for a particular user"""
    user = models.ForeignKey(User)
    score = models.FloatField(null=True, blank=True, default=None)

    objects = RecommendationManager()

    class Meta:
        unique_together = ('object_ctype', 'object_id', 'user')
        ordering = ['-score']

    def __unicode__(self):
        return u"Recommendation for user %s" % (self.user)
