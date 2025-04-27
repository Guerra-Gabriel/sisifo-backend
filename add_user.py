#!/opt/venvs/sisifo-auth/bin/python

import getpass
import MySQLdb
from werkzeug.security import generate_password_hash

# Configuración de conexión
DB_HOST = 'localhost'
DB_USER = 'sisifo_login'
DB_PASS = 'Lamichabot2025#'
DB_NAME = 'sisifo_auth'

def main():
    print("📋 Crear nuevo usuario (modo CLI)\n")

    username = input("👤 Nombre de usuario: ")
    email = input("📧 Correo electrónico: ")
    password = getpass.getpass("🔒 Contraseña: ")
    role = input("🔐 Rol (admin / user / moderator): ").strip().lower()

    if role not in ["admin", "user", "moderator"]:
        print("❌ Rol inválido. Usa uno de: admin, user, moderator.")
        return

    is_active = input("✅ ¿Activo? (s/n): ").strip().lower() == "s"

    # Hashear contraseña
    hashed_password = generate_password_hash(password)

    # Insertar en la base de datos
    try:
        connection = MySQLdb.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASS,
            db=DB_NAME,
            charset='utf8mb4'
        )
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO users (username, email, password, role, is_active)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, email, hashed_password, role, int(is_active)))
        connection.commit()
        cursor.close()
        connection.close()

        print("✅ Usuario creado exitosamente.")
    except Exception as e:
        print(f"❌ Error al crear el usuario: {e}")

if __name__ == "__main__":
    main()
