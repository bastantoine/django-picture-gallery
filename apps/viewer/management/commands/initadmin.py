from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    ADMINS = [
        ('admin', 'admin@admin.com'),
    ]

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            for (username, email) in self.ADMINS:
                password = 'admin'
                print('Creating account for %s (%s)' % (username, email))
                admin = User.objects.create_superuser(email=email, username=username, password=password)
                admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')