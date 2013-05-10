from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class MockModel(object):
    _object = None

    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __str__(self):
        return "Mock for content object %s" % self.object

    def __repr__(self):
        return "<%s>" % self.__str__()

    @property
    def object(self):
        if self._object is None:
            ModelClass = ContentType.objects.get(pk=self.object_ctype).model_class()
            self._object = ModelClass.objects.get(pk=self.object_id)
        return self._object


@python_2_unicode_compatible
class MockSimilarity(MockModel):
    _related_object = None

    @property
    def related_object(self):
        if self._related_object is None:
            ModelClass = ContentType.objects.get(pk=self.related_object_ctype).model_class()
            self._related_object = ModelClass.objects.get(pk=self.related_object_id)
        return self._related_object

    def __str__(self):
        return "Similarity between %s and %s" % (self.object, self.related_object)
