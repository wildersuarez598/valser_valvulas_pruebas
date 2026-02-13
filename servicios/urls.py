from django.urls import path
from . import views

urlpatterns = [
    # URLs para certificados
    path('certificados/', views.certificado_list, name='certificado_list'),
    path('certificados/<int:pk>/', views.certificado_detail, name='certificado_detail'),
    path('certificados/subir/', views.upload_certificado, name='upload_certificado'),
    path('certificados/<int:pk>/eliminar/', views.eliminar_certificado, name='eliminar_certificado'),
]
