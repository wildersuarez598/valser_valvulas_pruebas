"""
Señales de Django para crear y actualizar objetos automáticamente
"""
from django.db.models.signals import post_save
from django.core.management.sql import emit_post_migrate_signal
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PerfilUsuario


@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    """
    Crear automáticamente un PerfilUsuario cuando se crea un nuevo usuario
    """
    if created:
        PerfilUsuario.objects.create(usuario=instance)
    else:
        # Si el usuario existe, asegurar que tiene perfil
        try:
            instance.perfil
        except PerfilUsuario.DoesNotExist:
            PerfilUsuario.objects.create(usuario=instance)


# Auto-create default users after migrations
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_users(sender, app_config, **kwargs):
    """Create default users after migrations are complete."""
    if app_config and app_config.name == 'usuarios':
        users_data = [
            {'username': 'admin', 'email': 'admin@valser.com', 'password': 'admin123', 'is_superuser': True, 'is_staff': True},
            {'username': 'comercial', 'email': 'comercial@valser.com', 'password': 'comercial123', 'is_superuser': False, 'is_staff': True},
            {'username': 'cliente', 'email': 'cliente@valser.com', 'password': 'cliente123', 'is_superuser': False, 'is_staff': False},
        ]
        
        for user_data in users_data:
            username = user_data.pop('username')
            email = user_data.pop('email')
            password = user_data.pop('password')
            
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password, **user_data)

