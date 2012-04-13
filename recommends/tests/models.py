from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth import models as auth_models


class RecProduct(models.Model):
    """A generic Product"""
    name = models.CharField(blank=True, max_length=100)
    sites = models.ManyToManyField(Site)

    class Meta:
        app_label = 'recommends'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('product_detail', [self.id])

    def sites_str(self):
        return u', '.join([s.name for s in self.sites.all()])
    sites_str.short_description = 'sites'


class RecVote(models.Model):
    """A Vote on a Product"""
    user = models.ForeignKey(auth_models.User, related_name='rec_votes')
    product = models.ForeignKey(RecProduct)
    site = models.ForeignKey(Site)
    score = models.FloatField()

    class Meta:
        app_label = 'recommends'

    def __unicode__(self):
        return u"Vote"
