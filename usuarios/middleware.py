"""
Middleware para registrar la actividad de los usuarios y aplicar zona horaria
"""
import logging
import pytz
from django.utils import timezone
from .models import LogActividad

logger = logging.getLogger(__name__)


class SetearZonaHorariaMiddleware:
    """
    Middleware que establece la zona horaria del usuario autenticado
    Basado en la zona horaria configurada en su perfil
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Establecer zona horaria si el usuario está autenticado
        if request.user.is_authenticated:
            try:
                zona_horaria = request.user.perfil.zona_horaria
                timezone.activate(pytz.timezone(zona_horaria))
            except Exception as e:
                logger.warning(f"Error al establecer zona horaria para usuario autenticado: {e}")
                timezone.activate(pytz.timezone('America/Bogota'))
        else:
            # Usar zona horaria por defecto para usuarios no autenticados
            try:
                timezone.activate(pytz.timezone('America/Bogota'))
            except Exception as e:
                logger.warning(f"Error al establecer zona horaria por defecto: {e}")
        
        response = self.get_response(request)
        return response


class LogActividadMiddleware:
    """
    Middleware que registra cada solicitud HTTP de usuarios autenticados
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Procesar la solicitud
        response = self.get_response(request)
        
        # Registrar actividad si el usuario está autenticado
        if request.user.is_authenticated:
            try:
                # No registrar solicitudes a recursos estáticos ni al admin excesivamente
                if not self._es_recurso_excluido(request.path):
                    LogActividad.objects.create(
                        usuario=request.user,
                        accion=f"{request.method} {request.path}",
                        descripcion=f"Status: {response.status_code}",
                        direccion_ip=self._obtener_ip_cliente(request)
                    )
            except Exception as e:
                logger.error(f"Error registrando actividad: {e}")
        
        return response
    
    @staticmethod
    def _obtener_ip_cliente(request):
        """Obtener la IP verdadera del cliente considerando proxies"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def _es_recurso_excluido(path):
        """Verificar si el path debe ser excluido del logging"""
        recursos_excluidos = [
            '/static/',
            '/media/',
            '/favicon.ico',
        ]
        return any(path.startswith(excluido) for excluido in recursos_excluidos)
