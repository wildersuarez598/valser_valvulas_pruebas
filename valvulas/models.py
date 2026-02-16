from django.db import models
from django.utils import timezone
from clientes.models import Empresa


class Valvula(models.Model):
    """
    Modelo para representar las válvulas de los clientes
    Cada válvula pertenece a una empresa específica
    Incluye campos para la Hoja de Vida de la válvula
    """
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='valvulas')
    numero_serie = models.CharField(max_length=100, unique=True, db_index=True)
    codigo_interno = models.CharField(max_length=100, blank=True)
    tipo = models.CharField(
        max_length=100,
        choices=[
            ('alivio', 'Válvula de Alivio/Seguridad'),
            ('control', 'Válvula de Control/Corte'),
            ('check', 'Válvula Check'),
            ('bola', 'Válvula de Bola'),
            ('aguja', 'Válvula de Aguja'),
            ('compuerta', 'Válvula de Compuerta'),
            ('otra', 'Otra'),
        ]
    )
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    tamaño = models.CharField(max_length=50)
    tag_localizacion = models.CharField(max_length=100, blank=True, help_text="TAG o identificador de ubicación")
    presion_nominal = models.CharField(max_length=50, verbose_name="Presión Nominal", blank=True)
    presion_set = models.CharField(max_length=50, blank=True, verbose_name="Presión SET", help_text="Para válvulas de seguridad")
    temperatura_nominal = models.CharField(max_length=50, blank=True, verbose_name="Temperatura Nominal")
    material = models.CharField(max_length=100, blank=True)
    ubicacion = models.CharField(max_length=255, help_text="Ubicación física de la válvula", blank=True)
    norma_aplicable = models.CharField(max_length=50, blank=True, help_text="ASME I, ASME VIII, etc")
    estado = models.CharField(
        max_length=50,
        choices=[
            ('activa', 'Activa'),
            ('inactiva', 'Inactiva'),
            ('descartada', 'Descartada'),
        ],
        default='activa'
    )
    
    # Historial mínimo para Hoja de Vida
    fecha_instalacion = models.DateField(null=True, blank=True)
    fecha_ultimo_servicio = models.DateField(null=True, blank=True, verbose_name="Fecha Último Servicio/Mantenimiento")
    fecha_ultima_calibracion = models.DateField(null=True, blank=True, verbose_name="Fecha Última Calibración")
    
    # Control de cambios
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Válvula"
        verbose_name_plural = "Válvulas"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.numero_serie} - {self.marca} {self.modelo}"
    
    @property
    def requiere_calibracion(self):
        """Indica si la válvula requiere calibración (intervalo: 365 días)"""
        if self.fecha_ultima_calibracion is None:
            return True
        dias_desde_calibracion = (timezone.now().date() - self.fecha_ultima_calibracion).days
        return dias_desde_calibracion > 365
    
    @property
    def requiere_mantenimiento(self):
        """Indica si la válvula requiere mantenimiento (intervalo: 180 días)"""
        if self.fecha_ultimo_servicio is None:
            return True
        dias_desde_servicio = (timezone.now().date() - self.fecha_ultimo_servicio).days
        return dias_desde_servicio > 180
    
    @property
    def dias_desde_ultima_calibracion(self):
        """Retorna días desde la última calibración, None si nunca fue calibrada"""
        if self.fecha_ultima_calibracion is None:
            return None
        return (timezone.now().date() - self.fecha_ultima_calibracion).days
    
    @property
    def dias_desde_ultimo_servicio(self):
        """Retorna días desde el último servicio/mantenimiento, None si nunca tuvo servicio"""
        if self.fecha_ultimo_servicio is None:
            return None
        return (timezone.now().date() - self.fecha_ultimo_servicio).days
    
    def obtener_documentos_recientes(self, limite=10):
        """
        Obtiene los documentos (calibración, mantenimiento) más recientes de esta válvula
        """
        from servicios.models import Documento
        return Documento.objects.filter(
            servicio__valvula=self,
            extraido_exitosamente=True
        ).order_by('-fecha_documento')[:limite]
    
    def obtener_ultima_calibracion(self):
        """Obtiene el documento de última calibración"""
        from servicios.models import Documento
        return Documento.objects.filter(
            servicio__valvula=self,
            tipo_documento='calibracion',
            extraido_exitosamente=True
        ).order_by('-fecha_documento').first()
    
    def obtener_ultimo_mantenimiento(self):
        """Obtiene el documento de último mantenimiento"""
        from servicios.models import Documento
        return Documento.objects.filter(
            servicio__valvula=self,
            tipo_documento__in=['mantenimiento', 'reparacion'],
            extraido_exitosamente=True
        ).order_by('-fecha_documento').first()


class EspecificacionTecnica(models.Model):
    """
    Especificaciones técnicas adicionales de la válvula
    """
    valvula = models.OneToOneField(Valvula, on_delete=models.CASCADE, related_name='especificaciones')
    presion_maxima_trabajo = models.CharField(max_length=50, blank=True)
    capacidad_flujo = models.CharField(max_length=100, blank=True)
    conexion_entrada = models.CharField(max_length=100, blank=True)
    conexion_salida = models.CharField(max_length=100, blank=True)
    rango_temperatura = models.CharField(max_length=100, blank=True)
    certificacion = models.CharField(max_length=255, blank=True)
    notas_tecnicas = models.TextField(blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Especificación Técnica"
        verbose_name_plural = "Especificaciones Técnicas"
    
    def __str__(self):
        return f"Especificaciones - {self.valvula.numero_serie}"
