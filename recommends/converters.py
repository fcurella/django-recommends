from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType


def get_sites(obj):
    for field in obj._meta.fields:
        if field.rel and field.rel.to == Site:
            return [getattr(obj, field)]
    for field in obj._meta.many_to_many:
        if field.rel and field.rel.to == Site:
            return getattr(obj, field).all()
    return [Site.objects.get_current()]


def get_identifier(obj, site=None):
    """
    Given a Django Model, returns a string identifier in the format
    <app_label>.<model>:<site_id>:<object_id>.
    """
    if site is None:
        site = Site.objects.get_current()
    ctype = ContentType.objects.get_for_model(obj)
    return "%s.%s:%s:%s" % (ctype.app_label, ctype.model, site.id, obj.id)


def resolve_identifier(identifier):
    """
    The opposite of ``get_identifier()``
    """
    app_module, site_id, object_id = identifier.split(':')
    app_label, model = app_module.split('.')
    site = Site.objects.get(pk=site_id)
    ModelClass = ContentType.object.get(app_label=app_label, model=model).model_class()
    model = ModelClass.objects.get(pk=object_id)
    return model, site


def convert_iterable_to_prefs(iterable):
    """
    `iterable must be composed of (user_id, object_identifier, rating)

    `object_identifier` is any string that uniquely identifies the object ie:
    <app_label>.<model>:<object_id>.

    The `utils.get_identifier` method is provided as convenience for creating such identifiers.
    """
    prefs = {}
    for pref in iterable:
        prefs[pref[0]][pref[1]] = pref[2]
    return prefs


def similary_results_to_itemMatch(qs, provider):
    itemMatch = {}
    for i in qs:
        site = i.related_object_site
        item = provider.get_identifier(i.get_object(), site)
        similarity = i.score
        item2 = provider.get_identifier(i.get_related_object(), site)

        itemMatch.setdefault(item, [])
        itemMatch[item] = (similarity, item2)

    return itemMatch
