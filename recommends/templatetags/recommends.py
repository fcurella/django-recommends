from ..models import SimilarityResult, Recommendation
from django.contrib.sites import Site
from django.db import models
from django import template
register = template.Library()


@register.filter
def similar(obj):
    if isinstance(obj, models.Model):
        object_site = Site.objects.get_current()

        return SimilarityResult.objects.similar_to(obj, site=object_site)


class SuggestionNode(template.Node):
    def __init__(self, obj, varname):
        self.obj = obj
        self.site = Site.objects.get_current()
        self.varname = varname

    def render(self, context):
        user = context['user']
        suggestions = Recommendation.objects.get_recommendations_for_object(self.object, self.site, user)
        context[self.varname] = suggestions
        return ''


@register.simple_tag(takes_context=True)
def suggested(parser, token):
    """
    {% suggested myobject [limit 5] as suggestions %}
    {% for suggested in suggestions %}
        {{ suggested.get_object }}
    {% endfor %}
    """
    bits = token.contents.split()
    obj = bits[1]
    varname = bits[3]
    if isinstance(obj, models.Model):
        return SuggestionNode(obj, varname)
