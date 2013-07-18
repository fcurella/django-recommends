Settings
========

Template tags and filters cache timeout
---------------------------------------

RECOMMENDS_CACHE_TEMPLATETAGS_TIMEOUT controls how long template tags and fitlers cache their results. Default is 60 seconds.


Storage backend
---------------

``RECOMMENDS_STORAGE_BACKEND`` specifies which :doc:`storages` class to use for storing similarity and recommendations. Defaults to ``'recommends.storages.djangoorm.DjangoOrmStorage'``. Providers can override this settings using the ``storage`` property (see :doc:`providers`).

Logging
-------

``RECOMMENDS_LOGGER_NAME`` specifies which logger to use. Defaults to ``'recommends'``.
