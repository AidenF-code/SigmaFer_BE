from flask import Blueprint, jsonify, request
from sqlalchemy import text
from src.models import engine, session
from src.models.rol import Roles
from src.utils.auth import token_required, rol_required

roles_bp = Blueprint('roles', __name__)

# Asegurar que la columna permisos exista en MySQL
def _asegurar_columna_permisos():
    try:
        with engine.connect() as conn:
            res = conn.execute(text("SHOW COLUMNS FROM rol LIKE 'permisos'")).fetchone()
            if not res:
                conn.execute(text("ALTER TABLE rol ADD COLUMN permisos JSON DEFAULT NULL"))
                conn.commit()
    except Exception as e:
        print("Aviso al verificar columna permisos:", e)

_asegurar_columna_permisos()


@roles_bp.route('/', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_roles():
    roles = Roles.get()
    return jsonify([rol.to_dict() for rol in roles]), 200


@roles_bp.route('/<int:rol_id>', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_rol_by_id(rol_id):
    rol = Roles.get_by_id(rol_id)
    if not rol:
        return jsonify({'message': 'Rol no encontrado'}), 404
    return jsonify(rol.to_dict()), 200


# Crear Rol    
@roles_bp.route('/', methods=['POST'])
@token_required
@rol_required('Administrador')
def create_rol():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No se proporcionaron datos'}), 400

    nombre = data.get('nombre', '').strip()
    permisos = data.get('permisos', {})

    if not nombre:
        return jsonify({'message': 'El campo "nombre" es requerido'}), 400

    existente = Roles.get_by_nombre(nombre)
    if existente:
        return jsonify({'message': 'Ya existe un rol con ese nombre'}), 400

    rol = Roles(nombre=nombre, permisos=permisos)
    rol.save()
    return jsonify({'message': 'Rol creado exitosamente', 'rol': rol.to_dict()}), 201


# Actualizar Rol
@roles_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('Administrador')
def update_rol(id):
    rol = Roles.get_by_id(id)
    if not rol:
        return jsonify({'message': 'Rol no encontrado'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400

    nombre = data.get('nombre', '').strip()

    if not nombre:
        return jsonify({'message': 'El campo "nombre" es requerido'}), 400

    existente = Roles.get_by_nombre(nombre)
    if existente and existente.id != id:
        return jsonify({'message': 'Ya existe otro rol con ese nombre'}), 400

    rol.nombre = nombre
    if 'permisos' in data:
        rol.permisos = data['permisos']

    rol.save()
    return jsonify({'message': 'Rol actualizado exitosamente', 'rol': rol.to_dict()}), 200


# Eliminar Rol
@roles_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('Administrador')
def delete_rol(id):
    rol = Roles.get_by_id(id)
    if not rol:
        return jsonify({'message': 'Rol no encontrado'}), 404

    try:
        rol.delete()
        return jsonify({'message': 'Rol eliminado exitosamente'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'No se puede eliminar el rol (puede tener usuarios asignados)',
            'error': str(e)
        }), 500