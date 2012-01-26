.. ref-storages:

Storage backend
================

Results of the computation are stored according to the storage backend defined in ``RECOMMENDS_STORAGE_BACKEND`` (default to ``'recommends.storages.django.DjangoOrmStorage'``). A storage backend defines how de/serialize and store/retrieve objects and results.

A storage backend can be any class extending ``recommends.storages.base.RecommendationStorage`` that implements the following methods:

* ``get_identifier(self, obj, *args, **kwargs)``
* ``resolve_identifier(self, identifier)``
* ``get_similarities_for_object(self, obj, limit)``
* ``get_recommendations_for_user(self, user, limit)``
* ``get_votes(self)`` – Optional
* ``store_similarities(self, itemMatch)``
* ``store_recommendations(self, user, recommendations)``
* ``store_votes(self, iterable)`` – Optional
* ``remove_recommendation(self, user, obj)``
