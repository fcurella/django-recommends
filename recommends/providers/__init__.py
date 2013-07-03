import logging
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from ..converters import model_path
from ..settings import RECOMMENDS_STORAGE_BACKEND, RECOMMENDS_LOGGER_NAME
from ..tasks import remove_suggestions, remove_similarities
from ..utils import import_from_classname
from ..algorithms.ghetto import GhettoAlgorithm


logger = logging.getLogger(RECOMMENDS_LOGGER_NAME)


class RecommendationProviderRegistry(object):
    _vote_providers = {}
    _content_providers = {}
    providers = set()

    def __init__(self):
        StorageClass = import_from_classname(RECOMMENDS_STORAGE_BACKEND)
        self.storage = StorageClass(settings)

    def register(self, vote_model, content_models, Provider):
        provider_instance = Provider()
        self._vote_providers[model_path(vote_model)] = provider_instance
        for model in content_models:
            self._content_providers[model_path(model)] = provider_instance

        self.providers.add(provider_instance)

        for signal in provider_instance.rate_signals:
            if isinstance(signal, str):
                sig_class_name = signal.split('.')[-1]
                sig_instance = import_from_classname(signal)
                listener = getattr(provider_instance, sig_class_name, False)
                if listener:
                    for model in content_models:
                        sig_instance.connect(listener, sender=model)

    def unregister(self, vote_model, content_models, Provider):
        provider_instance = Provider()

        for signal in provider_instance.rate_signals:
            if isinstance(signal, str):
                sig_class_name = signal.split('.')[-1]
                sig_instance = import_from_classname(signal)
                listener = getattr(provider_instance, sig_class_name, False)
                if listener:
                    for model in content_models:
                        sig_instance.disconnect(listener, sender=model)

        new_set = [i for i in self.providers if not isinstance(i, Provider)]
        self.providers = set(new_set)

        for model in content_models:
            del self._content_providers[model_path(model)]
        del self._vote_providers[model_path(vote_model)]

    def get_provider_for_vote(self, model):
        return self._vote_providers[model_path(model)]

    def get_provider_for_content(self, model):
        return self._content_providers[model_path(model)]

    def get_vote_providers(self):
        return self._vote_providers.values()

recommendation_registry = RecommendationProviderRegistry()


class Rating(object):
    def __init__(self, user, rated_object, rating):
        self.user = user
        self.rated_object = rated_object
        self.rating = rating


class RecommendationProvider(object):
    """
    A ``RecommendationProvider`` specifies how to retrieve various informations (items, users, votes)
    necessary for computing recommendation and similarities for a set of objects.

    Subclasses override methods in order to determine what constitutes voted items, a vote,
    its score, and user.
    """
    rate_signals = ['django.db.models.signals.pre_delete']
    algorithm = GhettoAlgorithm()

    def __init__(self):
        if not getattr(self, 'storage', False):
            self.storage = recommendation_registry.storage

    def get_items(self):
        """Return items that have been voted."""
        raise NotImplementedError

    def get_ratings(self, obj):
        """Returns all ratings for given item."""
        raise NotImplementedError

    def get_rating_user(self, rating):
        """Returns the user who performed the rating."""
        raise NotImplementedError

    def get_rating_score(self, rating):
        """Returns the score of the rating."""
        raise NotImplementedError

    def get_rating_item(self, rating):
        """Returns the rated object."""
        raise NotImplementedError

    def get_rating_site(self, rating):
        """Returns the site of the rating. Can be a ``Site`` object or its ID.

        Defaults to ``settings.SITE_ID``."""
        return settings.SITE_ID

    def is_rating_active(self, rating):
        """Returns if the rating is active."""
        return True

    def pre_delete(self, sender, instance, **kwargs):
        """
        This function gets called when a signal in ``self.rate_signals`` is
        fired from one of the rated model.

        Overriding this method is optional. The default method removes the
        suggestions for the deleted objected.

        See :doc:`signals`.
        """
        remove_similarities.delay(rated_model=model_path(sender), object_id=instance.id)
        remove_suggestions.delay(rated_model=model_path(sender), object_id=instance.id)

    def vote_list(self):
        vote_list = self.storage.get_votes()
        if vote_list is None:
            vote_list = []
            for item in self.get_items():
                for rating in self.get_ratings(item):
                    user = self.get_rating_user(rating)
                    score = self.get_rating_score(rating)
                    site = self.get_rating_site(rating)
                    if isinstance(site, Site):
                        site_id = site.id
                    else:
                        site_id = site
                    identifier = self.storage.get_identifier(item, site_id)
                    vote_list.append((user, identifier, score))
            self.storage.store_votes(vote_list)
        return vote_list

    def items_ignored(self):
        """
        Returns user ignored items.
        User can delete items from the list of recommended.

        See recommends.converters.IdentifierManager.get_identifier for help.
        ::

            {<user1>: ["object_identifier1",..., "object_identifierN"], ..}
        """
        return {}

    def precompute(self, vote_list=None):
        """
        This function will be called by the task manager in order
        to compile and store the results.

        Returns a dictionary contains count of recommended and similar items
        ::
            {<similar_count>: XX, <recommend_count>: XX}
        """
        if vote_list is None:
            logger.info('fetching votes from the provider...')
            vote_list = self.vote_list()
        logger.info('calculating similarities...')
        self.algorithm.clear_cache()
        itemMatch = self.algorithm.calculate_similarities(vote_list)

        logger.info('saving similarities...')
        self.pre_store_similarities(itemMatch)
        self.storage.store_similarities(itemMatch)

        logger.info('fetching ignored items...')
        itemIgnored = self.items_ignored()

        logger.info('saving recommendations...')
        recommendItems = self.algorithm.calculate_recommendations(
            vote_list, itemMatch, itemIgnored)
        self.storage.store_recommendations(recommendItems)
        return {
            'similar_count': len(itemMatch),
            'recommend_count': len(recommendItems)}

    def get_users(self):
        """Returns all users who have voted something."""
        return User.objects.filter(is_active=True)

    def pre_store_similarities(self, itemMatch):
        """
        Optional. This method will get called right before passing the
        similarities to the storage. For example, you can override this method
        to do some stats or visualize the data.
        """
        pass
