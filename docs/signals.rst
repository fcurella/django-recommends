Signals
=======

When a signal specified in the provider is fired up by the one of the rated models, Django-recommends automaticaly calls a function with the same name.

You can override this function or connect to a different set of signals on the provider using the `signals` property::

    from django.db.models.signals import post_save, post_delete

    class MyProvider(DjangoRecommendationProvider):
        signals = ['django.db.models.post_save', 'django.db.models.pre_delete']

        def post_save(self, sender, instance, **kwargs):
            # Code that handles what should happen…

        def pre_delete(self, sender, instance, **kwargs):
            # Code that handles what should happen…


By default, a ``RecommendationProvider`` registers a function with the ``pre_delete`` signal that removes the suggestion for the deleted rated object (via its storage's ``remove_recommendation`` and ``remove_similarity`` methods).

