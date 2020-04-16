.. ref-changelog:

Changelog
=========
* v1.0.0
    * Drop support for Python 2
    * Drop support for Django 1.10
    * Add support for Django 1.11 up to Django 2.1
* v0.4.0
    * Drop support for Django 1.7.
    * Add support for Django 1.10.
* v0.3.11
    * Start deprecating ``GhettoAlgorithm`` in favor of ``NaiveAlgorithm``.
* v0.3.1
    * Fix wrong import
* v0.3.0
    * Added support for Django 1.9.
* v0.2.2
    * Added Python 3.3 Trove classifier to `setup.py`.
* v0.2.1
    * Added Python 3.4 Trove classifier to `setup.py`.
* v0.2.0
    * Added support for Python 3.4
    * Dropped support for Celery 2.x
* v0.1.0
    * Django 1.8 compatibility. Removed support for Django 1.6.
    * Added Providers autodiscovery.
* v0.0.22
    * Django 1.7 compatibility. Thanks Ilya Baryshev.
* v0.0.21
    * Release lock even if an exception is raised.
* v0.0.20
    * Removed lock expiration in Redis Storage.
* v0.0.19
    * added storages locking. Thanks Kirill Zaitsev.
* v0.0.16
    * renamed ``--verbose`` option to ``--verbosity``.
    * The ``recommends_precompute`` method is available even with ``RECOMMENDS_TASK_RUN = False``.
* v0.0.15
    * added ``--verbose`` option to ``recommends_precompute`` command.
* v0.0.14
    * more verbose ``recommends_precompute`` command. Thanks WANG GAOXIANG.
    * Introduced ``raw_id` parameter for lighter queries. WANG GAOXIANG.
    * Introduced ``RECOMMENDS_STORAGE_MONGODB_FSYNC`` setting.
* v0.0.13
    * Use ``{}`` instead of ``dict()`` for better performance.
* v0.0.12
    * python 3.3 and Django 1.5 compatibility
* v0.0.11
    * ``get_rating_site`` provider method now defaults to ``settings.SITE_ID`` instead of ``None``.
    * ``similarities`` templatetag result is now cached per object
    * fixed tests if ``recommends_precompute`` is None.
    * explicitly named celery tasks.
* v0.0.10
    * Added ``RecSysAlgorithm``.
* v0.0.9
    * Now tests can run in app's ./manage.py test. Thanks Andrii Kostenko.
    * Added support for ignored user recommendation. Thanks Maxim Gurets.
* v0.0.8
    * Added ``threshold_similarities`` and ``threshold_recommnedations`` to the storage backends.
* v0.0.7
    * added Mongodb storage
    * added Redis storage
    * added ``unregister`` method to the registry
* v0.0.6
	* added logging
	* DjangoOrmStorage now saves Similarities and Suggestions in batches, according to the new ``RECOMMENDS_STORAGE_COMMIT_THRESHOLD`` setting.
	* Decoupled Algorithms from Providers
* v0.0.5
	* Refactored providers registry
	* Renamed recommends.storages.django to recommends.storages.djangoorm to avoid name conflicts
	* Refactored DjangoOrmStorage and moved it to recommends.storages.djangoorm.storage
	* Added optional database router
* v0.0.4
	* Refactored providers to use lists of votes instead of dictionaries
	* fixed a critical bug where we ere calling the wrong method with the wrong signature.
* v0.0.3
	* Added filelocking to the pre-shipped precomputing task
	* Refactored signal handling, and added a task to remove similarities on pre_delete
	* Added optional hooks for storing and retrieving the vote matrix 
* v0.0.2
	* Added the ``RECOMMENDS_TASK_RUN`` setting
* v0.0.1
    * Initial Release
