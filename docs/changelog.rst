.. ref-changelog:

Changelog
=========

* v0.0.7
    * added Mongodb storage
    * added redis storage
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
