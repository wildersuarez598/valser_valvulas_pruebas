from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
import logging

from usuarios.decorators import requiere_comercial
from servicios.models import Certificado, Documento, Servicio
from servicios.forms import CertificadoForm, DocumentoForm
from servicios.extractors import extract_data, detect_document_type

logger = logging.getLogger(__name__)


def _parse_date(date_str):
    """
    Intenta parsear una cadena de fecha a objeto date.
    Soporta formatos comunes: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD, etc.
    
    Args:
        date_str: String con la fecha a parsear
        
    Returns:
        datetime.date object o None si no se puede parsear
    """
    if not date_str or not isinstance(date_str, str):
        return None
    
    # Limpiar espacios
    date_str = date_str.strip()
    
    # Formatos comunes a intentar (en orden de probabilidad)
    formats = [
        '%d/%m/%Y',      # 03/06/2025
        '%d-%m-%Y',      # 03-06-2025
        '%d.%m.%Y',      # 03.06.2025
        '%Y-%m-%d',      # 2025-06-03
        '%d/%m/%y',      # 03/06/25
        '%d-%m-%y',      # 03-06-25
        '%d %m %Y',      # 03 06 2025
        '%m/%d/%Y',      # 06/03/2025 (formato US)
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except (ValueError, TypeError):
            continue
    
    # Si no se puede parsear, registrar advertencia
    logger.warning(f'No se pudo parsear fecha: "{date_str}". Se ignorará.')
    return None


def extract_pdf_data(pdf_file):
    """
    DEPRECATED: Usar extractors.extract_data() en su lugar
    Manttenido para compatibilidad hacia atrás
    """
    return extract_data(pdf_file)


@requiere_comercial
def upload_certificado(request):
    """
    Vista para que comerciales suban documentos (Certificados, Informes, etc)
    Detección automática del tipo y extracción de datos
    """
    if request.method == 'POST':
        if 'archivo_pdf' not in request.FILES:
            messages.error(request, 'Por favor selecciona un archivo PDF')
            return redirect('servicios:upload_certificado')
        
        pdf_file = request.FILES['archivo_pdf']
        servicio_id = request.POST.get('servicio_id')
        servicio = None
        
        # Obtener el servicio si se proporciona
        if servicio_id:
            try:
                servicio = Servicio.objects.get(id=servicio_id, usuario_comercial=request.user)
            except Servicio.DoesNotExist:
                messages.error(request, 'Servicio no encontrado o no tienes permisos.')
                return redirect('servicios:certificado_list')
        
        try:
            # Detectar tipo de documento y extraer datos
            doc_type, extractor = detect_document_type(pdf_file)
            logger.info(f'Tipo detectado: {doc_type}')
            
            extracted_data = extractor.extract()
            logger.info(f'Datos extraídos: numero_documento={extracted_data.get("numero_documento")}, numero_serie={extracted_data.get("numero_serie")}')
            
            # Crear documento con los datos extraídos
            documento = Documento(
                servicio=servicio,
                usuario_comercial=request.user,
                tipo_documento=doc_type,
                archivo_pdf=pdf_file,
                nombre_original=pdf_file.name,
                numero_documento=extracted_data.get('numero_documento', ''),
                tecnico_responsable=extracted_data.get('tecnico_responsable', ''),
                extraido_exitosamente=True,
                fecha_extraccion_datos=timezone.now(),
            )
            
            # Llenar campos según tipo de documento
            if doc_type == 'calibracion':
                documento.fecha_documento = _parse_date(extracted_data.get('fecha_emision')) or timezone.now().date()
                documento.fecha_vencimiento = _parse_date(extracted_data.get('fecha_vencimiento'))
                documento.presion_inicial = extracted_data.get('presion_inicial') or None
                documento.presion_final = extracted_data.get('presion_final') or None
                documento.temperatura = extracted_data.get('temperatura') or None
                documento.resultado_calibracion = extracted_data.get('resultado') or None
                documento.laboratorio = extracted_data.get('laboratorio') or None
                documento.unidad_presion = extracted_data.get('unidad_presion') or None
            
            elif doc_type == 'mantenimiento':
                documento.fecha_documento = _parse_date(extracted_data.get('fecha_emision')) or timezone.now().date()
                documento.tipo_mantenimiento = extracted_data.get('tipo_mantenimiento') or None
                documento.descripcion_trabajos = extracted_data.get('descripcion_trabajos') or None
                documento.estado_valvula = extracted_data.get('estado_valvula') or None
                documento.materiales_utilizados = extracted_data.get('materiales_utilizados') or None
                documento.proximo_mantenimiento = _parse_date(extracted_data.get('proximo_mantenimiento'))
                documento.duracion_horas = extracted_data.get('duracion_horas') or None
            
            # Guardar el documento inicial
            documento.save()
            documento_id = documento.id
            logger.info(f'Documento guardado exitosamente: ID={documento_id}, Tipo={doc_type}')
            
            # Auto-identificar válvula por número de serie y actualizar hoja de vida
            numero_serie = extracted_data.get('numero_serie') or extracted_data.get('serial_number')
            if numero_serie:
                try:
                    valvula, fue_creada = documento.enlazar_valvula_por_numero_serie(numero_serie)
                    documento.save()  # Guardar la relación valvula
                    logger.info(f'Válvula enlazada: {numero_serie}, Creada={fue_creada}')
                    
                    # Actualizar fechas en la hoja de vida de la válvula
                    documento.actualizar_fechas_hoja_vida()
                    logger.info(f'Hoja de vida actualizada para válvula {numero_serie}')
                    
                    if fue_creada:
                        logger.info(f'Nueva válvula creada automáticamente: S/N {numero_serie}')
                    else:
                        logger.info(f'Válvula identificada: {valvula.marca} {valvula.modelo} (S/N {numero_serie})')
                except Exception as e:
                    logger.warning(f'Error al enlazar válvula: {str(e)}', exc_info=True)
                    # No interrumpir el flujo si hay error en auto-identificación
            
            tipo_display = documento.get_tipo_documento_display()
            numero_doc = documento.numero_documento or '(sin número)'
            messages.success(
                request,
                f'{tipo_display} "{numero_doc}" subido y procesado exitosamente'
            )
            return redirect('servicios:certificado_list')
        
        except Exception as e:
            # Mejorar mensaje de error para problemas de extracción/validación
            error_msg = str(e)
            
            # Detectar errores de validación de fecha
            if 'formato de fecha' in error_msg.lower() or 'dateformat' in error_msg.lower():
                mensaje_error = (
                    'Error al procesar fechas en el documento. '
                    'Asegúrate de que el PDF contenga fechas válidas en formato DD-MM-YYYY. '
                    'Puedes editar manualmente las fechas después de la carga.'
                )
            else:
                mensaje_error = f'Error al procesar el documento: {error_msg}'
            
            logger.error(f'Error en upload_certificado: {error_msg}', exc_info=True)
            messages.error(request, mensaje_error)
    
    # GET request - mostrar formulario
    servicios = Servicio.objects.none()
    if hasattr(request.user, 'perfil'):
        if request.user.perfil.rol == 'admin':
            servicios = Servicio.objects.all()
        else:
            # Filtrar servicios del comercial actual
            servicios = Servicio.objects.filter(tecnico__usuario=request.user)
    
    context = {
        'titulo': 'Subir Documento',
        'descripcion': 'Sube un certificado de calibración o informe de mantenimiento para extracción automática de datos',
        'servicios': servicios,
    }
    return render(request, 'servicios/upload_certificado.html', context)


@login_required
def certificado_list(request):
    """
    Lista de documentos subidos
    """
    if hasattr(request.user, 'perfil') and request.user.perfil.rol == 'comercial':
        certificados = Documento.objects.filter(usuario_comercial=request.user).order_by('-fecha_creacion')
    else:
        certificados = Documento.objects.all().order_by('-fecha_creacion')
    
    # Estadísticas
    total = certificados.count()
    extraidos = certificados.filter(extraido_exitosamente=True).count()
    errores = certificados.filter(extraido_exitosamente=False).count()
    
    context = {
        'certificados': certificados,
        'total': total,
        'extraidos': extraidos,
        'errores': errores,
        'titulo': 'Documentos Subidos',
        'descripcion': 'Lista de certificados, informes y otros documentos'
    }
    return render(request, 'servicios/lista_certificados.html', context)


@login_required
def certificado_detail(request, pk):
    """
    Detalles de un documento
    """
    documento = get_object_or_404(Documento, pk=pk)
    
    # Verificar permisos
    if hasattr(request.user, 'perfil') and request.user.perfil.rol == 'comercial':
        if documento.usuario_comercial != request.user:
            return redirect('servicios:certificado_list')
    
    context = {
        'documento': documento,
        'titulo': f'{documento.get_tipo_documento_display()} {documento.numero_documento}',
    }
    return render(request, 'servicios/detalle_certificado.html', context)


@requiere_comercial
@require_http_methods(["POST"])
def eliminar_certificado(request, pk):
    """
    Elimina un documento
    """
    documento = get_object_or_404(Documento, pk=pk)
    
    # Verificar permisos
    if documento.usuario_comercial != request.user:
        messages.error(request, 'No tienes permiso para eliminar este documento')
        return redirect('servicios:certificado_list')
    
    numero = documento.numero_documento or 'sin número'
    documento.delete()
    messages.success(request, f'Documento "{numero}" eliminado correctamente')
    
    return redirect('servicios:certificado_list')

