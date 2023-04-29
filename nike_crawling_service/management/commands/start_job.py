from django.core.management.base import BaseCommand, CommandError
from nike_crawling_service.controller.crawling_controller import get_product
from nike_crawling_service.util.string_util import to_boolean


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--parsing_option', type=str)
        parser.add_argument('--test', type=str)

    def handle(self, *args, **options):
        parsing_option = self.get_value(options, 'parsing_option', 'none')
        test = to_boolean(self.get_value(options, 'test', False))

        self.stdout.write(f'Start job.\n- parsing_option : {parsing_option}\n- test : {test}')

        result = get_product(parsing_option, test)

        self.stdout.write(f'End job.\n{result}')

    def get_value(self, options, key, default):
        if options[key]:
            return options[key]
        else:
            return default

