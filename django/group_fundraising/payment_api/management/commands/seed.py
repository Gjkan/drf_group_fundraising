from random import randint, choice
from django_seed import Seed
from payment_api.models import Payment, Collect, User
from django.core.management.base import BaseCommand
from faker import Faker
from django.conf import settings
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Command for filling DB by mock data'

    def handle(self, *args, **options):
        number = 2000
        fake = Faker()
        dates = [fake.date_time_between(start_date=now(), end_date='+2y') for _ in range(100)]
        seeder = Seed.seeder()
        seeder.add_entity(
            User,
            number,
            {
                'is_superuser': False,
                'is_staff': False,
                'email': settings.DJANGO_SUPERUSER_EMAIL,
            }
        )
        seeder.add_entity(
                          Collect,
                          number,
                          {
                              'number_of_people': 0,
                              'aim_sum': lambda x: randint(1, 1000000000),
                              'current_sum': 0,
                              'collect_lent': '',
                              'finish_collect_date_time': lambda x: choice(dates),
                          }
        )
        seeder.add_entity(
                          Payment,
                          number,
                          {
                              'payment': lambda x: randint(1, 100000),
                          }
        )
        seeder.execute()
