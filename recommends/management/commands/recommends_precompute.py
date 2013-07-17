from django.core.management.base import BaseCommand
from recommends.tasks import recommends_precompute

from datetime import datetime
import dateutil.relativedelta
from optparse import make_option


class Command(BaseCommand):
    help = 'Calculate recommendations and similarities based on ratings'

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 1))
        if verbosity == 0:
            results = recommends_precompute()
        else:
            if verbosity > 0:
                self.stdout.write("\nCalculation Started.\n")
            start_time = datetime.now()
            results = recommends_precompute()
            end_time = datetime.now()
            rd = dateutil.relativedelta.relativedelta(end_time, start_time)
            if verbosity > 1:
                for r in results:
                    self.stdout.write(
                        "%d similarities and %d recommendations saved.\n"
                        % (r['similar_count'], r['recommend_count']))
            if verbosity > 0:
                self.stdout.write(
                    "Calculation finished in %d years, %d months, %d days, %d hours, %d minutes and %d seconds\n"
                    % (rd.years, rd.months, rd.days, rd.hours, rd.minutes, rd.seconds))
