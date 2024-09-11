from flask import Blueprint, request, jsonify
from models import db, User
from datetime import datetime

# Crear un blueprint para las rutas de la API
api_blueprint = Blueprint('api', __name__)

# Ruta para registrar un nuevo usuario
@api_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        # Validar que los datos obligatorios estén presentes
        if not all([data.get('nombres'), data.get('apellidos'), data.get('fecha_nacimiento'), data.get('password')]):
            return jsonify({'error': 'Todos los campos son requeridos'}), 400
        
        # Crear un nuevo usuario
        new_user = User(
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d'),
            password=data['password']  # Nota: es recomendable cifrar las contraseñas
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Usuario registrado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener la lista de usuarios registrados
@api_blueprint.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_list = [{
            'id': user.id,
            'nombres': user.nombres,
            'apellidos': user.apellidos
        } for user in users]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

