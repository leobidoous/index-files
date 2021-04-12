import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Starter Celery process'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flower',
            action='store_true',
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        try:
            command = "celery -A indexes worker -l info | celery -A indexes beat -l info "
            if options['flower']:
                command = "celery -A indexes flower -l info --basic_auth=dev:mudar.dev | celery -A indexes worker -B -l info"
            os.system(command)
        except Exception as e:
            self.stdout.write(self.style.ERROR("Erro ao startar o celery"))

