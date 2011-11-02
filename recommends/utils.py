from django.conf import settings
from .models import SimilarityResult, Recommendation
from .distances import sim_distance, sim_pearson
from .converters import get_object


def top_matches(prefs, person, n=5, similarity=sim_pearson):
    """
    Returns the best matches for person from the prefs dictionary.
    Number of results and similarity function are optional params.
    """

    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]


def get_recommendations(prefs, person, similarity=sim_pearson):
    """
    Gets recommendations for a person by using a weighted average
    of every other user's rankings
    """

    totals = {}
    simSums = {}
    for other in prefs:
        # don't compare me to myself
        if other == person:
            continue
        sim = similarity(prefs, person, other)

        # ignore scores of zero or lower
        if sim <= 0:
            continue
        for item in prefs[other]:

            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim
    # Create the normalized list
    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings


def transform_prefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # Flip item and person
            result[item][person] = prefs[person][item]
    return result


def calculate_similar_items(prefs, n=10, similarity=sim_distance):
    """
    Create a dictionary of items showing which other items they
    are most similar to.

    Output::

        {
            "<object_id>": [
                            (<score>, <related_object_id>),
                            (<score>, <related_object_id>),
            ],
            "<object_id>": [
                            (<score>, <related_object_id>),
                            (<score>, <related_object_id>),
            ],
        }
    """

    result = {}
    # Invert the preference matrix to be item-centric
    itemPrefs = transform_prefs(prefs)
    c = 0
    for item in itemPrefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0 and settings.DEBUG:
            print "%d / %d" % (c, len(itemPrefs))
        # Find the most similar items to this one
        scores = top_matches(itemPrefs, item, n=n, similarity=similarity)
        result[item] = scores
    return result


def store_calculate_similar_items(itemMatch, get_object_func=get_object):
    for object_id, scores in itemMatch.items():
        for score, related_object_id in scores:
            object_target = get_object_func(object_id)
            object_related = get_object_func(related_object_id)

            SimilarityResult.objects.set_score_for_objects(
                object_target=object_target,
                object_related=object_related,
                score=score
            )


def get_recommended_items(prefs, itemMatch, user):
    """
    itemMatch is supposed to be the result of ``calculate_similar_items()``

    Output::

        [
            (<score>, '<object_id>'),
            (<score>, '<object_id>'),
        ]
    """
    userRatings = prefs[user.id]
    scores = {}
    totalSim = {}

    # Loop over items rated by this user
    for (item, rating) in userRatings.items():

        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings:
                continue

            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item) for item, score in scores.items()]

    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings


def store_recommended_items(user, rankings, get_object_func=get_object):
    for score, object_id in rankings:
        object_recommended = get_object_func(object_id)
        Recommendation.objects.set_score_for_object(
            user=user,
            object_recommended=object_recommended,
            score=score
        )
