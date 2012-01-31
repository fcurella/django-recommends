from django.contrib import admin
from .models import Similarity, Recommendation


class SimilarityAdmin(admin.ModelAdmin):
    list_display = ('object', 'object_site', 'related_object', 'related_object_site', 'score')
    list_filter = ('object_site',)
admin.site.register(Similarity, SimilarityAdmin)


class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'object', 'object_site')
    list_filter = ('object_site',)
admin.site.register(Recommendation, RecommendationAdmin)
