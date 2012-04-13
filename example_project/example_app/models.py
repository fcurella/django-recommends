from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from recommends.providers import recommendation_registry, RecommendationProvider
from recommends.algorithms.pyrecsys import RecSysAlgorithm


# Create your models here.
