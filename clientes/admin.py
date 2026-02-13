from django.contrib import admin
from config.admin import admin_site
from .models import Empresa, Contacto


class ContactoInline(admin.TabularInline):
    model = Contacto
    extra = 1
    fields = ('nombre', 'cargo', 'email', 'telefono', 'tipo_contacto', 'activo')


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'ciudad', 'activa', 'cantidad_valvulas')
    list_filter = ('activa', 'ciudad', 'fecha_registro')
    search_fields = ('nombre', 'nit', 'email')
    readonly_fields = ('fecha_registro', 'fecha_actualizacion', 'cantidad_valvulas')
    inlines = [ContactoInline]
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'nit', 'logo')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'contacto_principal', 'cargo_contacto')
        }),
        ('Ubicación', {
            'fields': ('direccion', 'ciudad', 'departamento', 'codigo_postal')
        }),
        ('Estado', {
            'fields': ('activa', 'cantidad_valvulas')
        }),
        ('Auditoría', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa', 'cargo', 'email', 'tipo_contacto', 'activo')
    list_filter = ('tipo_contacto', 'activo', 'empresa')
    search_fields = ('nombre', 'email', 'empresa__nombre')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'cargo', 'tipo_contacto')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono')
        }),
        ('Empresa', {
            'fields': ('empresa',)
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_creacion')
        }),
    )


admin_site.register(Empresa, EmpresaAdmin)
admin_site.register(Contacto, ContactoAdmin)
