from flask import current_app
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash
from typing import Optional, Dict, Any

mysql = MySQL()

def init_db(app):
    """Inicializa la extensión de MySQL con la app Flask."""
    mysql.init_app(app)


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """
    Recupera un usuario por su nombre de usuario.
    Retorna un diccionario con los datos si lo encuentra, o None.
    """
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT username, password, role, is_active FROM users WHERE username = %s",
            (username,)
        )
        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "username": result[0],
                "password": result[1],
                "role": result[2],
                "is_active": result[3]
            }
        return None

    except Exception as e:
        current_app.logger.error(f"❌ Error al consultar el usuario '{username}': {e}")
        return None


def verify_password(hashed_password: str, plain_password: str) -> bool:
    """
    Verifica si la contraseña ingresada coincide con el hash almacenado.
    """
    try:
        return check_password_hash(hashed_password, plain_password)
    except Exception as e:
        current_app.logger.error(f"❌ Error al verificar la contraseña: {e}")
        return False
