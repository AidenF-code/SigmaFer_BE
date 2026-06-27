from flask import Blueprint, jsonify, request
from src.models.usuarios import Usuarios

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])#Todos los usuarios
def get_usuarios():
    usuarios = Usuarios.get()
    usuarios_list = []
    for usuario in usuarios:
        usuarios_list.append({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'identificacion': usuario.identificacion,
            'correo': usuario.correo,
            'estado': usuario.estado,
            'fecha_creacion': usuario.fecha_creacion.isoformat(),
            'rol_id': usuario.rol_id
        })
    return jsonify(usuarios_list), 200



@usuarios_bp.route('/<int:id>', methods=['GET']) #Usuarios por ID
def get_usuario(id):
    usuario = Usuarios.get_by_id(id)
    if usuario:
        usuario_data = {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'identificacion': usuario.identificacion,
            'correo': usuario.correo,
            'estado': usuario.estado,
            'fecha_creacion': usuario.fecha_creacion.isoformat(),
            'rol_id': usuario.rol_id
        }
        return jsonify(usuario_data), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    

@usuarios_bp.route('/', methods=['POST']) #Crear usuarios
def create_usuario():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No se proporcionaron datos'}), 400

    # Validación de datos requeridos
    # Validación del campo "nombre"
    nombre = data.get('nombre', '').strip()
    if not nombre:
        return jsonify({'message': 'El campo "nombre" es obligatorio'}), 400
    
    # Validacion del campo "identificacion"
    identificacion =data.get('identificacion', '').strip()
    if not identificacion:
        return jsonify({'message': 'El campo "identificacion" es obligatorio'}), 400
    identificacion_existente =Usuarios.get_by_identificacion(identificacion)
    if identificacion_existente:
        return jsonify({'message': 'Ya existe un cliente con esa identificacion'}), 400
    
    # Validacion del campo  "correo"
    correo = data.get('correo', '').strip()
    if not correo:
        return jsonify({'message': 'El campo "correo" es obligatorio'}), 400
    correo_existente = Usuarios.get_by_correo(correo)
    if correo_existente:
        return jsonify({'message': 'Ya existe un cliente con esa correo'}), 400
    
    
 