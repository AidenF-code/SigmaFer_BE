from flask import Blueprint, jsonify, request
from src.models.rol import Roles

roles_bp = Blueprint('roles', __name__)

@roles_bp.route('/', methods=['GET'])
def get_roles():
    roles = Roles.get()
    roles_list = []
    for rol in roles:
        roles_list.append({
            'id': rol.id,
            'nombre': rol.nombre,
        })
    return jsonify(roles_list), 200

@roles_bp.route('/<int:rol_id>', methods=['GET'])
def get_rol_by_id(rol_id):
    rol = Roles.get_by_id(rol_id)
    if rol:
        rol_data = {
            'id': rol.id,
            'nombre': rol.nombre,
        }
        return jsonify(rol_data), 200
    else:
        return jsonify({'message': 'Rol no encontrado'}), 404
    

# Crear Rol    
@roles_bp.route('/', methods=['POST'])
def create_rol():
    data = request.get_json()
    nombre = data.get('nombre', '').strip()

    if not nombre:
        return jsonify({'message': 'El campo "nombre" es requerido'}), 400

    rol = Roles(nombre=nombre)
    rol.save()
    return jsonify({'message': 'Rol creado exitosamente', 'rol': rol.to_dict()}), 201


#Actualizar Rol
@roles_bp.route('/<int:id>', methods=['PUT'])
def update_rol(id):
    rol = Roles.get_by_id(id)
    if not rol:
        return jsonify({'message': 'Rol no encontrado'}), 404

    data = request.get_json()
    nombre = data.get('nombre', '').strip()

    if not nombre:
        return jsonify({'message': 'El campo "nombre" es requerido'}), 400

    rol.nombre = nombre

    rol.save()
    return jsonify({'message': 'Rol actualizado exitosamente', 'rol': rol.to_dict()}), 200