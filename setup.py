import os
from setuptools import setup, find_packages

from recommends import VERSION


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = [
    'django',
    'celery',
]

setup(
    name = "django-recommends",
    version = ".".join(map(str, VERSION)),
    description = "A django app that builds item-based suggestions for users",
    long_description = read('README.rst'),
    url = 'https://github.com/python-recsys/django-recommends',
    license = 'MIT',
    author = 'Flavio Curella',
    author_email = 'flavio.curella@gmail.com',
    packages = find_packages(exclude=['tests']),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Framework :: Django',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    install_requires = requirements,
)
