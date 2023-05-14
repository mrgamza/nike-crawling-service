from django.core.management.base import BaseCommand
from nike_crawling_service.controller.CrawlingController import get_product
from nike_crawling_service.util.StringUtil import to_boolean


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--parsing_option', type=str)
        parser.add_argument('--recipients', type=str)

    def handle(self, *args, **options):
        parsing_option = self.get_value(options, 'parsing_option', '')
        recipients = self.get_value(options, 'recipients', '')

        self.stdout.write(f'Start job.\n- parsing_option : {parsing_option}\n- recipients : {recipients}')

        result = get_product(parsing_option, recipients)

        self.stdout.write(f'End job.\n{result}')

    def get_value(self, options, key, default):
        if options[key]:
            return options[key]
        else:
            return default

