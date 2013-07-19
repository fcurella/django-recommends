from django.core.management.base import BaseCommand
from recommends.tasks import recommends_precompute

from datetime import datetime
import dateutil.relativedelta
from optparse import make_option

import warnings


class Command(BaseCommand):
    help = 'Calculate recommendations and similarities based on ratings'
    option_list = BaseCommand.option_list + (
        make_option('--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='verbose mode'
        ),
    )

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 0))
        if options['verbose']:
            warnings.warn('The `--verbose` option is being deprecated and it will be removed in the next release. Use `--verbosity` instead.', PendingDeprecationWarning)
            verbosity = 1

        if verbosity == 0:
            # avoids allocating the results
            recommends_precompute()
        else:
            self.stdout.write("\nCalculation Started.\n")
            start_time = datetime.now()
            results = recommends_precompute()
            end_time = datetime.now()
            if verbosity > 1:
                for r in results:
                    self.stdout.write(
                        "%d similarities and %d recommendations saved.\n"
                        % (r['similar_count'], r['recommend_count']))
            rd = dateutil.relativedelta.relativedelta(end_time, start_time)
            self.stdout.write(
                "Calculation finished in %d years, %d months, %d days, %d hours, %d minutes and %d seconds\n"
                % (rd.years, rd.months, rd.days, rd.hours, rd.minutes, rd.seconds))
