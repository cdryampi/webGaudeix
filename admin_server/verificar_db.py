#!/usr/bin/env python
"""
Script para verificar la conexión a la base de datos PostgreSQL.
Ayuda a diagnosticar problemas de autenticación.
"""

import psycopg
import json
import os
from pathlib import Path

# Cargar configuración
config_path = Path(__file__).parent.parent / "gaudeix" / "config.json"
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

db_config = config["DATABASES"]["default"]

print("=" * 60)
print("DIAGNÓSTICO DE CONEXIÓN A LA BASE DE DATOS")
print("=" * 60)
print(f"\nConfigurable:")
print(f"  HOST: {db_config['HOST']}")
print(f"  PORT: {db_config['PORT']}")
print(f"  DATABASE: {db_config['NAME']}")
print(f"  USER: {db_config['USER']}")
print(f"  PASSWORD: {'*' * len(db_config['PASSWORD'])}")

print("\n" + "-" * 60)
print("Intentando conectar con psycopg3...")
print("-" * 60)

try:
    conninfo = f"dbname={db_config['NAME']} user={db_config['USER']} password={db_config['PASSWORD']} host={db_config['HOST']} port={db_config['PORT']}"
    conn = psycopg.connect(conninfo)
    print("✅ ¡CONEXIÓN EXITOSA!")
    
    # Obtener información del servidor
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"\n📊 Versión de PostgreSQL:")
    print(f"  {version}")
    
    cursor.execute("SELECT current_database(), current_user;")
    db, user = cursor.fetchone()
    print(f"\n📌 Información de conexión:")
    print(f"  Base de datos actual: {db}")
    print(f"  Usuario actual: {user}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ Todo está configurado correctamente.")
    print("=" * 60)
    
except psycopg.OperationalError as e:
    print(f"❌ ERROR DE CONEXIÓN:\n")
    error_msg = str(e)
    
    if "authentication failed" in error_msg or "autentificaci" in error_msg or "password fall" in error_msg:
        print("⚠️  PROBLEMA DE AUTENTICACIÓN")
        print("\nLa contraseña es incorrecta o el usuario no tiene permisos.")
        print("\nSOLUCIONES POSIBLES:")
        print("\n1. Resetear la contraseña en PostgreSQL:")
        print(f"   Ejecuta en psql como superusuario (postgres):")
        print(f"   ALTER USER {db_config['USER']} WITH PASSWORD 'nueva_contraseña';")
        print("\n2. Verificar que el usuario existe:")
        print(f"   SELECT usename FROM pg_user WHERE usename = '{db_config['USER']}';")
        print("\n3. Actualizar config.json con la contraseña correcta")
        print("\n4. Conectarte a PostgreSQL con el comando:")
        print(f"   psql -U postgres -h localhost")
        print("   Y luego ejecutar:")
        print(f"   ALTER USER {db_config['USER']} WITH PASSWORD 'nueva_contraseña';")
        
    elif "could not connect" in error_msg or "connection refused" in error_msg:
        print("⚠️  PROBLEMA DE CONEXIÓN AL SERVIDOR")
        print("\nNo se puede conectar al servidor PostgreSQL.")
        print("\nVerifica:")
        print("1. PostgreSQL está ejecutándose")
        print("2. El puerto y host son correctos")
        print("3. El firewall permite la conexión")
        
    else:
        print(f"Error: {error_msg}")
    
    print("\n" + "=" * 60)
    print("❌ La conexión falló.")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ ERROR INESPERADO: {type(e).__name__}")
    print(f"   {str(e)}")
    print("\n" + "=" * 60)
    print("❌ Error inesperado.")
    print("=" * 60)
