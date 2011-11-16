from django.utils import unittest
from django.contrib.auth.models import User
from recommends.tasks import recommends_precompute
from example_app.models import Product, Vote
from recommends.models import SimilarityResult, Recommendation


class RecommendsTestCase(unittest.TestCase):
    def setUp(self):
        self.mug = Product.objects.get(name='Coffee Mug')
        self.orange_juice = Product.objects.get(name='Orange Juice')
        self.user1 = User.objects.get(username='user1')

        recommends_precompute()

    def test_similarities(self):
        self.assertNotEquals(SimilarityResult.objects.count(), 0)

        # Make sure we didn't get all 0s
        self.assertNotEquals(SimilarityResult.objects.filter(score=0).count(), SimilarityResult.objects.count())

        similar_to_mug = SimilarityResult.objects.similar_to(self.mug, score__gt=0)
        self.assertEquals(similar_to_mug.count(), 1)
        self.assertEquals(similar_to_mug[0].get_related_object(), self.orange_juice)

    def test_recommendation(self):
        self.assertNotEquals(Recommendation.objects.count(), 0)

        # Make sure we didn't get all 0s
        self.assertNotEquals(Recommendation.objects.filter(score=0).count(), Recommendation.objects.count())

        recommended = Recommendation.objects.filter(user=self.user1)
        self.assertEquals(recommended.count(), 1)
        self.assertEquals(recommended[0].get_object(), self.mug)

        # Make sure we don't recommend item that the user already have
        self.assertFalse(self.mug in [v.product for v in Vote.objects.filter(user=self.user1)])
