from django.core.management.base import BaseCommand
from datetime import datetime
from pytz import timezone

from nike_crawling_service.controller import CrawlingController

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--recipients', type=str)
        parser.add_argument('--date', type=str)
        parser.add_argument('--time', type=str)

    def handle(self, *args, **options):
        recipients = self.get_value(options, 'recipients', None)

        if recipients is None:
            print({"status": "required field not found"})
            return None

        now = datetime.now(timezone('Asia/Seoul'))
        date = self.get_value(options, 'date', f'{now.year}-{now.month}-{now.day}')
        date_split = list(map(int, date.split("-")))

        year = date_split[0]
        month = date_split[1]
        day = date_split[2]
        
        time = self.get_value(options, 'time', None)

        self.stdout.write(f'Start job.')

        result = CrawlingController.get_product(year, month, day, time, recipients)

        self.stdout.write(result)
        self.stdout.write(f'End job.')

    def get_value(self, options, key, default):
        if options[key]:
            return options[key]
        else:
            return default

