from ..providers import recommendation_registry
from ..settings import RECOMMENDS_CACHE_TEMPLATETAGS_TIMEOUT
from django import template
from django.core.cache import cache
from django.conf import settings
from django.db import models
register = template.Library()


@register.filter
def similarities(obj, limit=5):
    """
    Returns a list of Similarity objects, representing how much an object is similar to the given one.

    Usage:

    ::

        {% for similarity in myobj|similar:5 %}
            {{ similarity.related_object }}
        {% endfor %}
    """
    if isinstance(obj, models.Model):
        cache_key = 'recommends:similarities:%s:%s.%s:%s:%s' % (settings.SITE_ID, obj._meta.app_label, obj._meta.object_name.lower(), obj.id, limit)
        similarities = cache.get(cache_key)
        if similarities is None:
            provider = recommendation_registry.get_provider_for_content(obj)
            similarities = provider.storage.get_similarities_for_object(obj, int(limit))
            cache.set(cache_key, similarities, RECOMMENDS_CACHE_TEMPLATETAGS_TIMEOUT)
        return similarities


class SuggestionNode(template.Node):
    def __init__(self, varname, limit):
        self.varname = varname
        self.limit = limit

    def render(self, context):
        user = context['user']
        if user.is_authenticated():  # We need an id after all
            cache_key = 'recommends:recommendations:%s:%s:%s' % (settings.SITE_ID, user.id, self.limit)
            suggestions = cache.get(cache_key)
            if suggestions is None:
                suggestions = set()
                for provider in recommendation_registry.providers:
                    suggestions.update(provider.storage.get_recommendations_for_user(user, int(self.limit)))
                cache.set(cache_key, suggestions, RECOMMENDS_CACHE_TEMPLATETAGS_TIMEOUT)
            context[self.varname] = suggestions
        return ''


@register.tag()
def suggested(parser, token):
    """
    Returns a list of Recommendation (suggestions of objects) for the current user.

    Usage:

    ::

        {% suggested as suggestions [limit 5]  %}
        {% for suggested in suggestions %}
            {{ suggested.object }}
        {% endfor %}
    """
    bits = token.contents.split()
    varname = bits[2]
    try:
        limit = int(bits[4])
    except IndexError:
        limit = 5
    return SuggestionNode(varname, limit)
