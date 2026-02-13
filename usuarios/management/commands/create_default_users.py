from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create default users for testing'

    def handle(self, *args, **options):
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@valser.com',
                'password': 'admin123',
                'is_superuser': True,
                'is_staff': True,
            },
            {
                'username': 'comercial',
                'email': 'comercial@valser.com',
                'password': 'comercial123',
                'is_superuser': False,
                'is_staff': True,
            },
            {
                'username': 'cliente',
                'email': 'cliente@valser.com',
                'password': 'cliente123',
                'is_superuser': False,
                'is_staff': False,
            },
        ]

        for user_data in users_data:
            username = user_data['username']
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                )
                user.is_staff = user_data['is_staff']
                user.is_superuser = user_data['is_superuser']
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Usuario {username} creado'))
            else:
                self.stdout.write(self.style.WARNING(f'✅ Usuario {username} ya existe'))

        self.stdout.write(self.style.SUCCESS('\n📋 Credenciales:'))
        self.stdout.write('Admin:      admin / admin123')
        self.stdout.write('Comercial:  comercial / comercial123')
        self.stdout.write('Cliente:    cliente / cliente123')
