from recommends.managers import DictStorageManager


class MongoStorageManager(DictStorageManager):
    def filter_for_object(self, obj):
        ctype_id = self.get_ctype_id_for_obj(obj)
        return {'object_ctype': ctype_id, 'object_id': obj.id}

    def filter_for_related_object(self, related_obj):
        ctype_id = self.get_ctype_id_for_obj(related_obj)
        return {'related_object_ctype': ctype_id, 'related_object_id': related_obj.id}
