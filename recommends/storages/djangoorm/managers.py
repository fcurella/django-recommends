from django.conf import settings
from django.db import transaction
from django.db import models
from recommends.managers import CachedContentTypesMixin


class RecommendsManager(models.Manager, CachedContentTypesMixin):
    def get_query_set(self):
        return super(RecommendsManager, self).get_query_set().filter(score__isnull=False)

    def filter_for_model(self, model):
        ctype_id = self.get_ctype_id_for_obj(model)
        return self.filter(object_ctype=ctype_id)

    def filter_for_object(self, obj):
        return self.filter_for_model(obj).filter(object_id=obj.id)


class PendingManager(RecommendsManager):
    def get_query_set(self):
        return super(PendingManager, self).get_query_set().filter(pending=True, score__isnull=False)

    @transaction.commit_on_success
    def flip(self):
        self.all().delete()
        self.model.objects.all().update(pending=True)


class NonPendingManager(RecommendsManager):
    def get_query_set(self):
        return super(NonPendingManager, self).get_query_set().filter(pending=False, score__isnull=False)

    @transaction.commit_on_success
    def flip(self):
        self.all().delete()
        self.model.pending_objects.all().update(pending=False)


class SimilarityManager(NonPendingManager):
    def filter_for_related_model(self, related_model):
        ctype_id = self.get_ctype_id_for_obj(related_model)
        return self.filter(related_object_ctype=ctype_id)

    def filter_for_related_object(self, related_obj):
        return self.filter_for_related_model(related_obj).filter(related_object_id=related_obj.id)

    def filter_by_couple(self, target_object, related_obj):
        related_ctype_id = self.get_ctype_id_for_obj(related_obj)

        return self.filter_for_object(target_object).filter(
            related_object_ctype=related_ctype_id,
            related_object_id=related_obj.id
        )

    def create_for_objects(self, object_target, object_target_site, object_related, object_related_site):
        object_ctype_id = self.get_ctype_id_for_obj(object_target)
        object_id = object_target.id

        related_object_ctype_id = self.get_ctype_id_for_obj(object_related)
        related_object_id = object_related.id

        return self.create(
            object_ctype=object_ctype_id,
            object_id=object_id,
            object_site=object_target_site.id,
            related_object_ctype=related_object_ctype_id,
            related_object_id=related_object_id,
            related_object_site=object_related_site.id
        )

    def set_score_for_objects(self, object_target, object_target_site, object_related, object_related_site, score):
        if score == 0:
            self.filter_by_couple(object_target, object_related).filter(
                object_site=object_target_site.id,
                related_object_site=object_related_site.id
            ).delete()
            return None

        result = self.create_for_objects(object_target, object_target_site, object_related, object_related_site)
        result.score = score
        result.save()
        return result

    def similar_to(self, obj, site=None, **kwargs):
        if site is None and 'related_object_site' not in kwargs:
            kwargs['related_object_site'] = settings.SITE_ID
        return self.filter_for_object(obj).filter(**kwargs)


class RecommendationManager(NonPendingManager):
    def create_for_object(self, user, object_recommended, object_site):
        object_ctype_id = self.get_ctype_id_for_obj(object_recommended)
        object_id = object_recommended.id

        return self.create(
            object_ctype=object_ctype_id,
            object_id=object_id,
            object_site=object_site.id,
            user=user.id
        )

    def set_score_for_object(self, user, object_recommended, object_site, score):
        if score == 0:
            self.filter_for_object(object_recommended).filter(user=user.id).delete()
            return None

        result = self.create_for_object(user, object_recommended, object_site)
        result.score = score
        result.save()
        return result
