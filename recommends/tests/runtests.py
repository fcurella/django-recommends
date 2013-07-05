#!/usr/bin/env python
import sys
from os import path

from django.conf import settings

PROJECT_DIR = path.dirname(path.realpath(__file__))


settings.configure(
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3'}
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'recommends',
        'recommends.storages.djangoorm',
        'recommends.tests',
    ],
    ROOT_URLCONF='recommends.tests.urls',
    TEMPLATE_DIRS=(
        path.join(PROJECT_DIR, 'templates'),
    ),
    BROKER_URL = 'redis://localhost:6379/0',
    CELERY_ALWAYS_EAGER = True,
    ALLOWED_HOSTS = ['*'],
    SITE_ID = 1,
    RECOMMENDS_TEST_REDIS = True,
    RECOMMENDS_TEST_MONGO = True,
    RECOMMENDS_TEST_RECSYS = True
)


def runtests(*test_args):
    import django.test.utils
    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['recommends'])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
