from django.core.management.base import BaseCommand
from faker import Faker

from organization.models import Subsidiary


class Command(BaseCommand):
    help = 'Generate random data for Subsidiary model'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of subsidiaries to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']

        for _ in range(total):
            Subsidiary.objects.create(
                name=fake.company()
            )

        self.stdout.write(self.style.SUCCESS(f'{total} subsidiary created successfully!'))
