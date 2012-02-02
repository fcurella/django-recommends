from recommends.utils import ctypes_dict


class CachedContentTypesMixin():
    _ctypes = None

    @property
    def ctypes(self):
        if self._ctypes is None:
            self._ctypes = ctypes_dict()
        return self._ctypes

    def get_ctype_id_for_obj(self, obj):
        app_label = obj._meta.app_label
        module_name = obj._meta.module_name
        return self.ctypes["%s.%s" % (app_label, module_name)]
