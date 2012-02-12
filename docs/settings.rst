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

``RECOMMENDS_STORAGE_BACKEND`` specifies which :doc:`storages` class to use for storing similarity and recommendations. Defaults to ``'recommends.storages.djangoorm.DjangoOrmStorage'``. Providers can override this settings using the ``storage`` property (see :doc:`providers`).

Logging
-------

``RECOMMENDS_LOGGER_NAME`` specifies which logger to use. Defaults to ``'recommends'``.
