from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

superuser = os.environ['superuser']
superuseremail = os.environ['superuseremail']
superuserpass = os.environ['superuserpass']


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username=superuser).exists():
            User.objects.create_superuser(superuser, superuseremail, superuserpass)
