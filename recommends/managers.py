from django.db import models
from django.contrib.contenttypes.models import ContentType


class RecommendsManager(models.Manager):
    def filter_for_model(self, model):
        ctype = ContentType.objects.get_for_model(model)
        return self.filter(object_ctype=ctype)

    def filter_for_object(self, obj):
        return self.filter_for_model(obj).filter(object_id=obj.id)


class RatingManager(RecommendsManager):
    def get_query_set(self):
        return super(RecommendsManager, self).get_query_set().filter(rating__isnull=False)

    def prefs(self):
        """
        Returns a dict representing users' votes on items, as in::

            {
                '<user_id>': {
                    '<app_label>.<model>:<object_id>': <rating>,
                },
            }

        """
        prefs = {}
        for result in self.get_query_set():
            item_key = result.object_identifier()
            related_key = result.related_object_identifier()
            score = result.score
            prefs.setdefault(item_key, [])
            prefs[item_key].append((score, related_key))
        return prefs

    def prefs_for_model(self, model):
        return self.filter_for_model(model).prefs()


class SimilarityResultManager(RecommendsManager):
    def get_query_set(self):
        return super(RecommendsManager, self).get_query_set().filter(score__isnull=False)

    def prefs_for_qs(self):
        """
        Returns a dict representing similarity scores for a given content type::

        {
            "<object_id>": [
                            (<score>, <related_object_id>),
                            (<score>, <related_object_id>),
            ],
            "<object_id>": [
                            (<score>, <related_object_id>),
                            (<score>, <related_object_id>),
            ],
        }

        """
        prefs = {}
        for result in self.get_query_set():
            item_key = result.object_identifier()
            related_key = result.related_object_identifier()
            score = result.score
            prefs.setdefault(item_key, [])
            prefs[item_key].append((score, related_key))
        return prefs

    def prefs_for_model(self, model):
        return self.filter_for_model(model).prefs()

    def get_or_create_for_objects(self, object_target, object_target_site, object_related, object_related_site):
        object_ctype = ContentType.objects.get_for_model(object_target)
        object_id = object_target.id

        related_object_ctype = ContentType.objects.get_for_model(object_related)
        related_object_id = object_related.id

        return self.get_or_create(
            object_ctype=object_ctype,
            object_id=object_id,
            object_site=object_target_site,
            related_object_ctype=related_object_ctype,
            related_object_id=related_object_id,
            related_object_site=object_related_site
        )

    def set_score_for_objects(self, object_target, object_target_site, object_related, object_related_site, score):
        result, created = self.get_or_create_for_objects(object_target, object_target_site, object_related, object_related_site)
        result.score = score
        result.save()

    def similar_to(self, obj, site):
        object_ctype = ContentType.objects.get_for_model(obj)
        object_id = obj.pk
        return self.filter(object_ctype=object_ctype, object_id=object_id, related_object_site=site)


class RecommendationManager(RecommendsManager):
    def get_query_set(self):
        return super(RecommendsManager, self).get_query_set().filter(score__isnull=False)

    def get_or_create_for_object(self, user, object_recommended, object_site):
        object_ctype = ContentType.objects.get_for_model(object_recommended)
        object_id = object_recommended.id

        return self.get_or_create(
            object_ctype=object_ctype,
            object_id=object_id,
            object_site=object_site,
            user=user
        )

    def set_score_for_object(self, user, object_recommended, object_site, score):
        result, created = self.get_or_create_for_object(user, object_recommended, object_site)
        result.score = score
        result.save()

    def get_recommendations_for_user(self, user, site):
        self.filter(user=user, object_site=site)
