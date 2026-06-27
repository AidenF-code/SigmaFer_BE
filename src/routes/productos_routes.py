from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from src.models.productos import Productos


productos_bp = Blueprint('productos', __name__)


@productos_bp.route('/', methods=['GET'])
def get_productos():
    productos = Productos.get()
    productos_list = []
    for producto in productos:
        productos_list.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'codigo': producto.codigo,
            'stock': producto.stock,
            'stock_minimo': producto.stock_minimo,
            'stock_maximo': producto.stock_maximo,
            'precio': str(producto.precio),
            'estado': producto.estado,
            'fecha_creacion': producto.fecha_creacion.isoformat(),
            'categoria_id': producto.categoria_id,
            'proveedor_id': producto.proveedor_id
        })
    return jsonify(productos_list), 200


@productos_bp.route('/<int:producto_id>', methods=['GET'])
def get_producto_by_id(producto_id):
    producto = Productos.get_by_id(producto_id)
    if producto:
        producto_data = {
            'id': producto.id,
            'nombre': producto.nombre,
            'codigo': producto.codigo,
            'stock': producto.stock,
            'stock_minimo': producto.stock_minimo,
            'stock_maximo': producto.stock_maximo,
            'precio': str(producto.precio),
            'estado': producto.estado,
            'fecha_creacion': producto.fecha_creacion.isoformat(),
            'categoria_id': producto.categoria_id,
            'proveedor_id': producto.proveedor_id
        }
        return jsonify(producto_data), 200
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404



# Crear Productos
@productos_bp.route('/', methods=['POST'])
def create_producto():
    data = request.get_json()
    #Validacion de datos requeridos
    #Validacion del nombre
    nombre = data.get('nombre', '').strip()
    if not nombre:
        return jsonify({'message': 'El nombre del producto es obligatorio'}), 400
    
    #validacion del codigo
    codigo = data.get('codigo', '').strip().upper()
    if not codigo:
        return jsonify({'message': 'El codigo del producto es obligatorio'}), 400
    codigo_existente = Productos.get_by_codigo(codigo)
    if codigo_existente:
        return jsonify({'message': 'El codigo del producto ya existe'}), 400
    
    #Validacion del stock
    try:
        stock = Decimal(data['stock'])
    except KeyError:
        return jsonify({'message': 'El campo "stock" es requerido'}), 400
    except (InvalidOperation, TypeError):
        return jsonify({'message': 'El stock debe ser un número válido'}), 400
    if stock < 0:
        return jsonify({'message': 'El stock no puede ser negativo'}), 400
    
    #Validacion del stock_minimo
    try:
        stock_minimo = Decimal(data['stock_minimo'])
    except KeyError:
        return jsonify({'message': 'El campo "stock_minimo" es requerido'}), 400
    except (InvalidOperation, TypeError):
        return jsonify({'message': 'El stock_minimo debe ser un número válido'}), 400
    if stock_minimo < 0:
        return jsonify({'message': 'El stock_minimo no puede ser menor a cero'}), 400
    
    #Validacion del stock_maximo
    try:
        stock_maximo = Decimal(data['stock_maximo'])
    except KeyError:
        return jsonify({'message': 'El campo "stock_maximo" es requerido'}), 400
    except (InvalidOperation, TypeError):
        return jsonify({'message': 'El stock_maximo debe ser un número válido'}), 400
    if stock_maximo < 0:
        return jsonify({'message': 'El stock_maximo no puede ser menor a cero'}), 400
    if stock_maximo < stock_minimo:
        return jsonify({'message': 'El stock_maximo no puede ser menor que el stock_minimo'}), 400

    # Validación del precio
    try:
        precio = Decimal(data['precio'])
    except KeyError:
        return jsonify({'message': 'El campo "precio" es requerido'}), 400
    except (InvalidOperation, TypeError):
        return jsonify({'message': 'El precio debe ser un número válido'}), 400
    if precio <= 0:
        return jsonify({'message': 'El precio debe ser mayor que cero'}), 400
    
    #Elementos requeridos para crear un producto
    producto = Productos(
        nombre=nombre,
        codigo=codigo,
        stock=stock,
        stock_minimo=stock_minimo,
        stock_maximo=stock_maximo,
        precio=precio,
        categoria_id=data['categoria_id'],
        proveedor_id=data['proveedor_id']
    )
   
    # Guardar el producto en la base de datos
    producto.save()
    return jsonify({'message': 'Producto creado exitosamente', 'producto': producto.to_dict()}), 201 #Respuesta exitosa


# Actualizar Producto
@productos_bp.route('/<int:id>', methods=['PUT'])
def update_producto(id):
    producto = Productos.get_by_id(id) #Busca el producto por su ID

    if not producto:
        return jsonify({'message': 'Producto no encontrado'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400
    
    #Validacion del nombre
    nombre = data.get('nombre', '').strip()
    if not nombre:
        return jsonify({'message': 'El nombre del producto es obligatorio'}), 400
    
    #validacion del codigo
    codigo = data.get('codigo', '').strip().upper()
    if not codigo:
        return jsonify({'message': 'El codigo del producto es obligatorio'}), 400
    codigo_existente = Productos.get_by_codigo(codigo)
    if codigo_existente and codigo_existente.id != producto.id:
        return jsonify({'message': 'El código del producto ya existe'}), 400
        
    #Validacion del stock
    try:
        stock = Decimal(data['stock'])
    except KeyError:
        return jsonify({'message': 'El campo "stock" es requerido'}), 400
    except (InvalidOperation, TypeError):
        return jsonify({'message': 'El stock debe ser un número válido'}), 400
    if stock < 0:
        return jsonify({'message': 'El stock no puede ser negativo'}), 400
    
    #Validacion del stock_minimo
    try:
        stock_minimo = Decimal(data['stock_minimo'])
    except KeyError:
        return jsonify({'message': 'El campo "stock_minimo" es requerido'}), 400
    except (InvalidOperation, TypeError):
        return jsonify({'message': 'El stock_minimo debe ser un número válido'}), 400
    if stock_minimo < 0:
        return jsonify({'message': 'El stock_minimo no puede ser menor a cero'}), 400

     #Validacion del stock_maximo
    try:
        stock_maximo = Decimal(data['stock_maximo'])
    except KeyError:
        return jsonify({'message': 'El campo "stock_maximo" es requerido'}), 400
    except (InvalidOperation, TypeError):
        return jsonify({'message': 'El stock_maximo debe ser un número válido'}), 400
    if stock_maximo < 0:
        return jsonify({'message': 'El stock_maximo no puede ser menor a cero'}), 400
    if stock_maximo < stock_minimo:
        return jsonify({'message': 'El stock_maximo no puede ser menor que el stock_minimo'}), 400
    
     # Validación del precio
    try:
        precio = Decimal(data['precio'])
    except KeyError:
        return jsonify({'message': 'El campo "precio" es requerido'}), 400
    except (InvalidOperation, TypeError):
        return jsonify({'message': 'El precio debe ser un número válido'}), 400
    if precio <= 0:
        return jsonify({'message': 'El precio debe ser mayor que cero'}), 400

    #Actualiza los campos del producto con los nuevos valores
    producto.nombre = nombre
    producto.codigo = codigo
    producto.stock = stock
    producto.stock_minimo = stock_minimo
    producto.stock_maximo = stock_maximo
    producto.precio = precio
    producto.categoria_id = data['categoria_id']
    producto.proveedor_id = data['proveedor_id']


    producto.save()
    return jsonify({'message': 'Producto actualizado exitosamente', 'producto': producto.to_dict()}), 200