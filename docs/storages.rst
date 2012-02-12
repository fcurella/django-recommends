.. ref-storages:

Storage backend
================

Results of the computation are stored according to the storage backend defined in ``RECOMMENDS_STORAGE_BACKEND`` (default to ``'recommends.storages.djangoorm.storage.DjangoOrmStorage'``). A storage backend defines how de/serialize and store/retrieve objects and results.

A storage backend can be any class extending ``recommends.storages.base.RecommendationStorage`` that implements the following methods:

* ``get_identifier(self, obj, *args, **kwargs)``
* ``resolve_identifier(self, identifier)``
* ``get_similarities_for_object(self, obj, limit)`` 
* ``get_recommendations_for_user(self, user, limit)``
* ``get_votes(self)`` – Optional
* ``store_similarities(self, itemMatch)``
* ``store_recommendations(self, user, recommendations)``
* ``store_votes(self, iterable)`` – Optional
* ``remove_recommendations(self, obj)``
* ``remove_similarities(self, obj)``


DjangoOrmStorage
----------------

This storage allows you to store results in a database specified by your ``DATABASES`` setting.

In order to use this storage, you'll also need to add ``'recommends.storages.djangoorm'`` to your ``INSTALLED_APPS``.

Settings
~~~~~~~~

To minimize disk I/O from the database, Similiarities and Suggestions will be committed in batches. The ``RECOMMENDS_STORAGE_COMMIT_THRESHOLD`` setting set how many record should be committed in each batch. Defaults to ``1000``.

``RECOMMENDS_STORAGE_DATABASE_ALIAS`` is used as the database where similarities and suggestions will be stored. Note that you will have to add ``recommends.storage.djangoorm.routers.RecommendsRouter`` to your settings' ``DATABASE_ROUTERS`` if you want to use something else than the default database. Default value is set to ``'recommends'``.

To minimize disk I/O from the database, Similiarities and Suggestions will be committed in batches. The ``RECOMMENDS_STORAGE_COMMIT_THRESHOLD`` setting sets how many record should be committed in each batch. Defaults to ``1000``.

Using the router requires at least Django 1.3 rev16869 (which includes fixes not present in Django 1.3.1). You can install Django 1.3-svn running ``pip install svn+http://code.djangoproject.com/svn/django/branches/releases/1.3.X#egg=Django``.

MongoStorage
------------

Settings
~~~~~~~~

``RECOMMENDS_STORAGE_REDIS_DATABASE``: A dictionary representing how to connect to the mongodb server. Defaults to:

::

	{
	    'HOST': 'localhost',
	    'PORT': 27017,
	    'NAME': 'recommends'
	}

RedisStorage
------------

This storage allows you to store results in Redis.

Settings
~~~~~~~~

``RECOMMENDS_STORAGE_REDIS_DATABASE``: A dictionary representing how to connect to the redis server. Defaults to:

::

	{
	    'HOST': 'localhost',
	    'PORT': 6379,
	    'NAME': 0
	}
