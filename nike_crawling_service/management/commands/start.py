from django.core.management.base import BaseCommand
from nike_crawling_service.controller.CrawlingController import get_product
from datetime import datetime
from pytz import timezone


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--year', type=int)
        parser.add_argument('--month', type=int)
        parser.add_argument('--day', type=int)
        parser.add_argument('--recipients', type=str)

    def handle(self, *args, **options):
        now = datetime.now(timezone('Asia/Seoul'))

        year = self.get_value(options, 'year', now.year)
        month = self.get_value(options, 'month', now.month)
        day = self.get_value(options, 'day', now.day)
        recipients = self.get_value(options, 'recipients', None)

        if recipients is None:
            print({"status": "required field not found"})

        self.stdout.write(f'Start job.\n- year : {year}\n- month : {month}\n- day : {day}\n- recipients : {recipients}')

        result = get_product(year, month,day, recipients)

        self.stdout.write(f'End job.\n{result}')

    def get_value(self, options, key, default):
        if options[key]:
            return options[key]
        else:
            return default

