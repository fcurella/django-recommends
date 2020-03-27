from __future__ import unicode_literals

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth import models as auth_models
from django.urls import reverse


class RecProduct(models.Model):
    """A generic Product"""
    name = models.CharField(blank=True, max_length=100)
    sites = models.ManyToManyField(Site)

    class Meta:
        app_label = 'recommends'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])

    def sites_str(self):
        return ', '.join([s.name for s in self.sites.all()])
    sites_str.short_description = 'sites'


class RecVote(models.Model):
    """A Vote on a Product"""
    user = models.ForeignKey(
        auth_models.User, related_name='rec_votes', on_delete=models.CASCADE,
    )
    product = models.ForeignKey(RecProduct, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    score = models.FloatField()

    class Meta:
        app_label = 'recommends'

    def __str__(self):
        return "Vote"
