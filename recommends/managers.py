from django.db import models
from django.contrib.contenttypes.models import ContentType


class RatingManager(models.Manager):
    def filter_for_object(self, obj):
        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(rated_object_ctype=ctype, rated_object_id=obj.id)

    def filter_for_model(self, obj):
        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(rated_object_ctype=ctype)

    def prefs_for_model(self, obj):
        """
        Returns a dict representing users' votes on items, as in::

            {
                '<user_id>': {
                    '<app_label>.<model>:<object_id>': <rating>,
                },
            }

        """
        prefs = {}
        for rating in self.filter_for_model(obj):
            user = rating.user_id
            item_key = rating.rated_object_identifier()
            rating = rating.rating
            prefs.setdefault(user, {})
            prefs[user][item_key] = rating
        return prefs
