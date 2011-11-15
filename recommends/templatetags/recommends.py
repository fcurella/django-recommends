from ..models import SimilarityResult, Recommendation
from django.contrib.sites.models import Site
from django.db import models
from django import template
register = template.Library()


@register.filter
def similarities(obj, limit=5):
    """
    Returns a list of SimilarityResult, representing how much an object is similar to the given one.

    Usage::

        {% for similarities in myobj|similar:5 %}
            {{ similarities.get_object }}
        {% endfor %}
    """
    if isinstance(obj, models.Model):
        object_site = Site.objects.get_current()
        return SimilarityResult.objects.similar_to(obj, site=object_site, score__gt=0)[:int(limit)]


class SuggestionNode(template.Node):
    def __init__(self, varname, limit):
        self.site = Site.objects.get_current()
        self.varname = varname
        self.limit = limit

    def render(self, context):
        user = context['user']
        if user.is_authenticated():  # We need an id after all
            suggestions = Recommendation.objects.filter(user=user, object_site=self.site)[:self.limit]
            context[self.varname] = suggestions
        return ''


@register.tag()
def suggested(parser, token):
    """
    Returns a list of Recommendation (suggestions of objects) for the current user.

    {% suggested as suggestions [limit 5]  %}
    {% for suggested in suggestions %}
        {{ suggested.get_object }}
    {% endfor %}
    """
    bits = token.contents.split()
    varname = bits[2]
    try:
        limit = int(bits[4])
    except IndexError:
        limit = 5
    return SuggestionNode(varname, limit)
