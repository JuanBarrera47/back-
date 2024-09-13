from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mi_usuario:12345@localhost/registro_usuarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir el modelo de la tabla Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, nombres, apellidos, fecha_nacimiento, password):
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.password = password

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

@app.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    nuevo_usuario = Usuario(
        nombres=data['nombres'],
        apellidos=data['apellidos'],
        fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%d-%m-%Y'),
        password=data['password']
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuario registrado exitosamente"}), 201

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    resultado = [
        {"nombres": usuario.nombres, "apellidos": usuario.apellidos} for usuario in usuarios
    ]
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
