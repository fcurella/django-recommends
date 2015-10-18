from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from .managers import RecommendsManager, SimilarityManager, RecommendationManager
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class RecommendsBaseModel(models.Model):
    """(RecommendsBaseModel description)"""
    object_ctype = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object_site = models.PositiveIntegerField()
    object = GenericForeignKey('object_ctype', 'object_id')

    objects = RecommendsManager()

    class Meta:
        abstract = True
        unique_together = ('object_ctype', 'object_id', 'object_site')

    def __str__(self):
        return "RecommendsBaseModel"


@python_2_unicode_compatible
class Similarity(RecommendsBaseModel):
    """How much an object is similar to another"""

    score = models.FloatField(null=True, blank=True, default=None)

    related_object_ctype = models.ForeignKey(ContentType, related_name='similar')
    related_object_id = models.PositiveIntegerField()
    related_object_site = models.PositiveIntegerField()
    related_object = GenericForeignKey('related_object_ctype', 'related_object_id')

    objects = SimilarityManager()

    class Meta:
        verbose_name_plural = 'similarities'
        unique_together = ('object_ctype', 'object_id', 'object_site', 'related_object_ctype', 'related_object_id', 'related_object_site')
        ordering = ['-score']

    def __str__(self):
        return "Similarity between %s and %s" % (self.object, self.related_object)


@python_2_unicode_compatible
class Recommendation(RecommendsBaseModel):
    """Recommended an object for a particular user"""
    user = models.PositiveIntegerField()
    score = models.FloatField(null=True, blank=True, default=None)

    objects = RecommendationManager()

    class Meta:
        unique_together = ('object_ctype', 'object_id', 'user')
        ordering = ['-score']

    def __str__(self):
        return "Recommendation for user %s" % (self.user)
