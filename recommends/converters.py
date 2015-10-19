from collections import defaultdict
from django.apps import apps


def model_path(obj):
    return '%s.%s' % (obj._meta.app_label, obj._meta.object_name.lower())


class IdentifierManager(object):
    _sites = None
    _ctypes = None

    @property
    def sites(self):
        if self._sites is None:
            from django.contrib.sites.models import Site

            self._sites = dict([(s.id, s) for s in Site.objects.all()])
        return self._sites

    @property
    def ctypes(self):
        if self._ctypes is None:
            from django.contrib.contenttypes.models import ContentType

            self._ctypes = dict([("%s.%s" % (c.app_label, c.model), c) for c in ContentType.objects.all()])
        return self._ctypes

    def resolve_identifier(self, identifier):
        """
        The opposite of ``get_identifier()``
        """
        app_module, site_id, object_id = identifier.split(':')
        app_label, model = app_module.split('.')
        site = self.sites[int(site_id)]
        ModelClass = apps.get_model(app_label, model)
        model = ModelClass.objects.get(pk=object_id)
        return model, site

    def identifier_to_dict(self, identifier, score=None, related=False):
        """
        The opposite of ``get_identifier()``
        """
        app_module, site_id, object_id = identifier.split(':')
        ctype = self.ctypes[app_module]

        if related:
            spec = {
                'related_object_ctype': ctype.id,
                'related_object_id': int(object_id),
                'related_object_site': int(site_id)
            }
        else:
            spec = {
                'object_ctype': ctype.id,
                'object_id': int(object_id),
                'object_site': int(site_id)
            }
        if score is not None:
            spec['score'] = score

        return spec

    def get_identifier(self, obj, site_id):
        """
        Given a Django Model, returns a string identifier in the format
        <app_label>.<model>:<site_id>:<object_id>.
        """
        return "%s:%s:%s" % (model_path(obj), site_id, obj.id)


def convert_vote_list_to_userprefs(vote_list):
    """
    Return a user-centerd prefernce matrix.

    ``vote_list must be`` composed of (user_id, object_identifier, rating)

    ``object_identifier`` is any string that uniquely identifies the object ie:
    <app_label>.<model>:<object_id>.

    The ``utils.get_identifier`` method is provided as convenience for creating such identifiers.
    """
    prefs = defaultdict(dict)
    for pref in vote_list:
        prefs[pref[0]][pref[1]] = pref[2]
    return prefs


def convert_vote_list_to_itemprefs(vote_list):
    """
    Return a item-centerd prefernce matrix.

    ``vote_list must be`` composed of (user_id, object_identifier, rating)

    ``object_identifier`` is any string that uniquely identifies the object ie:
    <app_label>.<model>:<object_id>.

    The ``utils.get_identifier`` method is provided as convenience for creating such identifiers.
    """
    prefs = defaultdict(dict)
    for pref in vote_list:
        prefs[pref[1]][pref[0]] = pref[2]
    return prefs


def similary_results_to_itemMatch(qs, provider):
    itemMatch = defaultdict(list)
    for i in qs:
        site = i.related_object_site
        item = provider.get_identifier(i.get_object(), site)
        similarity = i.score
        item2 = provider.get_identifier(i.get_related_object(), site)

        itemMatch[item].append((similarity, item2))

    return itemMatch
