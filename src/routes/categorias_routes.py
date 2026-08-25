from flask import Blueprint, jsonify, request
from src.models.categorias import Categorias
from src.utils.auth import token_required, rol_required

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_categorias():
    categorias = Categorias.get()
    categorias_list = []
    for categoria in categorias:
        categorias_list.append({
            'id': categoria.id,
            'nombre': categoria.nombre,
        })
    return jsonify(categorias_list), 200

@categorias_bp.route('/<int:categoria_id>', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_categoria_by_id(categoria_id):
    categoria = Categorias.get_by_id(categoria_id)
    if categoria:
        categoria_data = {
            'id': categoria.id,
            'nombre': categoria.nombre,
        }
        return jsonify(categoria_data), 200
    else:
        return jsonify({'message': 'Categoría no encontrada'}), 404
    
@categorias_bp.route('/', methods=['POST'])
@token_required
@rol_required('Administrador')
def create_categoria():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No se proporcionaron datos'}), 400

    nombre = data.get('nombre', '').strip()

    if not nombre:
        return jsonify({'message': 'El campo "nombre" es requerido'}), 400

    existente = Categorias.get_by_nombre(nombre)
    if existente:
        return jsonify({'message': 'Ya existe una categoría con ese nombre'}), 400

    categoria = Categorias(nombre=nombre)
    categoria.save()
    return jsonify({'message': 'Categoría creada exitosamente', 'categoria': categoria.to_dict()}), 201

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

    if not nombre:
        return jsonify({'message': 'El campo "nombre" es requerido'}), 400

    existente = Categorias.get_by_nombre(nombre)
    if existente and existente.id != id:
        return jsonify({'message': 'Ya existe otra categoría con ese nombre'}), 400

    categoria.nombre = nombre
    categoria.save()
    return jsonify({'message': 'Categoría actualizada exitosamente', 'categoria': categoria.to_dict()}), 200

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
        from src.models import session
        session.rollback()
        return jsonify({
            'message': 'No se puede eliminar la categoría (puede tener productos asociados)',
            'error': str(e)
        }), 500
