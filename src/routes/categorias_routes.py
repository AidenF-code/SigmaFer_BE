from flask import Blueprint, jsonify, request
from sqlalchemy import text
from src.models import engine, session
from src.models.categorias import Categorias
from src.utils.auth import token_required, rol_required

categorias_bp = Blueprint('categorias', __name__)

# Asegurar que la columna estado exista en MySQL
def _asegurar_columna_estado():
    try:
        with engine.connect() as conn:
            res = conn.execute(text("SHOW COLUMNS FROM categorias LIKE 'estado'")).fetchone()
            if not res:
                conn.execute(text("ALTER TABLE categorias ADD COLUMN estado VARCHAR(20) DEFAULT 'Activo'"))
                conn.commit()
    except Exception as e:
        print("Aviso al verificar columna estado en categorias:", e)

_asegurar_columna_estado()


@categorias_bp.route('/', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_categorias():
    categorias = Categorias.get()
    return jsonify([cat.to_dict() for cat in categorias]), 200


@categorias_bp.route('/<int:categoria_id>', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_categoria_by_id(categoria_id):
    categoria = Categorias.get_by_id(categoria_id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404
    return jsonify(categoria.to_dict()), 200


# Crear Categoría
@categorias_bp.route('/', methods=['POST'])
@token_required
@rol_required('Administrador')
def create_categoria():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No se proporcionaron datos'}), 400

    nombre = data.get('nombre', '').strip()
    estado = data.get('estado', 'Activo').strip() or 'Activo'

    if not nombre:
        return jsonify({'message': 'El campo "nombre" es requerido'}), 400

    existente = Categorias.get_by_nombre(nombre)
    if existente:
        return jsonify({'message': 'Ya existe una categoría con ese nombre'}), 400

    categoria = Categorias(nombre=nombre, estado=estado)
    categoria.save()
    return jsonify({'message': 'Categoría creada exitosamente', 'categoria': categoria.to_dict()}), 201


# Actualizar Categoría
@categorias_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('Administrador')
def update_categoria(id):
    categoria = Categorias.get_by_id(id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400

    nombre = data.get('nombre', '').strip()
    estado = data.get('estado', categoria.estado or 'Activo').strip()

    if not nombre:
        return jsonify({'message': 'El campo "nombre" es requerido'}), 400

    existente = Categorias.get_by_nombre(nombre)
    if existente and existente.id != id:
        return jsonify({'message': 'Ya existe otra categoría con ese nombre'}), 400

    categoria.nombre = nombre
    categoria.estado = estado
    categoria.save()
    return jsonify({'message': 'Categoría actualizada exitosamente', 'categoria': categoria.to_dict()}), 200


# Alternar Estado (Activo / Inactivo)
@categorias_bp.route('/<int:id>/toggle_estado', methods=['PATCH', 'POST'])
@token_required
@rol_required('Administrador')
def toggle_estado(id):
    categoria = Categorias.get_by_id(id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404

    nuevo_estado = 'Inactivo' if (categoria.estado or 'Activo') == 'Activo' else 'Activo'
    categoria.estado = nuevo_estado
    categoria.save()
    return jsonify({'message': f'Estado cambiado a {nuevo_estado}', 'categoria': categoria.to_dict()}), 200


# Eliminar Categoría
@categorias_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('Administrador')
def delete_categoria(id):
    categoria = Categorias.get_by_id(id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404

    try:
        categoria.delete()
        return jsonify({'message': 'Categoría eliminada exitosamente'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'No se puede eliminar la categoría (puede tener productos asociados)',
            'error': str(e)
        }), 500
