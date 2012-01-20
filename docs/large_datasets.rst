.. ref-large_datasets:

Large Datasets
==============

Calculating item similarities is computationally heavy, in terms of cpu cycles, amount of RAM and database load.

Some strategy you can use to mitigate it includes:

* Parallelize the precomputing task. This could be achieved by disabling the default task (via ``RECOMMENDS_TASK_RUN = False``) and breaking it down to smaller tasks (one per app, or one per model), which will be distributed to different machines using dedicated celery queues.
 