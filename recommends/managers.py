from recommends.utils import ctypes_dict


class CachedContentTypesMixin(object):
    _ctypes = None

    @property
    def ctypes(self):
        if self._ctypes is None:
            self._ctypes = ctypes_dict()
        return self._ctypes

    def get_ctype_id_for_obj(self, obj):
        app_label = obj._meta.app_label
        module_name = obj._meta.model_name
        return self.ctypes["%s.%s" % (app_label, module_name)]


class DictStorageManager(CachedContentTypesMixin):
    def similarity_for_objects(self, object_target, object_target_site, object_related, object_related_site):
        object_ctype_id = self.get_ctype_id_for_obj(object_target)
        object_id = object_target.id

        related_object_ctype_id = self.get_ctype_id_for_obj(object_related)
        related_object_id = object_related.id

        return dict(
            object_ctype=object_ctype_id,
            object_id=object_id,
            object_site=object_target_site.id,
            related_object_ctype=related_object_ctype_id,
            related_object_id=related_object_id,
            related_object_site=object_related_site.id,
        )

    def suggestion_for_object(self, user, object_recommended, object_site):
        object_ctype_id = self.get_ctype_id_for_obj(object_recommended)
        object_id = object_recommended.id

        return dict(
            object_ctype=object_ctype_id,
            object_id=object_id,
            object_site=object_site.id,
            user=user.id,
        )
