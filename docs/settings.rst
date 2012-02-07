Settings
========

Celery Task
-----------

Computations are done by a scheduled celery task. The task is run every 24 hours by default, but can be overridden by the ``RECOMMENDS_TASK_CRONTAB`` setting::
    
    RECOMMENDS_TASK_CRONTAB = {'hour': '*/24'}

``RECOMMENDS_TASK_CRONTAB`` must be a dictionary of kwargs acceptable by celery.schedulers.crontab.

If you don’t want to run this task (maybe because you want to write your own), set ``RECOMMENDS_TASK_RUN = False``

Template tags and filters cache timeout
---------------------------------------

RECOMMENDS_CACHE_TEMPLATETAGS_TIMEOUT controls how long tample tags and fitlers cache their results. Default is 60 seconds.


Storage backend
---------------

``RECOMMENDS_STORAGE_BACKEND`` specifies which :doc:`storages` class to use for storing similarity and recommendations. Defaults to ``'recommends.storages.djangoorm.DjangoOrmStorage'``.

``RECOMMENDS_STORAGE_DATABASE_NAME`` is used by ``DjangoOrmStorage`` as the database where similarities and suggestions will be stored. Note that you will have to add ``recommends.storage.djangoorm.routers.RecommendsRouter`` to your settings' ``DATABASE_ROUTERS`` if you want to use something else than the default database. Default value is set to ``'recommends'``.

To minimize disk I/O from the database, Similiarities and Suggestions will be committed in batches. The ``RECOMMENDS_STORAGE_COMMIT_THRESHOLD`` setting sets how many record should be committed in each batch. Defaults to ``1000``.

Using the router requires at least Django 1.3 rev16869 (which includes fixes not present in Django 1.3.1). You can install Django 1.3 with ``pip install svn+http://code.djangoproject.com/svn/django/branches/releases/1.3.X#egg=Django``.

 

Logging
-------

``RECOMMENDS_LOGGER_NAME`` specifies which logger to use. Defaults to ``'recommends'``.