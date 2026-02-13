# 📚 ÍNDICE - Portal Valser

## 👋 ¡Bienvenido al Proyecto Valser!

Este es el **Sistema de Gestión de Mantenimiento y Calibración de Válvulas** construido con Django.

---

## 🚀 EMPEZAR AQUÍ

### 1️⃣ **Lee Primero:** [INICIO_RAPIDO.md](./INICIO_RAPIDO.md)
**¿Qué es?** Guía paso a paso para ejecutar el servidor  
**Toma:** 5 minutos  
**Resultado:** Servidor corriendo en tu navegador

### 2️⃣ **Documentación General:** [README.md](./README.md)
**¿Qué es?** Documentación completa del proyecto  
**Toma:** 15 minutos  
**Resultado:** Entender la estructura y capacidades

### 3️⃣ **Estado Actual:** [ESTADO_FASE_1.md](./ESTADO_FASE_1.md)
**¿Qué es?** Resumen de lo que se completó en FASE 1  
**Toma:** 10 minutos  
**Resultado:** Saber exactamente qué está listo

---

## 📑 DOCUMENTOS POR TÓPICO

### 🎯 Para Principiantes
1. **[INICIO_RAPIDO.md](./INICIO_RAPIDO.md)** - Cómo ejecutar el servidor
2. **[README.md](./README.md)** - Estructura general del proyecto

### 🔧 Para Desarrolladores
1. **[ESTADO_FASE_1.md](./ESTADO_FASE_1.md)** - Resumen técnico
2. **[ARCHIVOS_CREADOS.md](./ARCHIVOS_CREADOS.md)** - Listado de archivos
3. **[FASE_2_PLAN.md](./FASE_2_PLAN.md)** - Plan de desarrollo

### 📋 Configuración
- **[.env.example](./.env.example)** - Variables de entorno
- **[requirements.txt](./requirements.txt)** - Dependencias Python

### 💻 Scripts de Ejecución
- **[runserver.bat](./runserver.bat)** - Para Windows CMD
- **[runserver.ps1](./runserver.ps1)** - Para PowerShell

---

## 🎯 OBJETIVOS DEL PROYECTO

### ✅ Lo que hace Valser

**Para Clientes:**
- Ver sus válvulas registradas
- Consultar historial de servicios
- Descargar certificados
- Ver fechas próximas a vencer

**Para Comerciales:**
- Subir certificados PDF
- Extraer datos automáticamente
- Registrar servicios

**Para Administradores:**
- Gestionar todo el sistema
- Ver reportes
- Configurar parámetros

---

## 🗂️ ESTRUCTURA DEL PROYECTO

```
valser_portal/
├── config/          ← Configuración principal de Django
├── usuarios/        ← App: Gestión de usuarios y roles
├── clientes/        ← App: Gestión de empresas
├── valvulas/        ← App: Registro de válvulas
├── servicios/       ← App: Mantenimientos y calibraciones
├── media/           ← Carpeta para PDFs y archivos
├── venv/            ← Entorno virtual Python
└── Documentación    ← Varios archivos .md
```

---

## 🔑 CREDENCIALES

Para acceder al panel de administración:

```
URL: http://127.0.0.1:8000/admin
Usuario: admin
Contraseña: admin123
```

---

## 📊 ESTADO DEL PROYECTO

### ✅ FASE 1 - COMPLETADA

- [x] Entorno virtual creado
- [x] Dependencias instaladas
- [x] Proyecto Django configurado
- [x] 4 aplicaciones creadas
- [x] 8 modelos de base de datos creados
- [x] Base de datos inicializada
- [x] Superusuario creado
- [x] Servidor corriendo
- [x] Documentación escrita

**Tiempo invertido:** ~30 minutos

### ⏳ FASE 2 - PLANIFICADA

- [ ] Sistema de autenticación
- [ ] Roles y permisos
- [ ] Vistas (views)
- [ ] Templates HTML
- [ ] Validación de acceso

