"""
URLs de la aplicación de usuarios
"""
from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cliente/dashboard/', views.cliente_dashboard, name='cliente_dashboard'),
    path('comercial/dashboard/', views.comercial_dashboard, name='comercial_dashboard'),
    path('cambiar_zona_horaria/', views.cambiar_zona_horaria, name='cambiar_zona_horaria'),
    path('acceso_denegado/', views.acceso_denegado, name='acceso_denegado'),
]
