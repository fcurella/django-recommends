Settings
========

Celery Task
-----------

Computations are done by a scheduled celery task. The task is run every 24 hours by default, but can be overridden by the ``RECOMMENDS_TASK_CRONTAB`` setting::
    
    RECOMMENDS_TASK_CRONTAB = {'hour': '*/24'}

``RECOMMENDS_TASK_CRONTAB`` must be a dictionary of kwargs acceptable by celery.schedulers.crontab.

Template tags and filters cache timeout
---------------------------------------

RECOMMENDS_CACHE_TEMPLATETAGS_TIMEOUT controls how long tample tags and fitlers cache their results. Default is 60 seconds.


Storage backend
---------------

RECOMMENDS_STORAGE_BACKEND specifies which :doc:`storages` class to use for storing similarity and recommendations. Defaults to ``'recommends.storages.DjangoOrmStorage'``.

if set, RECOMMENDS_STORAGE_ORM_DATABASE specifies which database recommends should use. Note that you will need to add ``recommends.storages.RecommendsRouter`` to the ``DATABASE_ROUTERS`` setting in order to store and read recommendations using a database diffeerent than ``'default'``.
