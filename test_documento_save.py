#!/usr/bin/env python
"""
Script de prueba para verificar que los documentos se guardan correctamente en la BD
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, str(Path(__file__).parent))

django.setup()

from django.core.files.base import ContentFile
from servicios.models import Documento, Servicio
from usuarios.models import User, PerfilUsuario
from django.utils import timezone
import logging

logger = logging.getLogger('servicios')

def test_documento_save():
    """Prueba si podemos guardar un documento en la base de datos"""
    
    print("\n" + "="*60)
    print("PRUEBA: Guardado de documento en base de datos")
    print("="*60 + "\n")
    
    try:
        # 1. Obtener o crear usuario
        print("[1/5] Buscando usuario de comercial...")
        usuario = User.objects.filter(groups__name='comercial').first()
        if not usuario:
            print("  ⚠️  No hay usuarios comerciales. Usando admin.")
            usuario = User.objects.filter(is_superuser=True).first()
        
        if not usuario:
            print("  ❌ No hay usuarios en la base de datos.")
            return False
        
        print(f"  ✓ Usuario: {usuario.username}")
        
        # 2. Crear o obtener servicio
        print("\n[2/5] Buscando servicio...")
        servicio = Servicio.objects.first()
        print(f"  ✓ Servicio: {servicio.numero_servicio if servicio else 'No asignado'}")
        
        # 3. Crear documento de prueba
        print("\n[3/5] Creando objeto Documento...")
        documento = Documento(
            usuario_comercial=usuario,
            servicio=servicio,
            tipo_documento='calibracion',
            nombre_original='test_documento.pdf',
            numero_documento='TEST-001',
            presion_inicial='100',
            presion_final='105',
            temperatura='20',
            laboratorio='Lab Test',
            tecnico_responsable='Juan Pérez',
            extraido_exitosamente=True,
            fecha_extraccion_datos=timezone.now(),
        )
        
        # Crear archivo PDF de prueba
        pdf_content = b'%PDF-1.4\n%Test PDF\nendstream'
        documento.archivo_pdf = ContentFile(pdf_content, name='test_documento.pdf')
        
        print("  ✓ Objeto creado")
        
        # 4. Guardar documento
        print("\n[4/5] Guardando documento...")
        try:
            documento.save()
            documento_id = documento.id
            print(f"  ✓ Documento guardado con ID: {documento_id}")
            logger.info(f"Documento guardado exitosamente: ID={documento_id}")
        except Exception as e:
            print(f"  ❌ Error al guardar: {str(e)}")
            logger.error(f"Error al guardar documento: {str(e)}", exc_info=True)
            return False
        
        # 5. Verificar que está en la BD
        print("\n[5/5] Verificando en base de datos...")
        documento_verificado = Documento.objects.filter(id=documento_id).first()
        
        if documento_verificado:
            print(f"  ✓ Documento encontrado en BD: {documento_verificado.numero_documento}")
            print(f"    - Tipo: {documento_verificado.get_tipo_documento_display()}")
            print(f"    - Usuario: {documento_verificado.usuario_comercial.username}")
            print(f"    - Archivo: {documento_verificado.archivo_pdf.name if documento_verificado.archivo_pdf else 'No guardado'}")
            print(f"    - Creado: {documento_verificado.fecha_creacion}")
            print("\n✅ PRUEBA EXITOSA: Documento se guarda correctamente en BD")
            logger.info("✅ PRUEBA EXITOSA: Documento se guarda correctamente en BD")
            return True
        else:
            print(f"  ❌ Documento NO encontrado en BD con ID {documento_id}")
            logger.error(f"Documento NO encontrado en BD después de guardar (ID={documento_id})")
            
            # Intentar listar todos los documentos
            print("\n  Documentos en BD:")
            for doc in Documento.objects.all().order_by('-fecha_creacion')[:5]:
                print(f"    - ID {doc.id}: {doc.numero_documento} ({doc.fecha_creacion})")
            
            return False
            
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {str(e)}")
        logger.error(f"Error durante prueba: {str(e)}", exc_info=True)
        return False

if __name__ == '__main__':
    success = test_documento_save()
    sys.exit(0 if success else 1)
