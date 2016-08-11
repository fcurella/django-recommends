.. ref-storages:

Storage backend
================

Results of the computation are stored according to the storage backend defined in ``RECOMMENDS_STORAGE_BACKEND`` (default to ``'recommends.storages.djangoorm.storage.DjangoOrmStorage'``). A storage backend defines how de/serialize and store/retrieve objects and results.

A storage backend can be any class extending ``recommends.storages.base.RecommendationStorage`` that implements the following methods and properties:

.. method:: get_identifier(self, obj, *args, **kwargs)

    Given an object and optional parameters, returns a string identifying the object uniquely.

.. method:: resolve_identifier(self, identifier)

    This method is the opposite of ``get_identifier``. It resolve the object's identifier to an actual model.

.. method:: get_similarities_for_object(self, obj, limit, raw_id=False)

    if raw_id = False:
        Returns a list of ``Similarity`` objects for given ``obj``, ordered by score.
    else:
        Returns a list of similar ``model`` ids[pk] for given ``obj``, ordered by score.

        Example:

    ::

        [
            {
                "related_object_id": XX, "content_type_id": XX
            },
            ..
        ]


.. method:: get_recommendations_for_user(self, user, limit, raw_id=False)

    if raw_id = False:
        Returns a list of :doc:`Recommendation <models>` objects for given ``user``, order by score.
    else:
        Returns a list of recommended ``model`` ids[pk] for given ``user``, ordered by score.

        Example:

    ::

        [
            {
                "object_id": XX, "content_type_id": XX
            },
            ..
        ]

.. method:: get_votes(self)

    Optional.

    Retrieves the vote matrix saved by ``store_votes``.

    You won't usually need to implement this method, because you want to use fresh data.
    But it might be useful if you want some kind of heavy caching, maybe for testing purposes.

.. method:: store_similarities(self, itemMatch)

.. method:: store_recommendations(self, user, recommendations)

    Stores all the recommendations.

    ``recommendations`` is an iterable with the following schema:

    ::

        (
            (
                <user>,
                (
                    (<object_identifier>, <score>),
                    (<object_identifier>, <score>)
                ),
            )
        )

.. method:: store_votes(self, iterable)

    Optional.

    Saves the vote matrix.

    You won't usually need to implement this method, because you want to use fresh data.
    But it might be useful if you want to dump the votes on somewhere, maybe for testing purposes.

    ``iterable`` is the vote matrix, expressed as a list of tuples with the following schema:

    ::

        [
            ("<user_id1>", "<object_identifier1>", <score>),
            ("<user_id1>", "<object_identifier2>", <score>),
            ("<user_id2>", "<object_identifier1>", <score>),
            ("<user_id2>", "<object_identifier2>", <score>),
        ]

.. method:: remove_recommendations(self, obj)

    Deletes all recommendations for object ``obj``.

.. method:: remove_similarities(self, obj)

    Deletes all similarities that have object ``obj`` as source or target.

.. method:: get_lock(self)

    Optional. Acquires an exclusive lock on the storage is acquired. Returns ``True`` if the lock is aquired, or ``False`` if the lock is already acquired by a previous process.

.. method:: release_lock(self)

    Optional. Releases the lock acquired with the ``get_lock`` method.

.. property:: can_lock


    Optional. Determines if the storage provides its own locking mechanism. Defaults to ``False``, meaning the default file-base locking will be used.

RedisStorage
------------

This storage allows you to store results in Redis. This is the recommended storage backend, but it is not the default because it requires you to install redis-server.

Options
~~~~~~~

``threshold_similarities`` Defaults to ``0``. Only similarities with score greater than ``threshold similarities`` will be persisted.

``threshold_recommendations`` Defaults to ``0``. Only recommendations with score greater than ``threshold similarities`` will be persisted.

Settings
~~~~~~~~

``RECOMMENDS_STORAGE_REDIS_DATABASE``: A dictionary representing how to connect to the redis server. Defaults to:

::

	{
	    'HOST': 'localhost',
	    'PORT': 6379,
	    'NAME': 0
	}

DjangoOrmStorage
----------------

This is the default storage. It requires minimal installation, but it's also the less performant.

This storage allows you to store results in a database specified by your ``DATABASES`` setting.

In order to use this storage, you'll also need to add ``'recommends.storages.djangoorm'`` to your ``INSTALLED_APPS``.

Options
~~~~~~~

``threshold_similarities`` Defaults to ``0``. Only similarities with score greater than ``threshold similarities`` will be persisted.

``threshold_recommendations`` Defaults to ``0``. Only recommendations with score greater than ``threshold similarities`` will be persisted.

Settings
~~~~~~~~

To minimize disk I/O from the database, Similiarities and Suggestions will be committed in batches. The ``RECOMMENDS_STORAGE_COMMIT_THRESHOLD`` setting set how many record should be committed in each batch. Defaults to ``1000``.

``RECOMMENDS_STORAGE_DATABASE_ALIAS`` is used as the database where similarities and suggestions will be stored. Note that you will have to add ``recommends.storages.djangoorm.routers.RecommendsRouter`` to your settings' ``DATABASE_ROUTERS`` if you want to use something else than the default database. Default value is set to ``'recommends'``.


MongoStorage
------------

Options
~~~~~~~

``threshold_similarities`` Defaults to ``0``. Only similarities with score greater than ``threshold similarities`` will be persisted.

``threshold_recommendations`` Defaults to ``0``. Only recommendations with score greater than ``threshold similarities`` will be persisted.

Settings
~~~~~~~~

``RECOMMENDS_STORAGE_MONGODB_DATABASE``: A dictionary representing how to connect to the mongodb server. Defaults to:

::

	{
	    'HOST': 'localhost',
	    'PORT': 27017,
	    'NAME': 'recommends'
	}

``RECOMMENDS_STORAGE_MONGODB_FSYNC``: Boolean specifying if MongoDB should force writes to the disk. Default to ``False``.
