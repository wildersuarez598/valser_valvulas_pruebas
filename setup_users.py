#!/usr/bin/env python
"""Setup script to create default users for Railway deployment."""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

def create_users():
    """Create default test users."""
    users = [
        {'username': 'admin', 'email': 'admin@valser.com', 'password': 'admin123', 'is_superuser': True, 'is_staff': True},
        {'username': 'comercial', 'email': 'comercial@valser.com', 'password': 'comercial123', 'is_superuser': False, 'is_staff': True},
        {'username': 'cliente', 'email': 'cliente@valser.com', 'password': 'cliente123', 'is_superuser': False, 'is_staff': False},
    ]
    
    for user_data in users:
        username = user_data.pop('username')
        email = user_data.pop('email')
        password = user_data.pop('password')
        
        try:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password, **user_data)
                print(f"✅ Usuario creado: {username}")
            else:
                print(f"User ya existe: {username}")
        except Exception as e:
            print(f"Error creating {username}: {e}")

if __name__ == '__main__':
    try:
        create_users()
        print("✅ Setup completado")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
