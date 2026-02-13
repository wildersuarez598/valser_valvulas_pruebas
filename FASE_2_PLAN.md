# 🔐 FASE 2 — Sistema de Usuarios y Roles (Cliente / Comercial)

## 📋 Objetivo

Implementar sistema completo de autenticación, roles y permisos para que:
- **Clientes** accedan solo a su información
- **Comerciales** suban certificados y gestionen servicios
- **Administradores** gestionen todo el sistema

---

## 🏗️ Estructura de Roles y Permisos

### 1️⃣ CLIENTE
Permiso: Acceso de solo lectura a su información

**Funcionalidades:**
- Ver sus válvulas registradas
- Ver historial de servicios (mantenimiento y calibración)
- Descargar certificados
- Ver fechas de próximos servicios vencidos
- Ver alertas de servicios pendientes

**Restricciones:**
- No puede ver información de otros clientes
- No puede subir archivos
- No puede crear servicios

---

### 2️⃣ COMERCIAL
Permiso: Carga de certificados y gestión de servicios

**Funcionalidades:**
- Subir certificados PDF (calibración y mantenimiento)
- Crear/editar servicios
- Ver todas las válvulas de sus clientes
- Extraer datos automáticamente de PDFs

**Restricciones:**
- No puede ver información de clientes de otros comerciales
- No puede eliminar certificados
- No puede acceder al admin de Django

---

### 3️⃣ ADMINISTRADOR
Permiso: Acceso total al sistema

**Funcionalidades:**
- Acceso completo al panel de admin de Django
- Gestionar usuarios y roles
- Ver reportes
- Configurar parámetros del sistema

---

## 🔧 Tareas (Paso a Paso)

### PASO 1: Registrar Modelos en Admin

**Archivo:** `usuarios/admin.py`
```python
from django.contrib import admin
from .models import PerfilUsuario, LogActividad

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'empresa', 'activo')
    list_filter = ('rol', 'activo')
    search_fields = ('usuario__username', 'usuario__email')

@admin.register(LogActividad)
class LogActividadAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'fecha')
    list_filter = ('fecha', 'usuario')
    readonly_fields = ('fecha',)
```

**Archivo:** `clientes/admin.py`
- Registrar `Empresa` y `Contacto`

**Archivo:** `valvulas/admin.py`
- Registrar `Valvula` y `EspecificacionTecnica`

**Archivo:** `servicios/admin.py`
- Registrar `Servicio`, `Certificado` y `AlertaServicio`

---

### PASO 2: Crear Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### PASO 3: Crear Vista de Login

**Archivo:** `usuarios/views.py`
```python
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

@login_required
def dashboard(request):
    perfil = request.user.perfil
    if perfil.rol == 'cliente':
        return render(request, 'cliente/dashboard.html')
    elif perfil.rol == 'comercial':
        return render(request, 'comercial/dashboard.html')
    elif perfil.rol == 'admin':
        return redirect('/admin')
```

---

### PASO 4: Crear Decorador para Permisos

**Archivo:** `usuarios/decorators.py`
```python
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def requiere_rol(rol):
    """Decorador para verificar rol del usuario"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if hasattr(request.user, 'perfil') and request.user.perfil.rol == rol:
                return view_func(request, *args, **kwargs)
            return redirect('acceso_denegado')
        return wrapper
    return decorator

@requiere_rol('cliente')
def vista_cliente(request):
    pass
```

---

### PASO 5: Crear Templates Base

**Estructura de templates:**
```
templates/
├── base.html                 # Template base
├── login.html               # Página de login
├── cliente/
│   ├── dashboard.html       # Dashboard cliente
│   ├── mis_valvulas.html    # Listado de válvulas
│   └── certificados.html    # Descarga de certificados
├── comercial/
│   ├── dashboard.html       # Dashboard comercial
│   ├── subir_certificado.html
│   └── gestionar_servicios.html
└── admin/
    └── dashboard.html
```

---

### PASO 6: Crear URLs

**Archivo:** `usuarios/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
```

**Archivo:** `config/urls.py`
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
]
```

---

### PASO 7: Crear Señales para Crear Perfil Automáticamente

**Archivo:** `usuarios/signals.py`
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PerfilUsuario

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)
```

**En `usuarios/apps.py`:**
```python
def ready(self):
    import usuarios.signals
```

---

### PASO 8: Crear Middleware para Logging

**Archivo:** `usuarios/middleware.py`
```python
from .models import LogActividad

class LogActividadMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            LogActividad.objects.create(
                usuario=request.user,
                accion=f"{request.method} {request.path}",
                direccion_ip=self.get_client_ip(request)
            )
        return response
    
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

---

## ✅ Checklist de FASE 2

- [ ] Modelos creados (ya completado)
- [ ] Migraciones hechas
- [ ] Modelos registrados en Admin
- [ ] Vista de Login creada
- [ ] Decorador de roles implementado
- [ ] Templates base creados
- [ ] URLs configuradas
- [ ] Señales para perfil creadas
- [ ] Middleware de logging habilitado
- [ ] Prueba de login (Cliente, Comercial, Admin)
- [ ] Verificar aislamiento de datos por cliente

---

## 🧪 Pruebas Recomendadas

1. Crear 3 usuarios diferentes (cliente, comercial, admin)
2. Verificar que cada rol ve solo su información
3. Validar que el login funciona correctamente
4. Probar el logout
5. Verificar logging de actividades

---

## 📝 Notas Importantes

⚠️ **Seguridad:**
- Las contraseñas deben hashearse (Django lo hace automáticamente)
- Usar HTTPS en producción
- Implementar CSRF protection (ya incluido en Django)

📦 **Base de Datos:**
- After executing `makemigrations`, review the file before running `migrate`
- Keep migration files in version control

🔐 **Permisos:**
- Siempre validar permisos en el servidor (no confiar en cliente)
- Usar decoradores `@login_required` y `@requiere_rol`

---

**Próxima fase:** 📊 FASE 3 - Panel de Clientes
