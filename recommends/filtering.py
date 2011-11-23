import math
from collections import defaultdict
from .similarities import sim_distance, sim_pearson

# Most of this is adapted from: Programming collective intelligence, Toby Segaran, 2007


def top_matches(prefs, p1, similarity=sim_pearson):
    """
    Returns the best matches for p1 from the prefs dictionary.
    """

    return [(p2, similarity(prefs[p1], prefs[p2])) for p2 in prefs if p2 != p1]


def get_recommendations(prefs, person, similarity=sim_pearson):
    """
    Gets recommendations for a person by using a weighted average
    of every other user's rankings

    Returns a generator of tuples in the format::

        ("<object_identifier1>", <score>)

    """

    totals = defaultdict(int)
    simSums = defaultdict(int)

    for other in prefs:
        # don't compare me to myself
        if other != person:
            sim = similarity(prefs, person, other)
            # ignore scores of zero or lower
            if sim > 0:
                for item in prefs[other]:
                    # only score movies I haven't seen yet
                    if item not in prefs[person] or prefs[person][item] == 0:
                        # Similarity * Score
                        totals[item] += prefs[other][item] * sim
                        # Sum of similarities
                        simSums[item] += sim
    # Create the normalized list
    return ((item, (total / simSums[item])) for item, total in totals.iteritems())


def transform_prefs(prefs):
    result = defaultdict(dict)
    for person in prefs:
        for item in prefs[person]:
            # Flip item and person
            result[item][person] = prefs[person][item]
    return result


def calculate_similar_items(prefs, similarity=sim_distance, verbose=0):
    """
    Create an iterator of items showing which other items they
    are most similar to.

    Output:

    ::

        [
            ("<object_id>", [
                            (<related_object_id>, <score>),
                            (<related_object_id>, <score>),
            ]),
            ("<object_id>", [
                            (<related_object_id>, <score>),
                            (<related_object_id>, <score>),
            ]),
        ]
    """

    itemMatch = {}
    # Invert the preference matrix to be item-centric
    itemPrefs = transform_prefs(prefs)
    #[itemMatch.set(item, top_matches(itemPrefs, item, similarity=similarity)) for item in itemPrefs]
    for item in itemPrefs:
        # Find the most similar items to this one
        itemMatch[item] = top_matches(itemPrefs, item, similarity=similarity)
        iteritems = itemMatch.items()
    return iteritems


def get_recommended_items(prefs, itemMatch, user):
    """
    ``itemMatch`` is supposed to be the result of ``calculate_similar_items()``

    Output:

    ::

        [
            ('<object_id>', <score>),
            ('<object_id>', <score>),
        ]
    """
    if user in prefs:
        userRatings = prefs[user]
        scores = defaultdict(int)
        totalSim = defaultdict(int)
        itemMatch = dict(itemMatch)

        # Loop over items rated by this user
        for (item, rating) in userRatings.iteritems():
                # Loop over items similar to this one
            for (item2, similarity) in itemMatch[item]:
                # Ignore if this user has already rated this item
                if not math.isnan(similarity) and item2 not in userRatings:
                    # Weighted sum of rating times similarity
                    scores[item2] += similarity * rating

                    # Sum of all the similarities
                    totalSim[item2] += similarity

        # Divide each total score by total weighting to get an average
        rankings = ((item, (score / totalSim[item])) for item, score in scores.iteritems() if totalSim[item] != 0)
        return rankings
    return []
