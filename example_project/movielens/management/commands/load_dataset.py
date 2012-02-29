import os
import codecs
import logging
from django.core.management.base import BaseCommand
from optparse import make_option
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from recommends.settings import RECOMMENDS_LOGGER_NAME
from movielens.models import Movie, Rating


logger = logging.getLogger(RECOMMENDS_LOGGER_NAME)


class Command(BaseCommand):
    """
    Shifts all publication date field values by a delta.
    """
    option_list = BaseCommand.option_list + (
        make_option('-d', '--dir', dest='dir',
            help="path to the directory dataset"),
    )
    help = """Load the movielens dataset into django model instances"""
    args = '--dir'

    movies_filename = 'u.item'
    users_filename = 'u.user'
    ratings_filename = 'u.data'

    separator = "\t"

    def handle(self, *args, **options):
        base_dir = options['dir']
        site = Site.objects.get_current()

        User.objects.exclude(is_superuser=True).delete()
        counter = 0
        users_fh = codecs.open(os.path.join(base_dir, self.users_filename), 'r', 'latin-1')
        for line in users_fh.readlines():
            row = line.split("|")
            obj, created = User.objects.get_or_create(username=row[0])
            if created:
                counter = counter + 1
                logger.info('%s: created user %s' % (counter, row[0]))
            else:
                logger.info('%s: skipped user %s' % (counter, row[0]))
        users_fh.close()
        logger.info('created %s users' % counter)

        Movie.objects.all().delete()
        counter = 0
        movies_fh = codecs.open(os.path.join(base_dir, self.movies_filename), 'r', 'latin-1')
        for line in movies_fh.readlines():
            row = line.split("|")
            obj, created = Movie.objects.get_or_create(pk=int(row[0]), title=row[1])
            if created:
                counter = counter + 1
                logger.info('%s: created movie %s' % (counter, row[1]))
            else:
                logger.info('%s: skipped movie %s' % (counter, row[0]))
        movies_fh.close()
        logger.info('created %s movies' % counter)

        Rating.objects.all().delete()
        counter = 0
        ratings_fh = codecs.open(os.path.join(base_dir, self.ratings_filename), 'r', 'latin-1')
        for line in ratings_fh.readlines():
            row = line.split("\t")

            user = User.objects.get(username=row[0])
            movie = Movie.objects.get(pk=int(row[1]))
            obj, created = Rating.objects.get_or_create(user=user, movie=movie, score=int(row[2]), site=site)
            if created:
                counter = counter + 1
                logger.info('%s: created rating %s -> %s: %s' % (counter, row[0], row[1], row[2]))
            else:
                logger.info('%s: skipped rating %s -> %s: %s' % (counter, row[0], row[1], row[2]))
        ratings_fh.close()
        logger.info('created %s ratings' % counter)
