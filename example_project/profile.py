#!/usr/bin/env python
import os
from recommends.tasks import recommends_precompute
from example_project.movielens import models


def main():
    recommends_precompute()


if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'example_project.settings'
    main()
