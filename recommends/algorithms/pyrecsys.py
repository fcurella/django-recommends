from recsys.datamodel.data import Data
from recsys.algorithm.factorize import SVD
from .base import BaseAlgorithm
from recommends.converters import convert_vote_list_to_itemprefs


class RecSysAlgorithm(BaseAlgorithm):
    def __init__(self, k=100, *args, **kwargs):
        self.k = k
        super(RecSysAlgorithm, self).__init__(*args, **kwargs)

    @property
    def svd(self):
        return self.cache.get('svd', None)

    def setup_svd(self, vote_list):
        if self.svd is None:
            self.cache['svd'] = SVD()
            data = Data()

            for vote in vote_list:
                user_id = vote[0].id
                item_id = vote[1]
                value = float(vote[2])
                data.add_tuple((value, item_id, user_id))  # Tuple format is: <value, row, column>
            self.cache['svd'].set_data(data)
            self.cache['svd'].compute(k=self.k, min_values=1)
        return self.svd

    def calculate_similarities(self, vote_list, verbose=0):
        svd = self.setup_svd(vote_list)

        itemPrefs = convert_vote_list_to_itemprefs(vote_list)
        itemMatch = {}
        for item in itemPrefs:
            itemMatch[item] = svd.similar(item)
        iteritems = itemMatch.items()
        return iteritems

    def calculate_recommendations(self, vote_list, itemMatch, itemIgnored):
        svd = self.setup_svd(vote_list)

        recommendations = []
        users = set(map(lambda x: x[0], vote_list))
        for user in users:
            try:
                rankings = svd.recommend(user.id, only_unknowns=True, is_row=False)
                recommendations.append((user, rankings))
            except KeyError:
                pass
        return recommendations
