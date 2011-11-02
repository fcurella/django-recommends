from django.contrib.contenttypes.models import ContentType


def get_identifier(obj):
    """
    Given a Django Model, returns a string identifier in the format
    <app_label>.<model>:<object_id>.
    """
    ctype = ContentType.objects.get_for_model(obj)
    return "%s.%s:%s" % (ctype.app_label, ctype.model, obj.id)


def get_object(identifier):
    """
    The opposite of ``get_identifier()``
    """
    app_module, object_id = identifier.split(':')
    app_label, model = app_module.split('.')
    ModelClass = ContentType.object.get(app_label=app_label, model=model).model_class()
    return ModelClass.objects.get(pk=object_id)


def convert_tuple_to_prefs(atuple):
    """
    `atuple must be a tuple composed of (user_id, object_identifier, rating)

    `object_identifier` is any string that uniquely identifies the object ie:
    <app_label>.<model>:<object_id>.

    The `utils.get_identifier` method is provided as convenience for creating such identifiers.
    """
    prefs = {}
    for pref in atuple:
        prefs[pref[0]][pref[1]] = pref[2]
    return prefs


def convert_to_prefs(qs, func):
    """
    `func` must be a function that, given an item from qs, returns a tuple
    composed of (user_id, object_identifier, rating)

    `object_identifier` is any string that uniquely identifies the object ie:
    <app_label>.<model>:<object_id>.

    The `utils.get_identifier` method is provided as convenience for creating such identifiers.
    """
    prefs_tuple = map(func, qs)
    return convert_tuple_to_prefs(prefs_tuple)
