from django.contrib import admin
from config.admin import admin_site
from .models import PerfilUsuario, LogActividad


class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'empresa', 'activo', 'fecha_creacion')
    list_filter = ('rol', 'activo', 'fecha_creacion')
    search_fields = ('usuario__username', 'usuario__email', 'usuario__first_name')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('usuario', 'rol')
        }),
        ('Empresa', {
            'fields': ('empresa',)
        }),
        ('Zona Horaria', {
            'fields': ('zona_horaria',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


class LogActividadAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'fecha', 'direccion_ip')
    list_filter = ('fecha', 'usuario')
    search_fields = ('usuario__username', 'accion')
    readonly_fields = ('fecha', 'usuario', 'accion', 'descripcion', 'direccion_ip')
    date_hierarchy = 'fecha'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


admin_site.register(PerfilUsuario, PerfilUsuarioAdmin)
admin_site.register(LogActividad, LogActividadAdmin)
