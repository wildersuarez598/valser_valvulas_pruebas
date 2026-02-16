from django.contrib import admin
from .models import Servicio, Certificado, Documento, AlertaServicio


class CertificadoInline(admin.TabularInline):
    model = Certificado
    extra = 0
    fields = ('tipo_certificado', 'numero_certificado', 'fecha_emision', 'extraido_exitosamente')
    readonly_fields = ('extraido_exitosamente',)


class DocumentoInline(admin.TabularInline):
    model = Documento
    extra = 1
    fields = ('tipo_documento', 'numero_documento', 'fecha_documento', 'extraido_exitosamente', 'archivo_pdf')
    readonly_fields = ('tipo_documento', 'extraido_exitosamente')


class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'valvula', 'tipo_servicio', 'fecha_servicio', 'estado', 'tecnico')
    list_filter = ('tipo_servicio', 'estado', 'fecha_servicio', 'valvula__empresa')
    search_fields = ('valvula__numero_serie', 'valvula__marca', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    inlines = [DocumentoInline, CertificadoInline]
    fieldsets = (
        ('Información del Servicio', {
            'fields': ('valvula', 'tipo_servicio', 'fecha_servicio')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'observaciones')
        }),
        ('Personal', {
            'fields': ('tecnico', 'estado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'fecha_servicio'


class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('numero_certificado', 'servicio', 'tipo_certificado', 'fecha_emision', 'esta_vigente', 'extraido_exitosamente')
    list_filter = ('tipo_certificado', 'fecha_emision', 'extraido_exitosamente', 'servicio__valvula__empresa')
    search_fields = ('numero_certificado', 'servicio__valvula__numero_serie', 'laboratorio')
    readonly_fields = ('fecha_creacion', 'fecha_extraccion_datos', 'esta_vigente')
    fieldsets = (
        ('Información del Certificado', {
            'fields': ('servicio', 'tipo_certificado', 'numero_certificado')
        }),
        ('Fechas', {
            'fields': ('fecha_emision', 'fecha_vencimiento')
        }),
        ('Archivo', {
            'fields': ('archivo_pdf',)
        }),
        ('Datos Extraídos', {
            'fields': ('presion_inicial', 'presion_final', 'temperatura', 'resultado', 'extraido_exitosamente')
        }),
        ('Laboratorio', {
            'fields': ('laboratorio', 'tecnico_responsable')
        }),
        ('Notas', {
            'fields': ('notas_calibracion',)
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_extraccion_datos', 'esta_vigente'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'fecha_emision'


class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('numero_documento', 'get_tipo_documento', 'servicio', 'fecha_documento', 'extraido_exitosamente')
    list_filter = ('tipo_documento', 'fecha_documento', 'extraido_exitosamente', 'servicio__valvula__empresa')
    search_fields = ('numero_documento', 'servicio__valvula__numero_serie', 'laboratorio')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'fecha_extraccion_datos', 'esta_vigente', 'dias_para_vencer')
    fieldsets = (
        ('Información del Documento', {
            'fields': ('servicio', 'tipo_documento', 'numero_documento', 'usuario_comercial')
        }),
        ('Fechas', {
            'fields': ('fecha_documento', 'fecha_vencimiento', 'esta_vigente', 'dias_para_vencer')
        }),
        ('Archivo', {
            'fields': ('archivo_pdf', 'nombre_original')
        }),
        ('Calibración (si aplica)', {
            'fields': ('presion_inicial', 'presion_final', 'temperatura', 'resultado_calibracion', 'laboratorio', 'unidad_presion'),
            'classes': ('collapse',)
        }),
        ('Mantenimiento (si aplica)', {
            'fields': ('tipo_mantenimiento', 'descripcion_trabajos', 'estado_valvula', 'materiales_utilizados', 'proximo_mantenimiento', 'duracion_horas'),
            'classes': ('collapse',)
        }),
        ('Extracción de Datos', {
            'fields': ('tecnico_responsable', 'extraido_exitosamente', 'error_extraccion', 'fecha_extraccion_datos'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'fecha_documento'
    
    def get_tipo_documento(self, obj):
        return obj.get_tipo_documento_display()
    get_tipo_documento.short_description = 'Tipo'


class AlertaServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'valvula', 'tipo_alerta', 'fecha_alerta', 'resuelta')
    list_filter = ('tipo_alerta', 'resuelta', 'fecha_alerta', 'valvula__empresa')
    search_fields = ('valvula__numero_serie', 'descripcion')
    readonly_fields = ('fecha_alerta', 'fecha_resolucion')
    fieldsets = (
        ('Alerta', {
            'fields': ('valvula', 'tipo_alerta')
        }),
        ('Descripción', {
            'fields': ('descripcion',)
        }),
        ('Estado', {
            'fields': ('resuelta', 'fecha_resolucion')
        }),
        ('Auditoría', {
            'fields': ('fecha_alerta',),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'fecha_alerta'
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Certificado, CertificadoAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(AlertaServicio, AlertaServicioAdmin)
