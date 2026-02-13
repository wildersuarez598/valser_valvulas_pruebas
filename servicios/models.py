from django.db import models
from django.contrib.auth.models import User
from valvulas.models import Valvula
from usuarios.models import PerfilUsuario


class Servicio(models.Model):
    """
    Modelo para registrar manteniamientos y calibraciones
    """
    TIPO_SERVICIO_CHOICES = [
        ('mantenimiento', 'Mantenimiento'),
        ('calibracion', 'Calibración'),
        ('reparacion', 'Reparación'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    valvula = models.ForeignKey(Valvula, on_delete=models.CASCADE, related_name='servicios')
    tipo_servicio = models.CharField(max_length=50, choices=TIPO_SERVICIO_CHOICES)
    fecha_servicio = models.DateField()
    descripcion = models.TextField(blank=True)
    tecnico = models.ForeignKey(
        PerfilUsuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'rol': 'comercial'},
        related_name='servicios_realizados'
    )
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='completado')
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['-fecha_servicio']
    
    def __str__(self):
        return f"{self.get_tipo_servicio_display()} - {self.valvula.numero_serie} ({self.fecha_servicio})"


class Certificado(models.Model):
    """
    Modelo para almacenar certificados de calibración y mantenimiento
    Contiene la información extraída del PDF
    """
    TIPO_CERTIFICADO_CHOICES = [
        ('calibracion', 'Calibración'),
        ('mantenimiento', 'Mantenimiento'),
    ]
    
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE, related_name='certificado', null=True, blank=True)
    usuario_comercial = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='certificados_subidos')
    tipo_certificado = models.CharField(max_length=50, choices=TIPO_CERTIFICADO_CHOICES)
    archivo_pdf = models.FileField(upload_to='certificados/%Y/%m/%d/')
    numero_certificado = models.CharField(max_length=100, unique=True, blank=True)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField(null=True, blank=True)
    
    # Datos extraídos del PDF
    presion_inicial = models.CharField(max_length=50, blank=True)
    presion_final = models.CharField(max_length=50, blank=True)
    temperatura = models.CharField(max_length=50, blank=True)
    resultado = models.CharField(max_length=50, blank=True)  # APROBADO/RECHAZADO
    notas_calibracion = models.TextField(blank=True)
    
    # Información del laboratorio/técnico
    laboratorio = models.CharField(max_length=255, blank=True)
    tecnico_responsable = models.CharField(max_length=255, blank=True)
    
    # Estado
    extraido_exitosamente = models.BooleanField(default=False, help_text="Indica si los datos fueron extraídos exitosamente del PDF")
    fecha_extraccion_datos = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"
        ordering = ['-fecha_emision']
    
    def __str__(self):
        return f"Certificado {self.numero_certificado} - {self.get_tipo_certificado_display()}"
    
    @property
    def esta_vigente(self):
        """Verifica si el certificado está vigente"""
        if self.fecha_vencimiento is None:
            return True
        from django.utils import timezone
        return self.fecha_vencimiento >= timezone.now().date()


class AlertaServicio(models.Model):
    """
    Modelo para registrar alertas sobre servicios vencidos o próximos a vencer
    """
    TIPO_ALERTA_CHOICES = [
        ('proximamente_vencer', 'Próximamente a Vencer'),
        ('vencido', 'Vencido'),
        ('no_realizado', 'No Realizado'),
    ]
    
    valvula = models.ForeignKey(Valvula, on_delete=models.CASCADE, related_name='alertas_servicio')
    tipo_alerta = models.CharField(max_length=50, choices=TIPO_ALERTA_CHOICES)
    descripcion = models.TextField()
    fecha_alerta = models.DateTimeField(auto_now_add=True)
    resuelta = models.BooleanField(default=False)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Alerta de Servicio"
        verbose_name_plural = "Alertas de Servicio"
        ordering = ['-fecha_alerta']
    
    def __str__(self):
        return f"{self.get_tipo_alerta_display()} - {self.valvula.numero_serie}"
