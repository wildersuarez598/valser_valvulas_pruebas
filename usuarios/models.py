from django.db import models
from django.contrib.auth.models import User
import pytz


# Zonas horarias por país/región
ZONAS_HORARIAS = [
    ('UTC', 'UTC (Tiempo Universal)'),
    ('America/Bogota', 'Colombia (UTC-5)'),
    ('America/Guatemala', 'Guatemala (UTC-6)'),
    ('America/Mexico_City', 'México (UTC-6)'),
    ('America/Costa_Rica', 'Costa Rica (UTC-6)'),
    ('America/Panama', 'Panamá (UTC-5)'),
    ('America/Caracas', 'Venezuela (UTC-4)'),
    ('America/Lima', 'Perú (UTC-5)'),
    ('America/Argentina/Buenos_Aires', 'Argentina (UTC-3)'),
    ('America/Santiago', 'Chile (UTC-3)'),
    ('America/Sao_Paulo', 'Brasil (UTC-3)'),
    ('America/New_York', 'USA Este (UTC-5/-4)'),
    ('America/Chicago', 'USA Centro (UTC-6/-5)'),
    ('America/Denver', 'USA Montaña (UTC-7/-6)'),
    ('America/Los_Angeles', 'USA Oeste (UTC-8/-7)'),
    ('Europe/Madrid', 'España (UTC+1/+2)'),
    ('Europe/London', 'Reino Unido (UTC+0/+1)'),
    ('Europe/Paris', 'Francia (UTC+1/+2)'),
    ('Europe/Berlin', 'Alemania (UTC+1/+2)'),
    ('Asia/Dubai', 'Emiratos (UTC+4)'),
    ('Asia/Bangkok', 'Tailandia (UTC+7)'),
    ('Asia/Shanghai', 'China (UTC+8)'),
    ('Asia/Tokyo', 'Japón (UTC+9)'),
    ('Asia/Kolkata', 'India (UTC+5:30)'),
    ('Australia/Sydney', 'Australia (UTC+10/+11)'),
]


class RoleUser(models.TextChoices):
    """Roles disponibles en el sistema"""
    CLIENTE = 'cliente', 'Cliente'
    COMERCIAL = 'comercial', 'Comercial'
    ADMIN = 'admin', 'Administrador'


class PerfilUsuario(models.Model):
    """
    Perfil extendido del Usuario
    Relacionado con el modelo User de Django
    """
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(
        max_length=20, 
        choices=RoleUser.choices, 
        default=RoleUser.CLIENTE
    )
    empresa = models.ForeignKey(
        'clientes.Empresa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )
    zona_horaria = models.CharField(
        max_length=50,
        choices=ZONAS_HORARIAS,
        default='America/Bogota',
        help_text='Zona horaria del usuario para mostrar fechas y horas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_rol_display()}"
    
    def es_cliente(self):
        """Verifica si el usuario es cliente"""
        return self.rol == RoleUser.CLIENTE
    
    def es_comercial(self):
        """Verifica si el usuario es comercial"""
        return self.rol == RoleUser.COMERCIAL
    
    def es_admin(self):
        """Verifica si el usuario es administrador"""
        return self.rol == RoleUser.ADMIN


class LogActividad(models.Model):
    """
    Registro de actividades de usuarios
    Para auditoría y seguimiento
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='log_actividades')
    accion = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    direccion_ip = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Log de Actividad"
        verbose_name_plural = "Logs de Actividades"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.accion} ({self.fecha})"
