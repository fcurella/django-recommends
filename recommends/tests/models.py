from __future__ import unicode_literals
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth import models as auth_models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class RecProduct(models.Model):
    """A generic Product"""
    name = models.CharField(blank=True, max_length=100)
    sites = models.ManyToManyField(Site)

    class Meta:
        app_label = 'recommends'

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('product_detail', [self.id])

    def sites_str(self):
        return ', '.join([s.name for s in self.sites.all()])
    sites_str.short_description = 'sites'


@python_2_unicode_compatible
class RecVote(models.Model):
    """A Vote on a Product"""
    user = models.ForeignKey(auth_models.User, related_name='rec_votes')
    product = models.ForeignKey(RecProduct)
    site = models.ForeignKey(Site)
    score = models.FloatField()

    class Meta:
        app_label = 'recommends'

    def __str__(self):
        return "Vote"
