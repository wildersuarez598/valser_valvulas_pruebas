"""
Señales de Django para crear y actualizar objetos automáticamente
"""
from django.db.models.signals import post_save
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
