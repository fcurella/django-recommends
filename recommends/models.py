from django.contrib.contenttypes.models import ContentType


class MockModel(object):
    _object = None

    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __repr__(self):
        return "<%s>" % self.__unicode__()

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    @property
    def object(self):
        if self._object is None:
            ModelClass = ContentType.objects.get(pk=self.object_ctype).model_class()
            self._object = ModelClass.objects.get(pk=self.object_id)
        return self._object


class MockSimilarity(MockModel):
    _related_object = None

    @property
    def related_object(self):
        if self._related_object is None:
            ModelClass = ContentType.objects.get(pk=self.related_object_ctype).model_class()
            self._related_object = ModelClass.objects.get(pk=self.related_object_id)
        return self._related_object

    def __unicode__(self):
        return u"Similarity between %s and %s" % (self.object, self.related_object)
