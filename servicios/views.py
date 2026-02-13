from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from datetime import datetime
import pdfplumber
import re

from usuarios.decorators import requiere_comercial
from servicios.models import Certificado, Servicio
from servicios.forms import CertificadoForm, ServicioConCertificadoForm


def extract_pdf_data(pdf_file):
    """
    Extrae datos de un PDF de certificado
    Busca patrones comunes en certificados de calibración
    
    Retorna un diccionario con los datos extraídos
    """
    try:
        data = {
            'numero_certificado': None,
            'fecha_emision': None,
            'fecha_vencimiento': None,
            'presion_inicial': None,
            'presion_final': None,
            'temperatura': None,
            'resultado': None,
            'laboratorio': None,
            'tecnico_responsable': None,
        }
        
        with pdfplumber.open(pdf_file) as pdf:
            # Extraer texto de todas las páginas
            full_text = ''
            for page in pdf.pages:
                full_text += page.extract_text() + '\n'
            
            # Buscar patrones
            # Número de certificado
            cert_pattern = r'(?:CERT|Certificado|certificado)[\s:]*([A-Z0-9\-\/]+)'
            cert_match = re.search(cert_pattern, full_text)
            if cert_match:
                data['numero_certificado'] = cert_match.group(1).strip()
            
            # Fecha de emisión
            date_pattern = r'(?:Fecha|fecha|DATE|Emisión|emisión)[\s:]*(\d{1,2}[\s\-\/]\d{1,2}[\s\-\/]\d{2,4})'
            date_match = re.search(date_pattern, full_text)
            if date_match:
                data['fecha_emision'] = date_match.group(1).strip()
            
            # Presión inicial
            presion_inicial_pattern = r'(?:Presión inicial|presión inicial|Pressure initial|Initial Pressure)[\s:]*([0-9.]+)\s*(?:PSI|bar|atm|kPa)?'
            presion_match = re.search(presion_inicial_pattern, full_text, re.IGNORECASE)
            if presion_match:
                data['presion_inicial'] = presion_match.group(1).strip()
            
            # Presión final
            presion_final_pattern = r'(?:Presión final|presión final|Pressure final|Final Pressure)[\s:]*([0-9.]+)\s*(?:PSI|bar|atm|kPa)?'
            presion_final_match = re.search(presion_final_pattern, full_text, re.IGNORECASE)
            if presion_final_match:
                data['presion_final'] = presion_final_match.group(1).strip()
            
            # Temperatura
            temp_pattern = r'(?:Temperatura|temperatura|Temperature)[\s:]*([0-9.]+)\s*(?:°C|C|F|°F)?'
            temp_match = re.search(temp_pattern, full_text, re.IGNORECASE)
            if temp_match:
                data['temperatura'] = temp_match.group(1).strip()
            
            # Resultado (APROBADO/RECHAZADO)
            if 'aprobado' in full_text.lower():
                data['resultado'] = 'APROBADO'
            elif 'rechazado' in full_text.lower():
                data['resultado'] = 'RECHAZADO'
            elif 'passed' in full_text.lower():
                data['resultado'] = 'PASSED'
            elif 'failed' in full_text.lower():
                data['resultado'] = 'FAILED'
            
            # Laboratorio
            lab_pattern = r'(?:Laboratorio|laboratorio|Laboratory|LABORATORY)[\s:]*([^\n]+)'
            lab_match = re.search(lab_pattern, full_text)
            if lab_match:
                data['laboratorio'] = lab_match.group(1).strip()
            
            # Técnico responsable
            tech_pattern = r'(?:Técnico|técnico|Technician|technician|Responsable|responsable)[\s:]*([^\n]+)'
            tech_match = re.search(tech_pattern, full_text)
            if tech_match:
                data['tecnico_responsable'] = tech_match.group(1).strip()
        
        return data
    
    except Exception as e:
        return {'error': str(e)}


@requiere_comercial
def upload_certificado(request):
    """
    Vista para que comerciales suban certificados PDF
    Extrae automáticamente los datos del PDF
    """
    if request.method == 'POST':
        form = CertificadoForm(request.POST, request.FILES)
        if form.is_valid():
            certificado = form.save(commit=False)
            
            # Extraer datos del PDF si se subió
            if 'archivo_pdf' in request.FILES:
                pdf_file = request.FILES['archivo_pdf']
                extracted_data = extract_pdf_data(pdf_file)
                
                # Actualizar campos extraídos si están vacíos
                if extracted_data.get('numero_certificado') and not certificado.numero_certificado:
                    certificado.numero_certificado = extracted_data['numero_certificado']
                if extracted_data.get('presion_inicial') and not certificado.presion_inicial:
                    certificado.presion_inicial = extracted_data['presion_inicial']
                if extracted_data.get('presion_final') and not certificado.presion_final:
                    certificado.presion_final = extracted_data['presion_final']
                if extracted_data.get('temperatura') and not certificado.temperatura:
                    certificado.temperatura = extracted_data['temperatura']
                if extracted_data.get('resultado') and not certificado.resultado:
                    certificado.resultado = extracted_data['resultado']
                if extracted_data.get('laboratorio') and not certificado.laboratorio:
                    certificado.laboratorio = extracted_data['laboratorio']
                if extracted_data.get('tecnico_responsable') and not certificado.tecnico_responsable:
                    certificado.tecnico_responsable = extracted_data['tecnico_responsable']
                
                certificado.extraido_exitosamente = True
                certificado.fecha_extraccion_datos = datetime.now()
            
            certificado.usuario_comercial = request.user
            certificado.save()
            
            messages.success(request, f'Certificado "{certificado.numero_certificado}" subido exitosamente')
            return redirect('certificado_list')
    else:
        form = CertificadoForm()
    
    context = {
        'form': form,
        'titulo': 'Subir Certificado',
        'descripcion': 'Sube un certificado PDF para extraer automáticamente sus datos'
    }
    return render(request, 'servicios/upload_certificado.html', context)


@login_required
def certificado_list(request):
    """
    Lista de certificados subidos por el usuario comercial
    """
    if hasattr(request.user, 'perfil') and request.user.perfil.rol == 'comercial':
        certificados = Certificado.objects.filter(usuario_comercial=request.user)
    else:
        certificados = Certificado.objects.all()
    
    context = {
        'certificados': certificados,
        'titulo': 'Mis Certificados',
        'descripcion': 'Lista de certificados subidos'
    }
    return render(request, 'servicios/lista_certificados.html', context)


@login_required
def certificado_detail(request, pk):
    """
    Detalles de un certificado específico
    """
    certificado = get_object_or_404(Certificado, pk=pk)
    
    # Verificar permisos
    if hasattr(request.user, 'perfil') and request.user.perfil.rol == 'comercial':
        if certificado.usuario_comercial != request.user:
            return redirect('certificado_list')
    
    context = {
        'certificado': certificado,
        'titulo': f'Certificado {certificado.numero_certificado}',
    }
    return render(request, 'servicios/detalle_certificado.html', context)


@requiere_comercial
@require_http_methods(["POST"])
def eliminar_certificado(request, pk):
    """
    Elimina un certificado (solo el comercial que lo subió o admin)
    """
    certificado = get_object_or_404(Certificado, pk=pk)
    
    # Verificar permisos
    if certificado.usuario_comercial != request.user:
        messages.error(request, 'No tienes permiso para eliminar este certificado')
        return redirect('certificado_list')
    
    numero = certificado.numero_certificado
    certificado.delete()
    messages.success(request, f'Certificado "{numero}" eliminado correctamente')
    
    return redirect('certificado_list')
