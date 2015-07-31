.. ref-quickstart:

Quickstart
-----------
1. Install ``django-recommends`` with::

    $ pip install django-recommends

2. Create a RecommendationProvider for your models, and register it in your ``AppConfig`` (see :doc:`providers`)

3. Add ``'recommends'`` and ``'recommends.storages.djangoorm'`` to ``INSTALLED_APPS``

4. Run ``syncdb``

