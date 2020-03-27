#!/usr/bin/env python
import sys
from os import path

import django
from django.test.utils import get_runner

from django.conf import settings

PROJECT_DIR = path.dirname(path.realpath(__file__))


settings.configure(
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.messages',
        'django.contrib.sites',
        'django.contrib.admin',
        'django.contrib.sessions',
        'django.contrib.contenttypes',
        'recommends',
        'recommends.storages.djangoorm',
        'recommends.tests',
    ],
    ROOT_URLCONF='recommends.tests.urls',
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'DIRS': [
                path.join(PROJECT_DIR, 'templates'),
            ],
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    MIDDLEWARE=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ),
    BROKER_URL='redis://localhost:6379/0',
    CELERY_ALWAYS_EAGER=True,
    ALLOWED_HOSTS=['*'],
    SITE_ID=1,
    RECOMMENDS_TEST_REDIS=True,
    RECOMMENDS_TEST_MONGO=True,
    RECOMMENDS_TEST_RECSYS=True,
    RECOMMENDS_STORAGE_MONGODB_FSYNC=True,
    RECOMMENDS_TASK_RUN=True,
)


def runtests(*test_args):
    django.setup()
    runner_class = get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['recommends'])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
