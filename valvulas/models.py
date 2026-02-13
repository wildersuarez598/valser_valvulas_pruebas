from django.db import models
from clientes.models import Empresa


class Valvula(models.Model):
    """
    Modelo para representar las válvulas de los clientes
    Cada válvula pertenece a una empresa específica
    """
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='valvulas')
    numero_serie = models.CharField(max_length=100, unique=True)
    codigo_interno = models.CharField(max_length=100, blank=True)
    tipo = models.CharField(
        max_length=100,
        choices=[
            ('alivio', 'Válvula de Alivio'),
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
    presion_nominal = models.CharField(max_length=50, verbose_name="Presión Nominal")
    temperatura_nominal = models.CharField(max_length=50, blank=True, verbose_name="Temperatura Nominal")
    material = models.CharField(max_length=100, blank=True)
    ubicacion = models.CharField(max_length=255, help_text="Ubicación física de la válvula")
    estado = models.CharField(
        max_length=50,
        choices=[
            ('activa', 'Activa'),
            ('inactiva', 'Inactiva'),
            ('descartada', 'Descartada'),
        ],
        default='activa'
    )
    fecha_instalacion = models.DateField(null=True, blank=True)
    fecha_ultimo_servicio = models.DateField(null=True, blank=True, verbose_name="Fecha Último Servicio")
    fecha_ultima_calibracion = models.DateField(null=True, blank=True, verbose_name="Fecha Última Calibración")
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
        """Indica si la válvula requiere calibración"""
        if self.fecha_ultima_calibracion is None:
            return True
        # Aquí puedes agregar lógica para determinar si requiere calibración
        # Por ejemplo, si pasaron más de 12 meses
        from datetime import timedelta
        from django.utils import timezone
        dias_desde_calibracion = (timezone.now().date() - self.fecha_ultima_calibracion).days
        return dias_desde_calibracion > 365
    
    @property
    def requiere_mantenimiento(self):
        """Indica si la válvula requiere mantenimiento"""
        if self.fecha_ultimo_servicio is None:
            return True
        from datetime import timedelta
        from django.utils import timezone
        dias_desde_servicio = (timezone.now().date() - self.fecha_ultimo_servicio).days
        return dias_desde_servicio > 180


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
