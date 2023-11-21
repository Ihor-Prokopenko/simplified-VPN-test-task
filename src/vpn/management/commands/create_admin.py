from django.core.management.base import BaseCommand

from vpn.models import User


class Command(BaseCommand):
    help = 'Create admin'

    def handle(self, *args, **kwargs):
        try:
            User.objects.get(username='admin')
            self.stdout.write(self.style.SUCCESS('Admin already exists!'))
        except User.DoesNotExist:
            self.create_admin()

    def create_admin(self):
        try:
            user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin'
            )
            if user:
                user.save()
                self.stdout.write(self.style.SUCCESS('Admin created!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
