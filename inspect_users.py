#!/usr/bin/env python
"""
Inspección del sistema de usuarios y roles
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario

print("\n" + "="*80)
print("INSPECT: Usuarios y Roles en el Sistema")
print("="*80 + "\n")

usuarios = User.objects.all()
print(f"Total de usuarios: {usuarios.count()}\n")

for user in usuarios:
    print(f"[{user.id}] {user.username}")
    print(f"    - Email: {user.email}")
    print(f"    - Activo: {user.is_active}")
    print(f"    - Staff: {user.is_staff}")
    print(f"    - Superuser: {user.is_superuser}")
    
    try:
        perfil = user.perfil
        print(f"    - Rol: {perfil.rol}")
        print(f"    - Empresa: {perfil.empresa}")
        print(f"    - Zona Horaria: {perfil.zona_horaria}")
        print(f"    - Activo: {perfil.activo}")
    except PerfilUsuario.DoesNotExist:
        print(f"    - Rol: [SIN PERFIL]")
    
    # Documentos del usuario
    from servicios.models import Documento
    docs = Documento.objects.filter(usuario_comercial=user)
    if docs.exists():
        print(f"    - Documentos subidos: {docs.count()}")
        for doc in docs[:3]:
            print(f"      • {doc.numero_documento or '(sin #)'} - {doc.get_tipo_documento_display()}")
    
    print()

print("="*80)
