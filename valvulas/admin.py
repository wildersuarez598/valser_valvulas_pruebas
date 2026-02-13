from django.contrib import admin
from config.admin import admin_site
from .models import Valvula, EspecificacionTecnica


class EspecificacionTecnicaInline(admin.TabularInline):
    model = EspecificacionTecnica
    extra = 0
    fields = ('presion_maxima_trabajo', 'capacidad_flujo', 'conexion_entrada', 'conexion_salida')


class ValvulaAdmin(admin.ModelAdmin):
    list_display = ('numero_serie', 'codigo_interno', 'marca', 'modelo', 'empresa', 'estado', 'fecha_ultimo_servicio')
    list_filter = ('estado', 'tipo', 'empresa', 'fecha_ultimo_servicio')
    search_fields = ('numero_serie', 'codigo_interno', 'marca', 'modelo', 'empresa__nombre')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'requiere_calibracion', 'requiere_mantenimiento')
    inlines = [EspecificacionTecnicaInline]
    fieldsets = (
        ('Identificación', {
            'fields': ('numero_serie', 'codigo_interno', 'empresa')
        }),
        ('Especificaciones', {
            'fields': ('tipo', 'marca', 'modelo', 'tamaño', 'presion_nominal', 'temperatura_nominal', 'material')
        }),
        ('Ubicación y Estado', {
            'fields': ('ubicacion', 'estado')
        }),
        ('Fechas de Servicio', {
            'fields': ('fecha_instalacion', 'fecha_ultimo_servicio', 'fecha_ultima_calibracion')
        }),
        ('Avisos', {
            'fields': ('requiere_calibracion', 'requiere_mantenimiento')
        }),
        ('Notas', {
            'fields': ('observaciones',)
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'fecha_ultimo_servicio'


class EspecificacionTecnicaAdmin(admin.ModelAdmin):
    list_display = ('valvula', 'presion_maxima_trabajo', 'capacidad_flujo')
    list_filter = ('valvula__empresa',)
    search_fields = ('valvula__numero_serie', 'valvula__marca')
    readonly_fields = ('fecha_actualizacion',)
    fieldsets = (
        ('Válvula', {
            'fields': ('valvula',)
        }),
        ('Especificaciones Técnicas', {
            'fields': ('presion_maxima_trabajo', 'capacidad_flujo', 'conexion_entrada', 'conexion_salida', 'rango_temperatura')
        }),
        ('Certificación', {
            'fields': ('certificacion', 'notas_tecnicas')
        }),
        ('Auditoría', {
            'fields': ('fecha_actualizacion',),
            'classes': ('collapse',)
        }),
    )


admin_site.register(Valvula, ValvulaAdmin)
admin_site.register(EspecificacionTecnica, EspecificacionTecnicaAdmin)
