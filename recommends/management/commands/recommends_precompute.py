from django.core.management.base import NoArgsCommand
from recommends.tasks import recommends_precompute


class Command(NoArgsCommand):
    def handle(self, *args, **options):
        recommends_precompute()
