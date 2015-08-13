from collections import defaultdict
import math
from recommends.similarities import sim_distance
from recommends.converters import convert_vote_list_to_userprefs, convert_vote_list_to_itemprefs
from .base import BaseAlgorithm


class GhettoAlgorithm(BaseAlgorithm):
    """
    """
    similarity = sim_distance

    def top_matches(self, prefs, p1):
        """
        Returns the best matches for p1 from the prefs dictionary.
        """
        return [(p2, self.similarity(prefs[p1], prefs[p2])) for p2 in prefs if p2 != p1]

    def calculate_similarities(self, vote_list, verbose=0):
        # Invert the preference matrix to be item-centric
        itemPrefs = convert_vote_list_to_itemprefs(vote_list)
        itemMatch = {}
        for item in itemPrefs:
            # Find the most similar items to this one
            itemMatch[item] = self.top_matches(itemPrefs, item)
        iteritems = itemMatch.items()
        return iteritems

    def get_recommended_items(self, vote_list, itemMatch, itemIgnored, user):
        prefs = convert_vote_list_to_userprefs(vote_list)
        itemMatch = dict(itemMatch)

        if user in prefs:
            userRatings = prefs[user]
            scores = defaultdict(int)
            totalSim = defaultdict(int)

            # Loop over items rated by this user
            for (item, rating) in userRatings.items():
                # Loop over items similar to this one
                for (item2, similarity) in itemMatch[item]:
                    # Skip ignored items
                    if user.pk in itemIgnored and item2 in itemIgnored[user.pk]:
                        continue
                    # Ignore if this user has already rated this item
                    if not math.isnan(similarity) and item2 not in userRatings:
                        # Weighted sum of rating times similarity
                        scores[item2] += similarity * rating

                        # Sum of all the similarities
                        totalSim[item2] += similarity

            # Divide each total score by total weighting to get an average
            rankings = ((item, (score / totalSim[item])) for item, score in scores.items() if totalSim[item] != 0)
            return rankings
        return []

    def calculate_recommendations(self, vote_list, itemMatch, itemIgnored):
        """
        ``itemMatch`` is supposed to be the result of ``calculate_similarities()``

        Returns a list of recommendations:

        ::

            [
                (<user1>, [
                    ("<object_identifier1>", <score>),
                    ("<object_identifier2>", <score>),
                ]),
                (<user2>, [
                    ("<object_identifier1>", <score>),
                    ("<object_identifier2>", <score>),
                ]),
            ]

        """
        recommendations = []
        users = set(map(lambda x: x[0], vote_list))
        for user in users:
            rankings = self.get_recommended_items(vote_list, itemMatch, itemIgnored, user)
            recommendations.append((user, rankings))
        return recommendations
