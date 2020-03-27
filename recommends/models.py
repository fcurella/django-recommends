from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property


class MockModel(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __str__(self):
        return "Mock for content object %s" % self.object

    def __repr__(self):
        return "<%s>" % self.__str__()

    @cached_property
    def object(self):
        ModelClass = ContentType.objects.get(pk=self.object_ctype).model_class()
        return ModelClass.objects.get(pk=self.object_id)


class MockSimilarity(MockModel):
    @cached_property
    def related_object(self):
        ModelClass = ContentType.objects.get(pk=self.related_object_ctype).model_class()
        return ModelClass.objects.get(pk=self.related_object_id)

    def __str__(self):
        return "Similarity between %s and %s" % (self.object, self.related_object)
