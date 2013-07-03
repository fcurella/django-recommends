from django.core.management.base import NoArgsCommand
from recommends.tasks import recommends_precompute

from datetime import datetime
import dateutil.relativedelta


class Command(NoArgsCommand):
    help = 'Calculate recommendations and similarities based on ratings'

    def handle(self, *args, **options):
        self.stdout.write("\nCalculation Started.\n")
        start_time = datetime.now()
        results = recommends_precompute()
        end_time = datetime.now()
        rd = dateutil.relativedelta.relativedelta(end_time, start_time)
        for r in results:
            self.stdout.write(
                "%d similarities and %d recommendations saved.\n"
                % (r['similar_count'], r['recommend_count']))
        self.stdout.write(
            "Calculation finished in %d years, %d months, %d days, %d hours, %d minutes and %d seconds\n"
            % (rd.years, rd.months, rd.days, rd.hours, rd.minutes, rd.seconds))
