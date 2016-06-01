import os
from setuptools import setup, find_packages

VERSION = "0.3.10"


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''

requirements = read('requirements.txt').splitlines()

setup(
    name="django-recommends",
    version=VERSION,
    description="A django app that builds item-based suggestions for users",
    long_description=read('README.rst'),
    url='https://github.com/python-recsys/django-recommends',
    license='MIT',
    author='Flavio Curella',
    author_email='flavio.curella@gmail.com',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    install_requires=requirements,
)
