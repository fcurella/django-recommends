from ..models import SimilarityResult, Recommendation
from django.contrib.sites import Site
from django.db import models
from django import template
register = template.Library()


@register.filter
def similars(obj, limit):
    """
    Returns a list of SimilarityResult, representing how much an object is similar to the given one.

    Usage::

        {% for similar in myobj|similars:5 %}
            {{ similar.get_object }}
        {% endfor %}
    """
    if isinstance(obj, models.Model):
        object_site = Site.objects.get_current()

        return SimilarityResult.objects.similar_to(obj, site=object_site)[:int(limit)]


class SuggestionNode(template.Node):
    def __init__(self, varname, limit):
        self.site = Site.objects.get_current()
        self.varname = varname
        self.limit = limit

    def render(self, context):
        user = context['user']
        if user.is_authenticated():  # We need an id after all
            suggestions = Recommendation.objects.get_recommendations_for_user(user, self.site)[:self.limit]
            context[self.varname] = suggestions
        return ''


@register.simple_tag(takes_context=True)
def suggested(parser, token):
    """
    Returns a list of Recommendation (suggestions of objects) for the current user.

    {% suggested as suggestions [limit 5]  %}
    {% for suggested in suggestions %}
        {{ suggested.get_object }}
    {% endfor %}
    """
    bits = token.contents.split()
    varname = bits[3]
    try:
        limit = int(bits[5])
    except IndexError:
        limit = 5
    return SuggestionNode(varname, limit)
