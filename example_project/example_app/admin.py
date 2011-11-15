from django.contrib import admin
from .models import Product, Vote


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sites_str')
    list_filter = ('sites',)
admin.site.register(Product, ProductAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'site', 'score')
    list_filter = ('site',)
admin.site.register(Vote, VoteAdmin)
