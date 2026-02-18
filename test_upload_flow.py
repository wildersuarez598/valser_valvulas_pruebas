#!/usr/bin/env python
"""
Test exhaustivo del flujo completo de upload de certificados
Simula exactamente lo que hace la vista upload_certificado
"""
import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, str(Path(__file__).parent))
django.setup()

from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from servicios.models import Documento, Servicio
from servicios.extractors import detect_document_type
from django.utils import timezone
import logging

logger = logging.getLogger('servicios')

# Crear PDF de prueba más realista
PDF_CONTENT = b"""%PDF-1.4
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
<< /Length 200 >>
stream
BT
/F1 12 Tf
50 750 Td
(Certificado de Calibracion) Tj
0 -20 Td
(Numero: CERT-2026-001) Tj
0 -20 Td
(Serie: SN-12345-A) Tj
0 -20 Td
(Modelo: MOD-XYZ) Tj
0 -20 Td
(Presion inicial: 100 PSI) Tj
0 -20 Td
(Presion final: 105 PSI) Tj
0 -20 Td
(Temperatura: 20C) Tj
0 -20 Td
(Fecha: 2026-02-16) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000234 00000 n
0000000333 00000 n
trailer
<< /Size 6 /Root 1 0 R >>
startxref
583
%%EOF
"""

def test_upload_flow():
    """Prueba el flujo completo de upload"""
    
    print("\n" + "="*80)
    print("TEST: Flujo Completo de Upload de Certificado")
    print("="*80)
    
    try:
        # 1. Obtener usuario
        print("\n[1/6] Obteniendo usuario comercial...")
        usuario = User.objects.filter(is_staff=False).first()
        if not usuario:
            usuario = User.objects.filter(is_superuser=True).first()
        print(f"  ✓ Usuario: {usuario.username}")
        
        # 2. Crear archivo PDF en memoria
        print("\n[2/6] Creando archivo PDF en memoria...")
        pdf_file = ContentFile(PDF_CONTENT, name='test_cert.pdf')
        print(f"  ✓ Archivo creado: {pdf_file.name} ({len(PDF_CONTENT)} bytes)")
        print(f"  ✓ Posición inicial: {pdf_file.tell()}")
        
        # 3. Detectar tipo de documento (esto lee el archivo)
        print("\n[3/6] Detectando tipo de documento...")
        print(f"  - Posición antes: {pdf_file.tell()}")
        
        try:
            doc_type, extractor = detect_document_type(pdf_file)
            print(f"  ✓ Tipo detectado: {doc_type}")
            print(f"  - Posición después de detect: {pdf_file.tell()}")
            
            extracted_data = extractor.extract()
            print(f"  ✓ Datos extraídos:")
            print(f"    - numero_documento: {extracted_data.get('numero_documento')}")
            print(f"    - numero_serie: {extracted_data.get('numero_serie')}")
            print(f"    - presion_inicial: {extracted_data.get('presion_inicial')}")
            print(f"  - Posición después de extract: {pdf_file.tell()}")
        except Exception as e:
            print(f"  ❌ Error en detección: {str(e)}")
            return False
        
        # 4. Crear objeto Documento (sin guardar)
        print("\n[4/6] Creando objeto Documento...")
        documento = Documento(
            usuario_comercial=usuario,
            tipo_documento=doc_type,
            archivo_pdf=pdf_file,  # Asignar exactamente como en la vista
            nombre_original=pdf_file.name,
            numero_documento=extracted_data.get('numero_documento', ''),
            presion_inicial=extracted_data.get('presion_inicial'),
            presion_final=extracted_data.get('presion_final'),
            temperatura=extracted_data.get('temperatura'),
            extraido_exitosamente=True,
            fecha_extraccion_datos=timezone.now(),
        )
        
        print(f"  ✓ Objecto creado")
        print(f"  - archivo_pdf.name: {documento.archivo_pdf.name}")
        print(f"  - archivo_pdf.size: {documento.archivo_pdf.size}")
        print(f"  - Posición del archivo: {pdf_file.tell()}")
        
        # 5. Guardar documento
        print("\n[5/6] Guardando documento en BD...")
        try:
            documento.save()
            doc_id = documento.id
            print(f"  ✓ Documento guardado con ID: {doc_id}")
            print(f"  - archivo_pdf.name: {documento.archivo_pdf.name}")
            print(f"  - archivo_pdf.url: {documento.archivo_pdf.url}")
            print(f"  - archivo_pdf.size: {documento.archivo_pdf.size}")
        except Exception as e:
            print(f"  ❌ Error al guardar: {str(e)}")
            logger.error(f"Error guardando documento: {str(e)}", exc_info=True)
            return False
        
        # 6. Verificar en BD
        print("\n[6/6] Verificando en base de datos...")
        doc_verificado = Documento.objects.get(id=doc_id)
        
        print(f"  ✓ Documento encontrado en BD")
        print(f"    - ID: {doc_verificado.id}")
        print(f"    - número: {doc_verificado.numero_documento}")
        print(f"    - tipo: {doc_verificado.get_tipo_documento_display()}")
        print(f"    - archivo: {doc_verificado.archivo_pdf.name}")
        print(f"    - archivo.size: {doc_verificado.archivo_pdf.size}")
        # 6.b linkear la válvula (simulando vista)
        numero_serie = extracted_data.get('numero_serie')
        modelo = extracted_data.get('modelo')
        print(f"    - serie extraída: {numero_serie}, modelo extraído: {modelo}")
        if numero_serie or modelo:
            val, creada = doc_verificado.enlazar_valvula_por_numero_serie(numero_serie, modelo=modelo)
            print(f"    - Válvula enlazada: {val}, creada={creada}")
            assert val is not None
            assert val.modelo == (modelo or val.modelo)
            print(f"    - Válvula en BD: S/N {val.numero_serie}, modelo {val.modelo}")
        
        # Verificar que el archivo existe en el sistema de archivos
        if doc_verificado.archivo_pdf:
            file_path = doc_verificado.archivo_pdf.path
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"  ✓ Archivo existe en disk: {file_path}")
                print(f"    - Tamaño: {file_size} bytes")
                
                if file_size == 0:
                    print(f"  ⚠️  WARNING: Archivo está VACÍO (0 bytes)")
                    return False
                else:
                    print(f"  ✓ Archivo tiene contenido")
            else:
                print(f"  ❌ Archivo NO existe en disk: {file_path}")
                return False
        
        print("\n" + "="*80)
        print("✅ PRUEBA EXITOSA: Flujo completo de upload funciona correctamente")
        print("="*80)
        return True
        
    except Exception as e:
        print(f"\n❌ Error general: {str(e)}")
        logger.error(f"Error en test: {str(e)}", exc_info=True)
        return False

if __name__ == '__main__':
    success = test_upload_flow()
    sys.exit(0 if success else 1)
