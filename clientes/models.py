from django.db import models


class Empresa(models.Model):
    """
    Modelo para almacenar información de las empresas clientes
    """
    nombre = models.CharField(max_length=255, unique=True)
    nit = models.CharField(max_length=50, unique=True, verbose_name="NIT")
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=500)
    ciudad = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20, blank=True)
    contacto_principal = models.CharField(max_length=255)
    cargo_contacto = models.CharField(max_length=255, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='logo_empresas/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.nit})"
    
    @property
    def ubicacion_completa(self):
        """Retorna la ubicación completa de la empresa"""
        return f"{self.ciudad}, {self.departamento}"
    
    @property
    def cantidad_valvulas(self):
        """Retorna la cantidad de válvulas registradas para esta empresa"""
        return self.valvulas.all().count()


class Contacto(models.Model):
    """
    Contactos adicionales de la empresa
    """
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='contactos')
    nombre = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    tipo_contacto = models.CharField(
        max_length=50,
        choices=[
            ('tecnico', 'Técnico'),
            ('administrativo', 'Administrativo'),
            ('compras', 'Compras'),
            ('otro', 'Otro'),
        ],
        default='administrativo'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ['empresa', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.empresa.nombre}"
