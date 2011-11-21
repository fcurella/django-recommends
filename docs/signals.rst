Signals
=======

Django-recommends automaticaly connect a function called ``on_rate`` to the ``post_save`` signal of the rating model.

By default, this function removes the suggestion for the rated instance for the user that just rated, via a celery task.

You can override this function and connect to a different set of signals on the provider::
    from django.db.models.signals import post_save, post_delete

    class MyProvider(DjangoRecommendationProvider):
        signals = [post_save, post_delete]

        def on_signal(self, sender, instance, **kwargs):
            # Code that hadnles what should happen…
