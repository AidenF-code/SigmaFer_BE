from flask import Blueprint, jsonify, request
from src.models.categorias import Categorias

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/', methods=['GET'])
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
def create_categoria():
    data = request.get_json()
    nombre = data.get('nombre', '').strip()

    if not nombre:
        return jsonify({'message': 'El campo "nombre" es requerido'}), 400

    categoria = Categorias(nombre=nombre)
    categoria.save()
    return jsonify({'message': 'Categoría creada exitosamente', 'categoria': categoria.to_dict()}), 201

@categorias_bp.route('/<int:id>', methods=['PUT'])
def update_categoria(id):
    categoria = Categorias.get_by_id(id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404

    data = request.get_json()
    nombre = data.get('nombre', '').strip()

    if not nombre:
        return jsonify({'message': 'El campo "nombre" es requerido'}), 400

    categoria.nombre = nombre

    categoria.save()
    return jsonify({'message': 'Categoría actualizada exitosamente', 'categoria': categoria.to_dict()}), 200