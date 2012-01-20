.. ref-templatetags:

Template Tags & Filters
=======================

To use the included template tags and filters, load the library in your templates by using ``{% load recommends %}``.

Filters
-------

The available filters are:

``similar:<limit>``: returns a list of Similarity objects, representing how much an object is similar to the given one. The ``limit`` argument is optional and defaults to ``5``::

    {% for similarity in myobj|similar:5 %}
        {{ similarity.related_object }}
    {% endfor %}

Tags
----

The available tags are:

``{% suggested as <varname> [limit <limit>] %}``: Returns a list of Recommendation (suggestions of objects) for the current user. ``limit`` is optional and defaults to ``5``::

    {% suggested as suggestions [limit 5]  %}
    {% for suggested in suggestions %}
        {{ suggested.object }}
    {% endfor %}

Templatetags Cache
------------------

By default, the templatetags provided by django-recommends will cache their result for 60 seconds.
This time can be overridden via the ``RECOMMENDS_CACHE_TEMPLATETAGS_TIMEOUT``.
