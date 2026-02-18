from django.urls import path
from . import views

app_name = 'servicios'

urlpatterns = [
    # Nota: la ruta "certificados/" sigue existiendo para compatibilidad
    # pero ahora muestra un listado de válvulas (hoja de vida) en lugar de
    # los documentos individuales.
    path('certificados/', views.certificado_list, name='certificado_list'),
    path('certificados/<int:pk>/', views.certificado_detail, name='certificado_detail'),
    path('certificados/subir/', views.upload_certificado, name='upload_certificado'),
    path('certificados/<int:pk>/eliminar/', views.eliminar_certificado, name='eliminar_certificado'),

    # Eliminar válvula (se utilizará desde el listado de válvulas)
    path('valvulas/<int:pk>/eliminar/', views.eliminar_valvula, name='eliminar_valvula'),
]
