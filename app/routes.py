from flask import Blueprint, request, jsonify
from app.models import get_user_by_username, verify_password

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return "🟢 ¡Servidor Flask activo y funcionando!"

@main.route("/pong")
def pong():
    return jsonify({"message": "¡Pong! Flask responde desde el backend."})

@main.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return '', 200  # 👈 Respondemos ok al preflight
    data = request.get_json()
    print("📨 Datos recibidos:", data)

    username = data.get("username")
    password = data.get("password")

    password_display = '*' * len(password) if password else 'None'
    print(f"👤 Usuario: {username}, 🔑 Contraseña: {password_display}")

    if not username or not password:
        print("❌ Faltan credenciales")
        return jsonify({"error": "Faltan credenciales"}), 400

    user = get_user_by_username(username)
    if not user:
        print("❌ Usuario no encontrado")
        return jsonify({"error": "Usuario no encontrado"}), 404

    if not user["is_active"]:
        print("⛔ Usuario inactivo")
        return jsonify({"error": "Usuario inactivo"}), 403

    if not verify_password(user["password"], password):
        print("❌ Contraseña incorrecta")
        return jsonify({"error": "Contraseña incorrecta"}), 401

    print("✅ Inicio de sesión exitoso")
    return jsonify({
        "message": "Inicio de sesión exitoso",
        "username": user["username"],
        "role": user["role"]
    }), 200
