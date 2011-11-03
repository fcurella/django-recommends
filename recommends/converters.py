from django.contrib.contenttypes.models import ContentType


def get_identifier(obj):
    """
    Given a Django Model, returns a string identifier in the format
    <app_label>.<model>:<object_id>.
    """
    ctype = ContentType.objects.get_for_model(obj)
    return "%s.%s:%s" % (ctype.app_label, ctype.model, obj.id)


def resolve_identifier(identifier):
    """
    The opposite of ``get_identifier()``
    """
    app_module, object_id = identifier.split(':')
    app_label, model = app_module.split('.')
    ModelClass = ContentType.object.get(app_label=app_label, model=model).model_class()
    return ModelClass.objects.get(pk=object_id)


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
