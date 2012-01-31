import timeit
from django.utils import unittest
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from example_app.models import Product, Vote
from recommends.tasks import recommends_precompute
from recommends.storages.djangoorm.models import Similarity, Recommendation


class RecommendsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.mug = Product.objects.get(name='Coffee Mug')
        self.orange_juice = Product.objects.get(name='Orange Juice')
        self.wine = Product.objects.get(name='Bottle of Red Wine')
        self.user1 = User.objects.get(username='user1')

        recommends_precompute()

    def test_similarities(self):
        self.assertNotEquals(Similarity.objects.count(), 0)

        # Make sure we didn't get all 0s
        self.assertNotEquals(Similarity.objects.filter(score=0).count(), Similarity.objects.count())

        # Make sure we didn't get all 1s
        self.assertNotEquals(Similarity.objects.filter(score=1).count(), Similarity.objects.count())

        similar_to_mug = Similarity.objects.similar_to(self.mug, score__gt=0)
        self.assertEquals(similar_to_mug.count(), 2)
        self.assertEquals(similar_to_mug[0].related_object, self.orange_juice)

    def test_recommendation(self):
        self.assertNotEquals(Recommendation.objects.count(), 0)

        # Make sure we didn't get all 0s
        self.assertNotEquals(Recommendation.objects.filter(score=0).count(), Recommendation.objects.count())

        recommended = Recommendation.objects.filter(user=self.user1.id)
        self.assertEquals(recommended.count(), 2)
        self.assertEquals(recommended[0].object, self.wine)

        # Make sure we don't recommend item that the user already have
        self.assertFalse(self.mug in [v.product for v in Vote.objects.filter(user=self.user1)])

    def test_views(self):
        self.client.login(username='user1', password='user1')

        response = self.client.get(reverse('home'))
        self.assertTrue(self.mug.get_absolute_url() in response.content)

        response = self.client.get(self.mug.get_absolute_url())
        self.assertTrue(self.orange_juice.get_absolute_url() in response.content)

    def _test_performance(self):
        stmt = """recommends_precompute()"""
        setup = """from recommends.tasks import recommends_precompute"""
        print "timing..."
        times = timeit.repeat(stmt, setup, number=100)
        print times


class RecommendsListenersTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.mug = Product.objects.get(name='Coffee Mug')
        self.orange_juice = Product.objects.get(name='Orange Juice')
        self.wine = Product.objects.get(name='Bottle of Red Wine')
        self.steak = Product.objects.get(name='1lb Tenderloin Steak')
        self.user1 = User.objects.get(username='user1')

        recommends_precompute()

    def test_listeners(self):
        self.client.login(username='user1', password='user1')
        response = self.client.get(reverse('home'))

        self.vote = Vote.objects.create(
            user=self.user1,
            product=self.steak,
            site_id=1,
            score=1
        )

        response = self.client.get(reverse('home'))
        steak_url = self.steak.get_absolute_url()
        self.assertTrue(steak_url in response.content)
        self.assertEqual(1L, Recommendation.objects.filter(user=self.user1.id, object_id=self.steak.id).count())
        self.steak.delete()

        response = self.client.get(reverse('home'))
        self.assertFalse(steak_url in response.content)
        self.assertEqual(0L, Recommendation.objects.filter(user=self.user1.id, object_id=self.steak.id).count())

    def tearDown(self):
        self.vote.delete()
        recommends_precompute()
