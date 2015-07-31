Settings
========

Autodiscovery
-------------

By default, ``django-recommends`` will import and load any modules called
``recommendations`` within your apps.

You can change the default module name by setting ``RECOMMENDS_AUTODISCOVER_MODULE``
to the name that you want, or you can disable this behavior by setting it to ``False``.

Celery Task
-----------

Computations are done by a scheduled celery task.

The task is run every 24 hours by default, but can be overridden by the ``RECOMMENDS_TASK_CRONTAB`` setting::
    
    RECOMMENDS_TASK_CRONTAB = {'hour': '*/24'}

``RECOMMENDS_TASK_CRONTAB`` must be a dictionary of kwargs acceptable by celery.schedulers.crontab.

If you don’t want to run this task (maybe because you want to write your own), set ``RECOMMENDS_TASK_RUN = False``

Additionally, you can specify an expiration time for the task by using the ``RECOMMENDS_TASK_EXPIRES`` settings, which defaults to ``None``.

Template tags and filters cache timeout
---------------------------------------

RECOMMENDS_CACHE_TEMPLATETAGS_TIMEOUT controls how long template tags and fitlers cache their results. Default is 60 seconds.


Storage backend
---------------

``RECOMMENDS_STORAGE_BACKEND`` specifies which :doc:`storages` class to use for storing similarity and recommendations. Defaults to ``'recommends.storages.djangoorm.DjangoOrmStorage'``. Providers can override this settings using the ``storage`` property (see :doc:`providers`).

Logging
-------

``RECOMMENDS_LOGGER_NAME`` specifies which logger to use. Defaults to ``'recommends'``.
