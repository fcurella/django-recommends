from math import sqrt


@staticmethod
def sim_distance(p1, p2):
    """Returns a distance-based similarity score for p1 and p2"""
    # Get the list of shared_items
    si = [item for item in p1 if item in p2]

    if len(si) != 0:
        squares = [pow(p1[item] - p2[item], 2) for item in si]
        # Add up the squares of all the differences
        sum_of_squares = sum(squares)
        return 1 / (1 + sqrt(sum_of_squares))
    return 0


@staticmethod
def sim_pearson(p1, p2):
    """
    Returns the Pearson correlation coefficient for p1 and p2
    """
    # Get the list of mutually rated items
    si = [item for item in p1 if item in p2]

    # Find the number of elements
    n = len(si)

    # if they have no ratings in common, return 0
    if n != 0:
        # Add up all the preferences
        sum1 = sum([p1[it] for it in si])
        sum2 = sum([p2[it] for it in si])

        # Sum up the squares
        sum1Sq = sum([pow(p1[it], 2) for it in si])
        sum2Sq = sum([pow(p2[it], 2) for it in si])

        # Sum up the products
        pSum = sum([p1[it] * p2[it] for it in si])

        # Calculate Pearson score
        num = pSum - (sum1 * sum2 / n)
        den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
        if den == 0:
            return 0
        r = num / den
        return r
    return 0
