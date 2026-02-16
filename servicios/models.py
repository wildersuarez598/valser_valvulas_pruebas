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


class Documento(models.Model):
    """
    Modelo genérico para almacenar cualquier tipo de documento (Certificado, Informe, etc)
    Soporta múltiples documentos por servicio con extracción automática de datos
    """
    TIPO_DOCUMENTO_CHOICES = [
        ('calibracion', 'Certificado de Calibración'),
        ('mantenimiento', 'Informe de Mantenimiento'),
        ('reparacion', 'Informe de Reparación'),
        ('otro', 'Otro'),
    ]
    
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='documentos')
    usuario_comercial = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='documentos_subidos')
    tipo_documento = models.CharField(max_length=50, choices=TIPO_DOCUMENTO_CHOICES)
    archivo_pdf = models.FileField(upload_to='documentos/%Y/%m/%d/')
    nombre_original = models.CharField(max_length=255, blank=True, help_text="Nombre original del archivo")
    
    # Datos genéricos extraídos
    numero_documento = models.CharField(max_length=100, blank=True, db_index=True)
    fecha_documento = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    tecnico_responsable = models.CharField(max_length=255, blank=True)
    
    # Datos específicos para Calibración
    presion_inicial = models.CharField(max_length=50, blank=True)
    presion_final = models.CharField(max_length=50, blank=True)
    temperatura = models.CharField(max_length=50, blank=True)
    unidad_presion = models.CharField(max_length=20, blank=True)  # PSI, bar, atm, kPa
    resultado_calibracion = models.CharField(max_length=50, blank=True)  # APROBADO/RECHAZADO
    laboratorio = models.CharField(max_length=255, blank=True)
    
    # Datos específicos para Mantenimiento
    tipo_mantenimiento = models.CharField(max_length=100, blank=True)  # Preventivo/Correctivo
    descripcion_trabajos = models.TextField(blank=True)
    estado_valvula = models.CharField(max_length=100, blank=True)  # Bueno/Defectuoso
    materiales_utilizados = models.TextField(blank=True)
    duracion_horas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    proximo_mantenimiento = models.DateField(null=True, blank=True)
    
    # Estado de extracción
    extraido_exitosamente = models.BooleanField(default=False)
    error_extraccion = models.TextField(blank=True, help_text="Descripción del error si falló la extracción")
    fecha_extraccion_datos = models.DateTimeField(null=True, blank=True)
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ['-fecha_documento', '-fecha_creacion']
        indexes = [
            models.Index(fields=['tipo_documento', 'servicio']),
            models.Index(fields=['numero_documento']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_documento_display()} {self.numero_documento or 'Sin #'} - {self.servicio.valvula.numero_serie}"
    
    @property
    def esta_vigente(self):
        """Verifica si el documento está vigente"""
        if self.fecha_vencimiento is None:
            return True
        from django.utils import timezone
        return self.fecha_vencimiento >= timezone.now().date()
    
    @property
    def dias_para_vencer(self):
        """Retorna días faltantes para vencer (negativo si ya venció)"""
        if self.fecha_vencimiento is None:
            return None
        from django.utils import timezone
        delta = self.fecha_vencimiento - timezone.now().date()
        return delta.days


class Certificado(models.Model):
    """
    DEPRECATED: Modelo legado mantenido para compatibilidad con migraciones antiguas
    Usar modelo 'Documento' en su lugar
    """
    TIPO_CERTIFICADO_CHOICES = [
        ('calibracion', 'Calibración'),
        ('mantenimiento', 'Mantenimiento'),
    ]
    
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE, related_name='certificado_legacy', null=True, blank=True)
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
    resultado = models.CharField(max_length=50, blank=True)
    notas_calibracion = models.TextField(blank=True)
    
    # Información del laboratorio/técnico
    laboratorio = models.CharField(max_length=255, blank=True)
    tecnico_responsable = models.CharField(max_length=255, blank=True)
    
    # Estado
    extraido_exitosamente = models.BooleanField(default=False)
    fecha_extraccion_datos = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Certificado (Legado)"
        verbose_name_plural = "Certificados (Legado)"
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
