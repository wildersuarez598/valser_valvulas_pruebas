#!/usr/bin/env python
"""
Script de prueba para verificar que los documentos se guardan correctamente en la BD
y que el flujo de extracción de PDF no interfiere con el guardado del archivo
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
from servicios.extractors import detect_document_type
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
            print("  INFO: No hay usuarios comerciales. Usando admin.")
            usuario = User.objects.filter(is_superuser=True).first()
        
        if not usuario:
            print("  ERROR: No hay usuarios en la base de datos.")
            return False
        
        print(f"  OK: Usuario: {usuario.username}")
        
        # 2. Crear o obtener servicio
        print("\n[2/5] Buscando servicio...")
        servicio = Servicio.objects.first()
        print(f"  OK: Servicio: {servicio.numero_servicio if servicio else 'No asignado'}")
        
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
        
        print("  OK: Objeto creado")
        
        # 4. Guardar documento
        print("\n[4/5] Guardando documento...")
        try:
            documento.save()
            documento_id = documento.id
            print(f"  OK: Documento guardado con ID: {documento_id}")
            logger.info(f"Documento guardado exitosamente: ID={documento_id}")
        except Exception as e:
            print(f"  ERROR: No se pudo guardar: {str(e)}")
            logger.error(f"Error al guardar documento: {str(e)}", exc_info=True)
            return False
        
        # 5. Verificar que está en la BD
        print("\n[5/5] Verificando en base de datos...")
        documento_verificado = Documento.objects.filter(id=documento_id).first()
        
        if documento_verificado:
            print(f"  OK: Documento encontrado en BD: {documento_verificado.numero_documento}")
            print(f"    - Tipo: {documento_verificado.get_tipo_documento_display()}")
            print(f"    - Usuario: {documento_verificado.usuario_comercial.username}")
            print(f"    - Archivo: {documento_verificado.archivo_pdf.name if documento_verificado.archivo_pdf else 'No guardado'}")
            print(f"    - Creado: {documento_verificado.fecha_creacion}")
            print("\nSUCESO: Documento se guarda correctamente en BD")
            logger.info("SUCESO: Documento se guarda correctamente en BD")
            return True
        else:
            print(f"  ERROR: Documento NO encontrado en BD con ID {documento_id}")
            logger.error(f"Documento NO encontrado en BD después de guardar (ID={documento_id})")
            
            # Intentar listar todos los documentos
            print("\n  Documentos en BD:")
            for doc in Documento.objects.all().order_by('-fecha_creacion')[:5]:
                print(f"    - ID {doc.id}: {doc.numero_documento} ({doc.fecha_creacion})")
            
            return False
            
    except Exception as e:
        print(f"\nERROR durante la prueba: {str(e)}")
        logger.error(f"Error durante prueba: {str(e)}", exc_info=True)
        return False


def test_extractor_seek_position():
    """
    Prueba crítica: Verifica que el extractor resetea la posición del archivo
    para que el guardado posterior funcione correctamente
    """
    print("\n" + "="*80)
    print("PRUEBA CRÍTICA: Verificar reseteo de posición de archivo en extractor")
    print("="*80 + "\n")
    
    try:
        from servicios.extractors import CertificadoCalibracionExtractor
        
        # Crear un PDF de prueba con contenido calibración
        pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>
endobj
4 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
5 0 obj
<< /Length 100 >>
stream
BT
/F1 12 Tf
100 700 Td
(Certificado de Calibracion) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000253 00000 n
0000000338 00000 n
trailer
<< /Size 6 /Root 1 0 R >>
startxref
487
%%EOF
"""
        
        print("[TEST] Creando archivo PDF en memoria...")
        from django.core.files.base import ContentFile
        pdf_file = ContentFile(pdf_content, name='test_calibration.pdf')
        
        print("[TEST] Posición inicial del archivo:", pdf_file.tell())
        print("[TEST] Tamaño del archivo:", len(pdf_content), "bytes")
        
        print("\n[TEST] Extrayendo contenido del PDF...")
        try:
            extractor = CertificadoCalibracionExtractor(pdf_file)
            print("[TEST] Extractor creado exitosamente")
            print("[TEST] Texto extraído (primeros 100 caracteres):", extractor.full_text[:100])
        except Exception as e:
            print(f"[INFO] No se pudo extraer (esperado para PDF minimal): {str(e)}")
        
        print("\n[TEST] Verificando posición del archivo después de extracción:")
        print("[TEST] Posición actual del archivo:", pdf_file.tell())
        print("[TEST] Debería estar en 0 después de seek(0)")
        
        if pdf_file.tell() == 0:
            print("\nSUCESO: Posición de archivo fue resetada correctamente")
            print("El archivo ahora se puede guardar sin problemas")
            return True
        else:
            print(f"\nFALLA: Posición de archivo NO fue resetada. Está en {pdf_file.tell()}")
            print("Esto evitaría que el archivo se guardara correctamente")
            return False
        
    except Exception as e:
        print(f"\nERROR en prueba de seek: {str(e)}")
        logger.error(f"Error en prueba seek: {str(e)}", exc_info=True)
        return False


if __name__ == '__main__':
    # Ejecutar ambas pruebas
    test1_ok = test_documento_save()
    test2_ok = test_extractor_seek_position()
    
    print("\n" + "="*80)
    if test1_ok and test2_ok:
        print("TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("="*80)
        sys.exit(0)
    else:
        print("ALGUNAS PRUEBAS FALLARON")
        print("="*80)
        sys.exit(1)
