# 🔧 Portal Valser - Sistema de Gestión de Válvulas

## 📋 Descripción

**Valser** es un sistema web para gestionar el mantenimiento y calibración de válvulas. Permite a los clientes:
- Acceder únicamente a su información
- Consultar historial de mantenimientos y calibraciones
- Ver datos de válvulas
- Descargar certificados de calibración y mantenimiento
- Ver fechas de últimos servicios

Los **comerciales** pueden:
- Subir certificados PDF de calibración y mantenimiento
- El sistema extrae automáticamente los datos de los PDFs

---

## ✅ FASE 1 - Estado Actual: COMPLETADO

### Estructura Base Creada

```
valser_portal/
├── venv/                    # Entorno virtual Python
├── config/                  # Configuración principal Django
│   ├── settings.py         # Configuración del proyecto
│   ├── urls.py             # Rutas principales
│   └── wsgi.py / asgi.py   # Configuración WSGI/ASGI
├── usuarios/               # App: Gestión de usuarios y roles
├── clientes/               # App: Gestión de empresas clientes
├── valvulas/              # App: Activos (válvulas)
├── servicios/             # App: Mantenimientos y calibraciones
├── media/                 # Carpeta para certificados PDF
├── manage.py              # Herramienta de gestión Django
└── README.md             # Este archivo
```

### Tecnologías Instaladas

| Paquete | Versión | Propósito |
|---------|---------|----------|
| **Django** | 6.0.2 | Framework web Python |
| **psycopg2-binary** | 2.9.11 | Conector PostgreSQL |
| **pdfplumber** | 0.11.9 | Lectura de archivos PDF |
| **Pillow** | 12.1.1 | Procesamiento de imágenes |

### Base de Datos

- **Tipo:** PostgreSQL (configurado)
- **ODM:** Django ORM
- **Migraciones:** Aplicadas ✅

### Credenciales de Acceso

| Campo | Valor |
|-------|-------|
| **Usuario** | `admin` |
| **Contraseña** | `admin123` |
| **URL Admin** | `http://127.0.0.1:8000/admin` |

---

## 🚀 Cómo Usar

### 1. Activar el Entorno Virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\python.exe -m pip --version
```

**Windows (CMD):**
```cmd
venv\Scripts\activate
```

### 2. Instalar Dependencias (si es necesario)

```bash
pip install django psycopg2-binary pdfplumber pillow
```

### 3. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 4. Iniciar Servidor de Desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en: **http://127.0.0.1:8000**

### 5. Acceder al Panel de Administración

- **URL:** `http://127.0.0.1:8000/admin`
- **Usuario:** `admin`
- **Contraseña:** `admin123`

---

## 📦 Estructura de Apps

### 1. `usuarios` - Gestión de Usuarios y Roles
- Modelos: Usuario (Cliente, Comercial, Admin)
- Gestión de autenticación y permisos
- *Estado:* Pendiente configuración en FASE 2

### 2. `clientes` - Empresas Cliente
- Modelos: Empresa, Contactos
- Información de clientes
- *Estado:* Pendiente configuración en FASE 2

### 3. `valvulas` - Activos (Válvulas)
- Modelos: Válvula, Datos técnicos
- Registro de activos por cliente
- *Estado:* Pendiente configuración en FASE 2

### 4. `servicios` - Mantenimientos y Calibraciones
- Modelos: Servicio, Certificado
- Historial de servicios
- Extracción automática de datos desde PDF
- *Estado:* Pendiente configuración en FASE 2

---

## 📁 Carpetas Destacadas

### `/media`
Directorio donde se guardan:
- Certificados de calibración (PDF)
- Certificados de mantenimiento (PDF)
- Documentos relacionados

Configurado en `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'
```

### `/config`
Contiene la configuración central del proyecto:
- `settings.py` - Variables de configuración
- `urls.py` - Rutas principales
- `wsgi.py` - Servidor de producción

---

## 🔄 Próximas Fases

### 🔐 FASE 2 - Sistema de Usuarios y Roles
- [ ] Crear modelos de Usuario (Cliente, Comercial)
- [ ] Sistema de autenticación y login
- [ ] Asignación de roles y permisos
- [ ] Dashboard para cada tipo de usuario

### 📊 FASE 3 - Panel de Clientes
- [ ] Vista de válvulas del cliente
- [ ] Visualización de historial
- [ ] Descarga de certificados

### 📤 FASE 4 - Upload de Certificados (Comerciales)
- [ ] Interfaz de carga de PDF
- [ ] Extracción automática con pdfplumber
- [ ] Validación y almacenamiento

### 🔍 FASE 5 - Búsqueda y Reportes
- [ ] Búsqueda de válvulas por cliente
- [ ] Generación de reportes
- [ ] Alertas de servicios vencidos

---

## ⚙️ Configuración Django

### Apps Registradas

En `config/settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',        # ✅ Agregada
    'clientes',        # ✅ Agregada
    'valvulas',        # ✅ Agregada
    'servicios',       # ✅ Agregada
]
```

### URLs de Media

En `config/urls.py`:
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 🛠️ Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell interactivo de Django
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic

# Limpiar archivos temporales
python manage.py cleanup
```

---

## 📝 Notas Importantes

✅ **Completado en FASE 1:**
- Proyecto Django funcionando
- Apps creadas y registradas
- Base de datos configurada
- Entorno de desarrollo listo
- Admin accesible
- Estructura lista para crecer

🚨 **Siguiente paso:**
- Implementar FASE 2: Sistema de Usuarios y Roles

---

## 🆘 Solución de Problemas

### El servidor no inicia
1. Verifica que estés en el directorio correcto
2. Confirma que el entorno virtual esté activado
3. Revisa que las migraciones estén aplicadas: `python manage.py migrate`

### Error en MEDIA_URL
Si los archivos PDF no se sirven correctamente:
1. Crea la carpeta `media/` si no existe
2. Verifica permisos de escritura en la carpeta
3. Asegúrate de que DEBUG=True en settings.py

### Error de base de datos
- SQLite por defecto puede tener limitaciones
- Configura PostgreSQL para producción
- Instala: `pip install psycopg2-binary`

---

## 📞 Contacto

**Empresa:** Valser Industriales S.A.S
**Ambiente:** Desarrollo Local
**Creado:** Febrero 2026

---

**¡Listo para continuar a FASE 2! 🚀**
