from .settings import RECOMMENDS_STORAGE_DATABASE_ALIAS


class RecommendsRouter(object):
    def db_for_read(self, model, **hints):
        "Point all operations on recommends models to RECOMMENDS_STORAGE_DATABASE_NAME"
        if model._meta.app_label == 'recommends':
            return RECOMMENDS_STORAGE_DATABASE_ALIAS
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on recommends models to RECOMMENDS_STORAGE_DATABASE_NAME"
        if model._meta.app_label == 'recommends':
            return RECOMMENDS_STORAGE_DATABASE_ALIAS
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in recommends is involved"
        if obj1._meta.app_label == 'recommends' or obj2._meta.app_label == 'recommends':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the recommends app only appears on the RECOMMENDS_STORAGE_DATABASE_NAME db"
        if db == RECOMMENDS_STORAGE_DATABASE_ALIAS:
            return model._meta.app_label == 'recommends'
        elif model._meta.app_label == 'recommends':
            return False
        return None
