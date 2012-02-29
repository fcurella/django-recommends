from django.db import models
from django.contrib.contenttypes import generic
from .managers import RecommendsManager, SimilarityManager, RecommendationManager, PendingManager


class RecommendsBaseModel(models.Model):
    """(RecommendsBaseModel description)"""
    object_ctype = models.PositiveIntegerField()
    object_id = models.PositiveIntegerField()
    object_site = models.PositiveIntegerField()
    object = generic.GenericForeignKey('object_ctype', 'object_id')
    score = models.FloatField(null=True, blank=True, default=None)
    pending = models.BooleanField(default=True)

    pending_objects = PendingManager()
    objects = RecommendsManager()

    class Meta:
        abstract = True
        unique_together = ('object_ctype', 'object_id', 'object_site', 'pending')

    def __unicode__(self):
        return u"RecommendsBaseModel"


class Similarity(RecommendsBaseModel):
    """How much an object is similar to another"""
    related_object_ctype = models.PositiveIntegerField()
    related_object_id = models.PositiveIntegerField()
    related_object_site = models.PositiveIntegerField()
    related_object = generic.GenericForeignKey('related_object_ctype', 'related_object_id')

    pending_objects = PendingManager()
    objects = SimilarityManager()

    class Meta:
        verbose_name_plural = 'similarities'
        unique_together = ('object_ctype', 'object_id', 'object_site', 'related_object_ctype', 'related_object_id', 'related_object_site', 'pending')
        ordering = ['-score']

    def __unicode__(self):
        return u"Similarity between %s and %s" % (self.object, self.related_object)


class Recommendation(RecommendsBaseModel):
    """Recommended an object for a particular user"""
    user = models.PositiveIntegerField()

    all_objects = models.Manager()
    pending_objects = PendingManager()
    objects = RecommendationManager()

    class Meta:
        unique_together = ('object_ctype', 'object_id', 'user', 'pending')
        ordering = ['-score']

    def __unicode__(self):
        return u"Recommendation for user %s" % (self.user)
