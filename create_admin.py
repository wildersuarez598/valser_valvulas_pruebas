#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    from django.contrib.auth.models import User
    
    # Crear usuario admin
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@valser.com', 'admin123')
        print("✅ Usuario admin creado")
    else:
        print("✅ Usuario admin ya existe")
    
    # Crear usuario comercial
    if not User.objects.filter(username='comercial').exists():
        User.objects.create_user('comercial', 'comercial@valser.com', 'comercial123', is_staff=True)
        print("✅ Usuario comercial creado")
    else:
        print("✅ Usuario comercial ya existe")
    
    # Crear usuario cliente
    if not User.objects.filter(username='cliente').exists():
        User.objects.create_user('cliente', 'cliente@valser.com', 'cliente123')
        print("✅ Usuario cliente creado")
    else:
        print("✅ Usuario cliente ya existe")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
