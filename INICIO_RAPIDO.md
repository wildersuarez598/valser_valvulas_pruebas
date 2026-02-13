# 🚀 GUÍA RÁPIDA - Cómo Ejecutar el Servidor

## 1️⃣ Localización del Proyecto

```
C:\Users\Administracion\OneDrive - VALSER INDUSTRIALES S.A.S\
Documentos\proyecto\OTROS\Valvulas\valser_portal
```

---

## 2️⃣ Opción A: Usar Script (RECOMENDADO)

### En PowerShell:

Haz clic derecho en `runserver.ps1` → Ejecutar con PowerShell

O ejecuta en PowerShell:
```powershell
cd "C:\Users\Administracion\OneDrive - VALSER INDUSTRIALES S.A.S\Documentos\proyecto\OTROS\Valvulas\valser_portal"
.\runserver.ps1
```

### En CMD (Símbolo del Sistema):

Haz doble clic en `runserver.bat`

O ejecuta en CMD:
```cmd
cd C:\Users\Administracion\OneDrive - VALSER INDUSTRIALES S.A.S\Documentos\proyecto\OTROS\Valvulas\valser_portal
runserver.bat
```

---

## 3️⃣ Opción B: Manual (Si los scripts no funcionan)

### Paso 1: Abre PowerShell o CMD

Navega a la carpeta del proyecto

### Paso 2: Ejecuta el servidor

**PowerShell:**
```powershell
$pythonPath = "C:\Users\Administracion\OneDrive - VALSER INDUSTRIALES S.A.S\Documentos\proyecto\OTROS\Valvulas\valser_portal\venv\Scripts\python.exe"
& $pythonPath manage.py runserver
```

**CMD:**
```cmd
venv\Scripts\python.exe manage.py runserver
```

---

## 4️⃣ Acceder al Servidor

Una vez que veas este mensaje:
```
Starting development server at http://127.0.0.1:8000/
```

### Abre tu navegador web:

**Página Principal:**
```
http://127.0.0.1:8000
```

**Panel Administrativo:**
```
http://127.0.0.1:8000/admin
```

---

## 5️⃣ Credenciales de Acceso

Para entrar al panel de administración:

| Campo | Valor |
|-------|-------|
| **Usuario** | `admin` |
| **Contraseña** | `admin123` |

---

## 6️⃣ Detener el Servidor

Presiona:
```
CTRL + C
```

en la terminal donde está corriendo el servidor.

---

## ⚠️ Solución de Problemas

### El script .ps1 no se ejecuta

**Error:** "No se puede cargar el archivo porque la ejecución de scripts está deshabilitada"

**Solución:** Usa `runserver.bat` en su lugar o ejecuta en CMD

### El servidor no inicia

**Error:** "ModuleNotFoundError: No module named..."

**Solución:** El entorno virtual no está activado. Verifica que existe la carpeta `venv/`

### Puerto 8000 ya está en uso

**Error:** "Address already in use"

**Solución:** Otro proceso está en el puerto 8000. Usa:
```
python manage.py runserver 8001
```

Accede entonces a `http://127.0.0.1:8001`

---

## ✅ Verificación

Si ves esto en la terminal:
```
System check identified no issues (0 silenced).
February 13, 2026 - 10:21:15
Django version 6.0.2, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
```

✅ **¡El servidor está corriendo correctamente!**

---

## 📁 Estructura de Carpetas

```
valser_portal/
├── venv/               ← No tocar (entorno virtual)
├── config/             ← Configuración Django
├── usuarios/           ← App: Usuarios
├── clientes/           ← App: Clientes
├── valvulas/           ← App: Válvulas
├── servicios/          ← App: Servicios
├── media/              ← Archivos subidos (PDFs, imágenes)
├── manage.py           ← Herramienta de Django
├── db.sqlite3          ← Base de datos
├── runserver.bat       ← Script Windows CMD
├── runserver.ps1       ← Script PowerShell
├── README.md           ← Documentación
├── requirements.txt    ← Dependencias
└── FASE_2_PLAN.md      ← Próxima fase
```

---

## 🎯 Próximos Pasos

Una vez que el servidor esté corriendo:

1. ✅ Accede a `http://127.0.0.1:8000/admin`
2. ✅ Inicia sesión con `admin` / `admin123`
3. ✅ Explora las opciones disponibles
4. ✅ Lee `FASE_2_PLAN.md` para la siguiente etapa

---

**¡Listo para empezar! 🚀**
