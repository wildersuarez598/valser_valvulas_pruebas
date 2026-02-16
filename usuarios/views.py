from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import PerfilUsuario, ZONAS_HORARIAS


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vista para iniciar sesión"""
    if request.user.is_authenticated:
        return redirect('usuarios:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name or user.username}!')
                return redirect('usuarios:dashboard')
            else:
                messages.error(request, 'Tu cuenta ha sido desactivada.')
        else:
            messages.error(request, 'Usuario o contraseña inválidos.')
    
    return render(request, 'login.html')


@login_required(login_url='usuarios:login')
def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('usuarios:login')


@login_required(login_url='usuarios:login')
def dashboard(request):
    """
    Dashboard principal - redirige a la vista correspondiente según el rol
    """
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        # Si no existe perfil, crear uno automáticamente
        perfil = PerfilUsuario.objects.create(usuario=request.user)
    
    context = {
        'usuario': request.user,
        'perfil': perfil,
    }
    
    # Redirigir según el rol
    if perfil.rol == 'cliente':
        return redirect('usuarios:cliente_dashboard')
    elif perfil.rol == 'comercial':
        return redirect('usuarios:comercial_dashboard')
    elif perfil.rol == 'admin' or request.user.is_superuser:
        return redirect('/admin/')
    
    return render(request, 'dashboard.html', context)


@login_required(login_url='usuarios:login')
def cliente_dashboard(request):
    """Dashboard para clientes"""
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        return redirect('usuarios:login')
    
    if perfil.rol != 'cliente':
        messages.error(request, 'Acceso denegado.')
        return redirect('usuarios:dashboard')
    
    # Obtener datos del cliente
    empresa = perfil.empresa
    valvulas = empresa.valvulas.all() if empresa else []
    
    # Contar válvulas (maneja QuerySet y lista)
    try:
        total_valvulas = valvulas.count()
    except (TypeError, AttributeError):
        total_valvulas = len(list(valvulas))
    
    context = {
        'usuario': request.user,
        'empresa': empresa,
        'valvulas': valvulas,
        'total_valvulas': total_valvulas,
    }
    
    return render(request, 'cliente/dashboard.html', context)


@login_required(login_url='usuarios:login')
def comercial_dashboard(request):
    """Dashboard para comerciales"""
    from servicios.models import Certificado
    
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        return redirect('usuarios:login')
    
    if perfil.rol != 'comercial':
        messages.error(request, 'Acceso denegado.')
        return redirect('usuarios:dashboard')
    
    # Obtener clientes del comercial
    clientes = PerfilUsuario.objects.filter(rol='cliente').values_list('empresa', flat=True).distinct()
    
    # Obtener certificados del comercial
    certificados = Certificado.objects.filter(usuario_comercial=request.user).order_by('-fecha_emision')[:5]
    
    context = {
        'usuario': request.user,
        'total_clientes': len(clientes),
        'certificados': certificados,
    }
    
    return render(request, 'comercial/dashboard.html', context)


def acceso_denegado(request):
    """Vista cuando se deniega acceso"""
    return render(request, 'acceso_denegado.html', status=403)


@login_required(login_url='usuarios:login')
@require_http_methods(["GET", "POST"])
def cambiar_zona_horaria(request):
    """Vista para cambiar la zona horaria del usuario"""
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        return redirect('usuarios:login')
    
    if request.method == 'POST':
        nueva_zona = request.POST.get('zona_horaria')
        
        # Validar que la zona horaria sea válida
        zonas_validas = [z[0] for z in ZONAS_HORARIAS]
        
        if nueva_zona in zonas_validas:
            perfil.zona_horaria = nueva_zona
            perfil.save()
            messages.success(request, f'Zona horaria actualizada a {nueva_zona}')
            return redirect('usuarios:dashboard')
        else:
            messages.error(request, 'Zona horaria no válida.')
    
    context = {
        'usuario': request.user,
        'zonas_horarias': ZONAS_HORARIAS,
        'zona_actual': perfil.zona_horaria,
    }
    
    return render(request, 'cambiar_zona_horaria.html', context)
