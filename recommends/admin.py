from django.contrib import admin
from .models import SimilarityResult, Recommendation


class SimilarityResultAdmin(admin.ModelAdmin):
    list_display = ('get_subject', 'object_site', 'get_related_object', 'related_object_site', 'score')
    list_filter = ('object_site',)
admin.site.register(SimilarityResult, SimilarityResultAdmin)


class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'get_subject', 'object_site')
    list_filter = ('object_site',)
admin.site.register(Recommendation, RecommendationAdmin)
