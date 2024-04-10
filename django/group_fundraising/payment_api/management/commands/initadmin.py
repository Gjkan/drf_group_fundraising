from django.core.management.base import BaseCommand
from payment_api.models import Payment, Collect, User
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
                admin = User.objects.create_superuser(email=settings.DJANGO_SUPERUSER_EMAIL, username=settings.DJANGO_SUPERUSER_USERNAME, password=settings.DJANGO_SUPERUSER_PASSWORD)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')