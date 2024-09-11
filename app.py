from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from models import db
from routes import api_blueprint

# Crear la aplicación Flask
app = Flask(_name_)

# Cargar la configuración desde config.py
app.config.from_object(Config)

# Inicializar CORS para permitir solicitudes desde el frontend (React, etc.)
CORS(app)

# Inicializar la base de datos
db.init_app(app)

# Registrar las rutas de la API (blueprint)
app.register_blueprint(api_blueprint)

# Crear las tablas en la base de datos (si no existen)
with app.app_context():
    db.create_all()

# Punto de entrada para ejecutar la aplicación
if _name_ == '_main_':
    # Inicia el servidor en modo de depuración (solo para desarrollo)
    app.run(debug=True, host='0.0.0.0')
