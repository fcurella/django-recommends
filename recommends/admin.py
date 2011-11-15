from django.contrib import admin
from .models import SimilarityResult, Recommendation


admin.site.register(SimilarityResult)
admin.site.register(Recommendation)
