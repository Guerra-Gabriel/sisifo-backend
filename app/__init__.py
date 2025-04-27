from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from app.routes import main
from app.models import init_db  

def create_app():
    app = Flask(__name__)

    # Configuración de conexión a MySQL
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'sisifo_login'
    app.config['MYSQL_PASSWORD'] = 'Lamichabot2025#'
    app.config['MYSQL_DB'] = 'sisifo_auth'

    # Inicializar extensión MySQL
    init_db(app)

    # Configurar CORS para permitir solicitudes desde el frontend
   # CORS(app, origins=[
    #    "http://localhost:5173",
     #   "https://www.videotopdf.com"
    #])
# Habilitar CORS en toda la app
    CORS(app, resources={r"/api/*": {"origins": "*"}}) 
    # Registrar blueprints
    app.register_blueprint(main, url_prefix="/api")

    return app
