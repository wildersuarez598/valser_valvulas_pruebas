#!/usr/bin/env python
"""
Script para crear usuarios de prueba para FASE 2
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario
from clientes.models import Empresa

def crear_usuarios_prueba():
    print("\n" + "="*60)
    print("CREANDO USUARIOS DE PRUEBA - FASE 2")
    print("="*60 + "\n")
    
    # 1. Crear empresa de prueba
    empresa, creada = Empresa.objects.get_or_create(
        nit='900123456',
        defaults={
            'nombre': 'Empresa Test S.A.S',
            'email': 'contacto@empresatest.com',
            'telefono': '3001234567',
            'direccion': 'Calle Principal 123',
            'ciudad': 'Bogotá',
            'departamento': 'Cundinamarca',
            'contacto_principal': 'Juan Pérez',
            'cargo_contacto': 'Jefe de Planta',
            'activa': True
        }
    )
    if creada:
        print(f"✓ Empresa creada: {empresa.nombre}")
    else:
        print(f"✓ Empresa existente: {empresa.nombre}")
    
    # 2. Crear usuario CLIENTE
    usuario_cliente, creado = User.objects.get_or_create(
        username='cliente01',
        defaults={
            'email': 'cliente@empresatest.com',
            'first_name': 'Juan',
            'last_name': 'Cliente',
            'is_active': True
        }
    )
    if creado:
        usuario_cliente.set_password('cliente123')
        usuario_cliente.save()
        print(f"✓ Usuario CLIENTE creado: {usuario_cliente.username}")
    else:
        print(f"✓ Usuario CLIENTE existente: {usuario_cliente.username}")
    
    # Actualizar perfil de cliente
    perfil_cliente, creado_perfil = PerfilUsuario.objects.get_or_create(
        usuario=usuario_cliente,
        defaults={
            'rol': 'cliente',
            'empresa': empresa,
            'zona_horaria': 'America/Bogota',
            'activo': True
        }
    )
    if not creado_perfil:
        perfil_cliente.rol = 'cliente'
        perfil_cliente.empresa = empresa
        perfil_cliente.zona_horaria = 'America/Bogota'
        perfil_cliente.activo = True
        perfil_cliente.save()
    print(f"  └─ Perfil: Cliente | Empresa: {empresa.nombre} | Zona: Bogotá (UTC-5)")
    
    # 3. Crear usuario COMERCIAL
    usuario_comercial, creado = User.objects.get_or_create(
        username='comercial01',
        defaults={
            'email': 'comercial@valser.com',
            'first_name': 'Carlos',
            'last_name': 'Comercial',
            'is_active': True
        }
    )
    if creado:
        usuario_comercial.set_password('comercial123')
        usuario_comercial.save()
        print(f"✓ Usuario COMERCIAL creado: {usuario_comercial.username}")
    else:
        print(f"✓ Usuario COMERCIAL existente: {usuario_comercial.username}")
    
    # Actualizar perfil de comercial
    perfil_comercial, creado_perfil = PerfilUsuario.objects.get_or_create(
        usuario=usuario_comercial,
        defaults={
            'rol': 'comercial',
            'zona_horaria': 'America/Guatemala',
            'activo': True
        }
    )
    if not creado_perfil:
        perfil_comercial.rol = 'comercial'
        perfil_comercial.zona_horaria = 'America/Guatemala'
        perfil_comercial.activo = True
        perfil_comercial.save()
    print(f"  └─ Perfil: Comercial | Zona: Guatemala (UTC-6)")
    
    # 4. Actualizar usuario ADMIN
    usuario_admin = User.objects.get(username='admin')
    perfil_admin, creado_perfil = PerfilUsuario.objects.get_or_create(
        usuario=usuario_admin,
        defaults={
            'rol': 'admin',
            'zona_horaria': 'UTC',
            'activo': True
        }
    )
    if not creado_perfil:
        perfil_admin.rol = 'admin'
        perfil_admin.zona_horaria = 'UTC'
        perfil_admin.activo = True
        perfil_admin.save()
    print(f"✓ Usuario ADMIN (existente)")
    print(f"  └─ Perfil: Admin | Zona: UTC")
    
    print("\n" + "="*60)
    print("CREDENCIALES DE PRUEBA")
    print("="*60)
    print(f"\n👤 CLIENTE:")
    print(f"   Usuario: cliente01")
    print(f"   Contraseña: cliente123")
    print(f"   Empresa: {empresa.nombre}\n")
    
    print(f"👥 COMERCIAL:")
    print(f"   Usuario: comercial01")
    print(f"   Contraseña: comercial123\n")
    
    print(f"👑 ADMIN:")
    print(f"   Usuario: admin")
    print(f"   Contraseña: admin123\n")
    
    print("="*60)
    print("✓ Usuarios de prueba creados exitosamente")
    print("="*60 + "\n")

if __name__ == '__main__':
    crear_usuarios_prueba()