**Estimado:** ~2-3 horas

### ⏳ FASE 3 - FUTURO

- [ ] Panel de clientes
- [ ] Upload de certificados
- [ ] Extracción automática de PDFs
- [ ] Sistema de alertas
- [ ] Reportes

---

## 🚀 PRÓXIMOS PASOS

### ¿Qué debo hacer ahora?

1. **Ejecuta el servidor**
   ```bash
   cd valser_portal
   runserver.bat        (en Windows CMD)
   # o
   .\runserver.ps1      (en PowerShell)
   ```

2. **Abre http://127.0.0.1:8000/admin en tu navegador**

3. **Inicia sesión con:**
   - Usuario: `admin`
   - Contraseña: `admin123`

4. **Explora el panel de administración**

5. **Lee [FASE_2_PLAN.md](./FASE_2_PLAN.md) para continuar**

---

## ❓ PREGUNTAS FRECUENTES

### ¿Cómo ejecuto el servidor?
Ver [INICIO_RAPIDO.md](./INICIO_RAPIDO.md)

### ¿Dónde está la base de datos?
Archivo: `db.sqlite3` (SQLite)

### ¿Cómo instalo dependencias nuevas?
```bash
pip install nombre_paquete
pip freeze > requirements.txt
```

### ¿Cómo creo un nuevo usuario?
```bash
python manage.py createsuperuser
```

### ¿Cómo creo migraciones de modelos?
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📞 INFORMACIÓN TÉCNICA

| Aspecto | Valor |
|--------|-------|
| **Lenguaje** | Python 3.14 |
| **Framework** | Django 6.0.2 |
| **Base de Datos** | SQLite (desarrollo) |
| **Servidor** | Django Development Server |
| **Puerto** | 8000 |
| **Entorno Virtual** | venv/ |

---

## 🔐 SEGURIDAD

⚠️ **Importante para Producción:**

- [ ] Cambiar SECRET_KEY en `settings.py`
- [ ] Cambiar DEBUG a `False`
- [ ] Usar PostgreSQL en lugar de SQLite
- [ ] Configurar ALLOWED_HOSTS
- [ ] Usar SSL/HTTPS
- [ ] Cambiar contraseña del admin

---

## 📚 RECURSOS EXTERNOS

- [Documentación Oficial Django](https://docs.djangoproject.com/)
- [pdfplumber - Lectura de PDFs](https://github.com/jsvine/pdfplumber)
- [Pillow - Procesamiento de Imágenes](https://python-pillow.org/)

---

## 💡 TIPS Y TRUCOS

### Ver todos los usuarios creados
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()
```

### Crear usuario rápidamente
```bash
python manage.py createsuperuser --username test --email test@example.com
```

### Resetear base de datos

⚠️ **CUIDADO - Borra todo:**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 🎓 APRENDE MÁS

### Documentos para leer en orden:

1. **Principiante:** INICIO_RAPIDO.md → README.md
2. **Estudiante:** ESTADO_FASE_1.md → ARCHIVOS_CREADOS.md
3. **Desarrollador:** FASE_2_PLAN.md → Code en cada app

---

## ✉️ SOPORTE

Si tienes problemas:

1. Revisa [README.md](./README.md) - Sección "Solución de Problemas"
2. Verifica que el servidor esté corriendo: `http://127.0.0.1:8000/admin`
3. Revisa la terminal para mensajes de error
4. Consulta la documentación oficial de Django

---

## 🎉 ¡LISTO PARA EMPEZAR!

### Tu próximo movimiento:

📖 Abre [INICIO_RAPIDO.md](./INICIO_RAPIDO.md)

O ejecuta directamente:

```bash
cd valser_portal
.\runserver.ps1
```

Luego accede a:
```
http://127.0.0.1:8000/admin
```

---

**Bienvenido al equipo Valser! 🚀**

*Proyecto: Sistema de Gestión de Válvulas*  
*Fecha: Febrero 2026*  
*Versión: FASE 1 - Completo*
