from decimal import Decimal, InvalidOperation
from flask import Blueprint, jsonify, request
from src.models import session
from src.models.productos import Productos
from src.models.categorias import Categorias
from src.models.proveedores import Proveedores
from src.utils.auth import token_required, rol_required

productos_bp = Blueprint('productos', __name__)


@productos_bp.route('/', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_productos():
    productos = Productos.get()
    productos_list = []
    for producto in productos:
        productos_list.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'codigo': producto.codigo,
            'stock': str(producto.stock),
            'stock_minimo': str(producto.stock_minimo),
            'stock_maximo': str(producto.stock_maximo) if producto.stock_maximo is not None else None,
            'precio': str(producto.precio),
            'estado': producto.estado,
            'fecha_creacion': producto.fecha_creacion.isoformat(),
            'categoria_id': producto.categoria_id,
            'categoria': producto.categoria.nombre if producto.categoria else None,
            'proveedor_id': producto.proveedor_id,
            'proveedor': producto.proveedor.nombre if producto.proveedor else None
        })
    return jsonify(productos_list), 200


@productos_bp.route('/<int:producto_id>', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_producto_by_id(producto_id):
    producto = Productos.get_by_id(producto_id)
    if producto:
        producto_data = {
            'id': producto.id,
            'nombre': producto.nombre,
            'codigo': producto.codigo,
            'stock': str(producto.stock),
            'stock_minimo': str(producto.stock_minimo),
            'stock_maximo': str(producto.stock_maximo) if producto.stock_maximo is not None else None,
            'precio': str(producto.precio),
            'estado': producto.estado,
            'fecha_creacion': producto.fecha_creacion.isoformat(),
            'categoria_id': producto.categoria_id,
            'categoria': producto.categoria.nombre if producto.categoria else None,
            'proveedor_id': producto.proveedor_id,
            'proveedor': producto.proveedor.nombre if producto.proveedor else None
        }
        return jsonify(producto_data), 200
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404


# Crear Productos
@productos_bp.route('/', methods=['POST'])
@token_required
@rol_required('Administrador')
def create_producto():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No se proporcionaron datos'}), 400

    # Validación del nombre
    nombre = data.get('nombre', '').strip()
    if not nombre:
        return jsonify({'message': 'El nombre del producto es obligatorio'}), 400
    
    # Validación del código
    codigo = data.get('codigo', '').strip().upper()
    if not codigo:
        return jsonify({'message': 'El código del producto es obligatorio'}), 400
    codigo_existente = Productos.get_by_codigo(codigo)
    if codigo_existente:
        return jsonify({'message': 'El código del producto ya existe'}), 400
    
    # Validación de categoría y proveedor
    categoria_id = data.get('categoria_id')
    if categoria_id is None:
        return jsonify({'message': 'El campo "categoria_id" es obligatorio'}), 400
    if not Categorias.get_by_id(categoria_id):
        return jsonify({'message': 'La categoría seleccionada no existe'}), 404

    proveedor_id = data.get('proveedor_id')
    if proveedor_id is None:
        return jsonify({'message': 'El campo "proveedor_id" es obligatorio'}), 400
    if not Proveedores.get_by_id(proveedor_id):
        return jsonify({'message': 'El proveedor seleccionado no existe'}), 404

    # Validación del stock
    try:
        stock = Decimal(str(data['stock']))
    except (KeyError, InvalidOperation, TypeError):
        return jsonify({'message': 'El campo "stock" es requerido y debe ser un número válido'}), 400
    if stock < 0:
        return jsonify({'message': 'El stock no puede ser negativo'}), 400
    
    # Validación del stock_minimo
    try:
        stock_minimo = Decimal(str(data['stock_minimo']))
    except (KeyError, InvalidOperation, TypeError):
        return jsonify({'message': 'El campo "stock_minimo" es requerido y debe ser un número válido'}), 400
    if stock_minimo < 0:
        return jsonify({'message': 'El stock_minimo no puede ser menor a cero'}), 400
    
    # Validación del stock_maximo
    valor_stock_maximo = data.get('stock_maximo')
    if valor_stock_maximo in [None, '']:
        stock_maximo = None
    else:
        try:
            stock_maximo = Decimal(str(valor_stock_maximo))
        except (InvalidOperation, TypeError):
            return jsonify({'message': 'El stock_maximo debe ser un número válido'}), 400

        if stock_maximo < 0:
            return jsonify({'message': 'El stock_maximo no puede ser menor a cero'}), 400

        if stock_maximo <= stock_minimo:
            return jsonify({'message': 'El stock_maximo debe ser mayor que el stock_minimo'}), 400

    # Validación del precio
    try:
        precio = Decimal(str(data['precio']))
    except (KeyError, InvalidOperation, TypeError):
        return jsonify({'message': 'El campo "precio" es requerido y debe ser un número válido'}), 400
    if precio <= 0:
        return jsonify({'message': 'El precio debe ser mayor que cero'}), 400
    
    # Validación del estado
    estado = data.get('estado', True)
    if isinstance(estado, str):
        if estado == '1':
            estado = True
        elif estado == '0':
            estado = False
        else:
            return jsonify({'message': 'El estado debe ser válido (1 o 0)'}), 400
    elif not isinstance(estado, bool):
        return jsonify({'message': 'El estado debe ser un valor booleano'}), 400

    try:
        producto = Productos(
            nombre=nombre,
            codigo=codigo,
            stock=stock,
            stock_minimo=stock_minimo,
            stock_maximo=stock_maximo,
            precio=precio,
            estado=estado,
            categoria_id=categoria_id,
            proveedor_id=proveedor_id
        )
        producto.save()
        return jsonify({'message': 'Producto creado exitosamente', 'producto': producto.to_dict()}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Error al crear el producto', 'error': str(e)}), 500


# Actualizar Producto
@productos_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('Administrador')
def update_producto(id):
    producto = Productos.get_by_id(id)
    if not producto:
        return jsonify({'message': 'Producto no encontrado'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400
    
    # Validación del nombre
    nombre = data.get('nombre', producto.nombre).strip()
    if not nombre:
        return jsonify({'message': 'El nombre del producto es obligatorio'}), 400
    
    # Validación del código
    codigo = data.get('codigo', producto.codigo).strip().upper()
    if not codigo:
        return jsonify({'message': 'El código del producto es obligatorio'}), 400
    codigo_existente = Productos.get_by_codigo(codigo)
    if codigo_existente and codigo_existente.id != producto.id:
        return jsonify({'message': 'El código del producto ya existe'}), 400

    # Categoría y Proveedor
    categoria_id = data.get('categoria_id', producto.categoria_id)
    if not Categorias.get_by_id(categoria_id):
        return jsonify({'message': 'La categoría seleccionada no existe'}), 404

    proveedor_id = data.get('proveedor_id', producto.proveedor_id)
    if not Proveedores.get_by_id(proveedor_id):
        return jsonify({'message': 'El proveedor seleccionado no existe'}), 404
        
    # Validación del stock
    try:
        stock = Decimal(str(data.get('stock', producto.stock)))
    except (InvalidOperation, TypeError):
        return jsonify({'message': 'El stock debe ser un número válido'}), 400
    if stock < 0:
        return jsonify({'message': 'El stock no puede ser negativo'}), 400
    
    # Validación del stock_minimo
    try:
        stock_minimo = Decimal(str(data.get('stock_minimo', producto.stock_minimo)))
    except (InvalidOperation, TypeError):
        return jsonify({'message': 'El stock_minimo debe ser un número válido'}), 400
    if stock_minimo < 0:
        return jsonify({'message': 'El stock_minimo no puede ser menor a cero'}), 400

    # Validación del stock_maximo
    valor_stock_maximo = data.get('stock_maximo', producto.stock_maximo)
    if valor_stock_maximo in [None, '']:
        stock_maximo = None
    else:
        try:
            stock_maximo = Decimal(str(valor_stock_maximo))
        except (InvalidOperation, TypeError):
            return jsonify({'message': 'El stock_maximo debe ser un número válido'}), 400
        if stock_maximo < 0:
            return jsonify({'message': 'El stock_maximo no puede ser menor a cero'}), 400
        if stock_maximo <= stock_minimo:
            return jsonify({'message': 'El stock_maximo debe ser mayor que el stock_minimo'}), 400
    
    # Validación del precio
    try:
        precio = Decimal(str(data.get('precio', producto.precio)))
    except (InvalidOperation, TypeError):
        return jsonify({'message': 'El precio debe ser un número válido'}), 400
    if precio <= 0:
        return jsonify({'message': 'El precio debe ser mayor que cero'}), 400

    if 'estado' in data:
        estado_val = data.get('estado')
        if isinstance(estado_val, str):
            producto.estado = estado_val.lower() in ['1', 'true', 'activo']
        elif isinstance(estado_val, (int, bool)):
            producto.estado = bool(estado_val)

    producto.nombre = nombre
    producto.codigo = codigo
    producto.stock = stock
    producto.stock_minimo = stock_minimo
    producto.stock_maximo = stock_maximo
    producto.precio = precio
    producto.categoria_id = categoria_id
    producto.proveedor_id = proveedor_id

    try:
        producto.save()
        return jsonify({'message': 'Producto actualizado exitosamente', 'producto': producto.to_dict()}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Error al actualizar el producto', 'error': str(e)}), 500


# Eliminar Producto
@productos_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('Administrador')
def delete_producto(id):
    producto = Productos.get_by_id(id)
    if not producto:
        return jsonify({'message': 'Producto no encontrado'}), 404

    try:
        producto.delete()
        return jsonify({'message': 'Producto eliminado exitosamente'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'No se pudo eliminar el producto (puede tener movimientos o facturas asociadas)',
            'error': str(e)
        }), 500