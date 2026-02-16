from django.urls import path
from . import views

app_name = 'valvulas'

urlpatterns = [
    # Hoja de vida de válvula
    path('<int:valvula_id>/hoja-vida/', views.hoja_vida_valvula, name='hoja_vida'),
    path('<int:valvula_id>/editar/', views.editar_hoja_vida, name='editar'),
    
    # Listado de válvulas
    path('', views.listar_valvulas, name='lista'),
    
    # Descargar documentos
    path('documento/<int:documento_id>/descargar/', views.descargar_documento, name='descargar_documento'),
]
