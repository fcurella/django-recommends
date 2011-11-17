from math import sqrt


def sim_distance(prefs, p1, p2):
    """Returns a distance-based similarity score for p1 and p2"""

    # Get the list of shared_items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    # if they have no ratings in common, return 0
    if len(si) != 0:
        squares = [pow(prefs[p1][item] - prefs[p2][item], 2) for item in si]
        # Add up the squares of all the differences
        sum_of_squares = sum(squares)
        return 1 / (1 + sqrt(sum_of_squares))
    return 0

def sim_pearson(prefs, p1, p2):
    """
    Returns the Pearson correlation coefficient for p1 and p2
    """
    # Get the list of mutually rated items
    si = {}

    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # Find the number of elements
    n = len(si)

    # if they have no ratings in common, return 0
    if n != 0:
        # Add up all the preferences
        sum1 = sum([prefs[p1][it] for it in si])
        sum2 = sum([prefs[p2][it] for it in si])

        # Sum up the squares
        sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
        sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

        # Sum up the products
        pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

        # Calculate Pearson score
        num = pSum - (sum1 * sum2 / n)
        den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
        if den == 0:
            return 0
        r = num / den
        return r
    return 0
