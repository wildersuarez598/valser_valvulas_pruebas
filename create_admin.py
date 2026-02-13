#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario

# Crear usuario admin
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@valser.com', 'admin123')
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=admin, defaults={'rol': 'Admin'})
    print("✅ Usuario admin creado")
else:
    print("✅ Usuario admin ya existe")

# Crear usuario comercial
if not User.objects.filter(username='comercial').exists():
    comercial = User.objects.create_user('comercial', 'comercial@valser.com', 'comercial123')
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=comercial, defaults={'rol': 'Comercial'})
    print("✅ Usuario comercial creado")
else:
    print("✅ Usuario comercial ya existe")

# Crear usuario cliente
if not User.objects.filter(username='cliente').exists():
    cliente = User.objects.create_user('cliente', 'cliente@valser.com', 'cliente123')
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=cliente, defaults={'rol': 'Cliente'})
    print("✅ Usuario cliente creado")
else:
    print("✅ Usuario cliente ya existe")

print("\n📋 Credenciales disponibles:")
print("Admin:      admin / admin123")
print("Comercial:  comercial / comercial123")
print("Cliente:    cliente / cliente123")
