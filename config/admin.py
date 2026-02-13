"""
Configuración personalizada del sitio de administración de Django
Traductor al español y personalización de estilos
"""

from django.contrib import admin


class AdminSitePersonalizado(admin.AdminSite):
    """Sitio de admin personalizado con interfaz en español"""
    
    site_header = "Panel de Administración - Valser"
    site_title = "Valser Admin"
    index_title = "Gestión del Sistema"
    
    def each_context(self, request):
        context = super().each_context(request)
        context['site_header'] = self.site_header
        context['site_title'] = self.site_title
        context['index_title'] = self.index_title
        return context


# Crear instancia personalizada
admin_site = AdminSitePersonalizado(name='admin_personalizado')
