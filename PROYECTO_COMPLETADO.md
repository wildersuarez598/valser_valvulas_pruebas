# Valser Portal - Sistema de Gestión de Válvulas
## ✅ Estado: FUNCIONAL EN PRODUCCIÓN

### Dirección en Producción
https://web-production-67e7.up.railway.app

### Credenciales de Prueba
- **Admin**: `admin` / `admin123`
- **Comercial**: `comercial` / `comercial123`
- **Cliente**: `cliente` / `cliente123`

---

## Estructura del Proyecto

### Aplicaciones Django
- **usuarios/** - Autenticación, roles y perfiles
- **servicios/** - Certificados PDF y extracto de datos
- **valvulas/** - Gestión de válvulas
- **clientes/** - Gestión de clientes/empresas
- **config/** - Configuración de Django

### Modelos Principais
- **User** - Django Auth
- **PerfilUsuario** - Roles: Admin, Comercial, Cliente
- **Empresa** - Empresas/Clientes
- **Valvula** - Catálogo de válvulas
- **Certificado** - Certificados PDF y datos extraídos
- **Servicio** - Servicios relacionados a válvulas

### Funcionalidades
✅ Autenticación con roles (Admin, Comercial, Cliente)  
✅ Dashboard personalizado por rol  
✅ Upload y extracción de datos de PDFs  
✅ Panel de administración profesional  
✅ Timezone dinámico (25 zonas horarias)  
✅ Responsive design con Bootstrap 5  
✅ Sistema de permisos basado en decoradores  

### Tecnologías
- Django 6.0.2
- Python 3.14
- Bootstrap 5.3.0
- PDFPlumber (extracción de datos)
- WhiteNoise (static files)
- Gunicorn (WSGI)
- Railway.app (hosting)

### Variables de Entorno (Railway)
```
SECRET_KEY = [generada]
DEBUG = False
ALLOWED_HOSTS = web-production-67e7.up.railway.app
CSRF_TRUSTED_ORIGINS = https://web-production-67e7.up.railway.app
DATABASE_URL = [empty - usa SQLite]
```

### Despliegue
- Repositorio: https://github.com/wildersuarez598/valser_valvulas_pruebas
- Plataforma: Railway.app
- Proceso: `python manage.py migrate && gunicorn config.wsgi`

### Código Limpio
- Imports necesarios (sin redundancias)
- Funciones definidas y usadas
- Decoradores para control de permisos
- Signals para creación automática de usuarios
- Sin archivos de testing innecesarios

### Próximas Mejoras Opcionales
- PostgreSQL en producción
- Almacenamiento de medios en S3
- Caché con Redis
- Tests unitarios
- CI/CD avanzado
