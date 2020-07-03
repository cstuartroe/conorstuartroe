from django.core.management.base import BaseCommand, CommandError
from lauvinko.lang.tests import main

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        main()