from ..models import SimilarityResult, Recommendation
from ..providers import recommendation_registry
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
        return recommendation_registry.storage.get_similarities_for_object(obj, int(limit))


class SuggestionNode(template.Node):
    def __init__(self, varname, limit):
        self.varname = varname
        self.limit = limit

    def render(self, context):
        user = context['user']
        if user.is_authenticated():  # We need an id after all
            suggestions = recommendation_registry.storage.get_recommendations_for_user(user, int(self.limit))
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
