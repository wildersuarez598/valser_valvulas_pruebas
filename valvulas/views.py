from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import logging

from valvulas.models import Valvula
from servicios.models import Documento
from .forms import ValvulaEditarHojaVidaForm

logger = logging.getLogger(__name__)


@login_required
def hoja_vida_valvula(request, valvula_id):
    """
    Vista para mostrar la Hoja de Vida de una válvula
    Incluye: datos básicos, historial de servicios, documentos adjuntos
    """
    valvula = get_object_or_404(Valvula, id=valvula_id)
    
    # Verificar permisos (el usuario debe ser del mismo grupo empresarial)
    if hasattr(request.user, 'perfil'):
        if request.user.perfil.rol != 'admin' and request.user.perfil.empresa != valvula.empresa:
            messages.error(request, 'No tienes permiso para ver esta válvula')
            return redirect('/')
    
    # Obtener documentos (últimas calibraciones y mantenimientos)
    documentos = Documento.objects.filter(
        valvula=valvula,
        extraido_exitosamente=True
    ).order_by('-fecha_documento')
    
    ultima_calibracion = valvula.obtener_ultima_calibracion()
    ultimo_mantenimiento = valvula.obtener_ultimo_mantenimiento()
    
    context = {
        'valvula': valvula,
        'documentos': documentos[:10],  # Últimos 10 documentos
        'ultima_calibracion': ultima_calibracion,
        'ultimo_mantenimiento': ultimo_mantenimiento,
        'requiere_calibracion': valvula.requiere_calibracion,
        'requiere_mantenimiento': valvula.requiere_mantenimiento,
    }
    
    return render(request, 'valvulas/hoja_vida.html', context)


@login_required
def editar_hoja_vida(request, valvula_id):
    """
    Vista para editar los datos básicos de la Hoja de Vida
    El comercial puede cambiar: ubicación, TAG, observaciones, etc
    """
    valvula = get_object_or_404(Valvula, id=valvula_id)
    
    # Verificar permisos
    if hasattr(request.user, 'perfil'):
        if request.user.perfil.rol == 'cliente':
            messages.error(request, 'No tienes permiso para editar la válvula')
            return redirect('hoja_vida_valvula', valvula_id=valvula.id)
    
    if request.method == 'POST':
        form = ValvulaEditarHojaVidaForm(request.POST, instance=valvula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hoja de vida actualizada correctamente')
            return redirect('hoja_vida_valvula', valvula_id=valvula.id)
    else:
        form = ValvulaEditarHojaVidaForm(instance=valvula)
    
    context = {
        'valvula': valvula,
        'form': form,
        'titulo': f'Editar Hoja de Vida - {valvula.numero_serie}',
    }
    
    return render(request, 'valvulas/editar_hoja_vida.html', context)


@login_required
def listar_valvulas(request):
    """
    Lista todas las válvulas (con filtros por empresa y estado)
    """
    valvulas = Valvula.objects.all()
    
    # Filtro por empresa (si el usuario es comercial)
    if hasattr(request.user, 'perfil') and request.user.perfil.rol != 'admin':
        valvulas = valvulas.filter(empresa=request.user.perfil.empresa)
    
    # Filtros por parámetros GET
    estado = request.GET.get('estado')
    requiere = request.GET.get('requiere')  # calibracion o mantenimiento
    busca = request.GET.get('busca')
    
    if estado:
        valvulas = valvulas.filter(estado=estado)
    
    if busca:
        valvulas = valvulas.filter(
            Q(numero_serie__icontains=busca) |
            Q(marca__icontains=busca) |
            Q(modelo__icontains=busca) |
            Q(tag_localizacion__icontains=busca)
        )
    
    # Anotar si requieren servicio
    if requiere == 'calibracion':
        # Esto es una lógica simplificada - en producción usar anotación DB
        valvulas = [v for v in valvulas if v.requiere_calibracion]
    elif requiere == 'mantenimiento':
        valvulas = [v for v in valvulas if v.requiere_mantenimiento]
    
    context = {
        'valvulas': valvulas,
        'estados': Valvula._meta.get_field('estado').choices,
        'filtro_estado': estado,
        'filtro_requiere': requiere,
        'filtro_busca': busca,
    }
    
    return render(request, 'valvulas/lista_valvulas.html', context)


@login_required
def descargar_documento(request, documento_id):
    """
    Descarga un documento PDF asociado a una válvula
    """
    documento = get_object_or_404(Documento, id=documento_id)
    
    # Verificar permisos
    if hasattr(request.user, 'perfil'):
        if request.user.perfil.rol != 'admin':
            if documento.valvula.empresa != request.user.perfil.empresa:
                messages.error(request, 'No tienes permiso para descargar este documento')
                return redirect('/')
    
    if documento.archivo_pdf:
        return redirect(documento.archivo_pdf.url)
    
    messages.error(request, 'El archivo no está disponible')
    return redirect('hoja_vida_valvula', valvula_id=documento.valvula.id)
