#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Crear usuario admin si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@valser.com', 'admin123')
    print("✅ Usuario admin creado: admin / admin123")
else:
    print("✅ Usuario admin ya existe")
