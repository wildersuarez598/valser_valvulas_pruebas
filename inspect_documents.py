#!/usr/bin/env python
"""
Test completo del upload en la BD con verificación de datos
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from servicios.models import Documento
from django.contrib.auth.models import User

print("\n" + "="*80)
print("INSPECT: Documentos en la base de datos")
print("="*80 + "\n")

# Contar documentos
total = Documento.objects.count()
print(f"Total de documentos: {total}")

if total > 0:
    # Mostrar últimos 5 documentos
    documentos = Documento.objects.all().order_by('-fecha_creacion')[:5]
    
    for doc in documentos:
        print(f"\n[ID: {doc.id}] {doc.numero_documento or '(Sin número)'}")
        print(f"  - Tipo: {doc.get_tipo_documento_display()}")
        print(f"  - Usuario: {doc.usuario_comercial.username if doc.usuario_comercial else '(Anónimo)'}")
        print(f"  - Archivo: {doc.archivo_pdf.name if doc.archivo_pdf else '(Sin archivo)'}")
        print(f"  - Tamaño: {doc.archivo_pdf.size if doc.archivo_pdf else 0} bytes")
        print(f"  - Extraído: {doc.extraido_exitosamente}")
        print(f"  - Creado: {doc.fecha_creacion}")
        print(f"  - Presión Inicial: {doc.presion_inicial}")
        print(f"  - Laboratorio: {doc.laboratorio}")
else:
    print("No hay documentos en la base de datos")

print("\n" + "="*80)
