"""
Decoradores para control de acceso basado en roles
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def requiere_rol(*roles):
    """
    Decorador para verificar que el usuario tiene uno de los roles especificados
    
    Uso:
        @requiere_rol('cliente')
        def mi_vista(request):
            ...
        
        @requiere_rol('comercial', 'admin')
        def otra_vista(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='/login/')
        def wrapper(request, *args, **kwargs):
            try:
                perfil = request.user.perfil
                if perfil.rol in roles and perfil.activo:
                    return view_func(request, *args, **kwargs)
            except AttributeError:
                pass
            
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('/acceso_denegado/')
        return wrapper
    return decorator


def requiere_cliente(view_func):
    """Decorador simplificado para requerir rol de cliente"""
    @wraps(view_func)
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        try:
            perfil = request.user.perfil
            if perfil.rol == 'cliente' and perfil.activo:
                return view_func(request, *args, **kwargs)
        except AttributeError:
            pass
        
        messages.error(request, 'Acceso solo para clientes.')
        return redirect('/acceso_denegado/')
    return wrapper


def requiere_comercial(view_func):
    """Decorador simplificado para requerir rol de comercial"""
    @wraps(view_func)
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        try:
            perfil = request.user.perfil
            if perfil.rol == 'comercial' and perfil.activo:
                return view_func(request, *args, **kwargs)
        except AttributeError:
            pass
        
        messages.error(request, 'Acceso solo para comerciales.')
        return redirect('/acceso_denegado/')
    return wrapper


def requiere_admin(view_func):
    """Decorador simplificado para requerir rol de admin"""
    @wraps(view_func)
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        try:
            perfil = request.user.perfil
            if perfil.rol == 'admin' and perfil.activo:
                return view_func(request, *args, **kwargs)
        except AttributeError:
            pass
        
        messages.error(request, 'Acceso solo para administradores.')
        return redirect('/acceso_denegado/')
    return wrapper


def requiere_activo(view_func):
    """Decorador para verificar que el usuario está activo"""
    @wraps(view_func)
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        try:
            perfil = request.user.perfil
            if not perfil.activo:
                messages.error(request, 'Tu cuenta ha sido desactivada.')
                return redirect('/login/')
        except AttributeError:
            pass
        
        return view_func(request, *args, **kwargs)
    return wrapper
