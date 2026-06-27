from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from src.models.detalle_facturas import DetalleFacturas
from src.models.facturas import Facturas
from src.models.productos import Productos

detalle_facturas_bp = Blueprint('detalle_facturas', __name__)

@detalle_facturas_bp.route('/', methods=['GET'])#Mostrar todos los detalles de facturas
def get_detalle_facturas():
    detalle_facturas_list = DetalleFacturas.get()
    result = []
    for detalle in detalle_facturas_list:
        result.append({
            'id': detalle.id,
            'factura_id': detalle.factura_id,
            'producto_id': detalle.producto_id,
            'cantidad': detalle.cantidad,
            'valor_unitario': str(detalle.valor_unitario),
            'subtotal': str(detalle.subtotal),
            'iva': str(detalle.iva),
            'iva_porcentaje': str(detalle.iva_porcentaje),
            'valor_total': str(detalle.valor_total)
        })
    return jsonify(result), 200

@detalle_facturas_bp.route('/<int:id>', methods=['GET'])#Mostrar detalle de factura por ID
def get_detalle_factura_by_id(id):
    detalle = DetalleFacturas.get_by_id(id)
    if detalle:
        result = {
            'id': detalle.id,
            'factura_id': detalle.factura_id,
            'producto_id': detalle.producto_id,
            'cantidad': detalle.cantidad,
            'valor_unitario': str(detalle.valor_unitario),
            'subtotal': str(detalle.subtotal),
            'iva': str(detalle.iva),
            'iva_porcentaje': str(detalle.iva_porcentaje),
            'valor_total': str(detalle.valor_total)
        }
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Detalle de factura no encontrado'}), 404
    

@detalle_facturas_bp.route('/factura/<int:factura_id>', methods=['GET'])#Mostrar detalles de factura por ID de factura
def get_detalle_facturas_by_factura(factura_id):

    factura = Facturas.get_by_id(factura_id)
    if not factura:
        return jsonify({'message': 'Factura no encontrada'}), 404
    
    detalles = DetalleFacturas.get_by_factura(factura_id)
    if not detalles:
        return jsonify({'message': f'La factura {factura.numero_factura} no tiene detalles registrados'}), 404
    
    result = []
    for detalle in detalles:
        result.append({
            'id': detalle.id,
            'factura_id': detalle.factura_id,
            'producto_id': detalle.producto_id,
            'cantidad': detalle.cantidad,
            'valor_unitario': str(detalle.valor_unitario),
            'subtotal': str(detalle.subtotal),
            'iva': str(detalle.iva),
            'iva_porcentaje': str(detalle.iva_porcentaje),
            'valor_total': str(detalle.valor_total)
        })
    return jsonify(result), 200



@detalle_facturas_bp.route('/', methods=['POST'])#Crear detalle de factura
def create_detalle_factura():

    data = request.get_json()

    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400

    # Obtener datos
    factura_id = data.get('factura_id')
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad')
    valor_unitario = data.get('valor_unitario')
    iva_porcentaje = data.get('iva_porcentaje')

    # Validar campos obligatorios
    if not factura_id:
        return jsonify({'message': 'La factura es obligatoria'}), 400

    if not producto_id:
        return jsonify({'message': 'El producto es obligatorio'}), 400

    if not cantidad:
        return jsonify({'message': 'La cantidad es obligatoria'}), 400

    if valor_unitario is None:
        return jsonify({'message': 'El valor unitario es obligatorio'}), 400

    if iva_porcentaje is None:
        return jsonify({'message': 'El porcentaje de IVA es obligatorio'}), 400

    # Verificar que exista la factura
    factura = Facturas.get_by_id(factura_id)

    if not factura:
        return jsonify({'message': 'Factura no encontrada'}), 404
    
    # Verificar que la factura no esté pagada
    if factura.estado_pago == True:
        return jsonify({
            'message': 'No se pueden agregar productos a una factura pagada'
        }), 400

    # Verificar que exista el producto
    producto = Productos.get_by_id(producto_id)

    if not producto:
        return jsonify({'message': 'Producto no encontrado'}), 404
    
    
    # Validar valores numéricos
    try:
        cantidad = int(cantidad)
        valor_unitario = Decimal(str(valor_unitario))
        iva_porcentaje = Decimal(str(iva_porcentaje))
    except (ValueError, InvalidOperation):
        return jsonify({
            'message': 'Los valores numéricos son inválidos'
        }), 400
    
    #validar stock del producto
    if producto.stock < cantidad:
        return jsonify({
            'message': 'Stock insuficiente'
        }), 400

    # Validaciones de negocio
    if cantidad <= 0:
        return jsonify({
            'message': 'La cantidad debe ser mayor que cero'
        }), 400

    if valor_unitario < 0:
        return jsonify({
            'message': 'El valor unitario no puede ser negativo'
        }), 400

    if iva_porcentaje < 0:
        return jsonify({
            'message': 'El porcentaje de IVA no puede ser negativo'
        }), 400

    # Crear detalle
    detalle_factura = DetalleFacturas(
        factura_id=factura_id,
        producto_id=producto_id,
        cantidad=cantidad,
        valor_unitario=valor_unitario,
        iva_porcentaje=iva_porcentaje
    )

    detalle_factura.save()
    producto.stock -= cantidad
    producto.save()

    # Recalcular totales de la factura
    detalles = DetalleFacturas.get_by_factura(factura_id)

    factura.recalcular_totales(detalles)

    factura.save()

    detalle_dict = detalle_factura.to_dict()
    detalle_dict['valor_unitario'] = str(detalle_factura.valor_unitario)
    detalle_dict['subtotal'] = str(detalle_factura.subtotal)
    detalle_dict['iva'] = str(detalle_factura.iva)
    detalle_dict['iva_porcentaje'] = str(detalle_factura.iva_porcentaje)
    detalle_dict['valor_total'] = str(detalle_factura.valor_total)

    return jsonify({
        'message': 'Detalle de factura creado exitosamente',
        'detalle_factura': detalle_dict
    }), 201



@detalle_facturas_bp.route('/<int:detalle_id>', methods=['PUT'])
def update_detalle_factura(detalle_id):

    # 1. Buscar detalle
    detalle = DetalleFacturas.get_by_id(detalle_id)

    if not detalle:
        return jsonify({'message': 'Detalle de factura no encontrado'}), 404

    # 2. Buscar factura (no se puede cambiar)
    factura = Facturas.get_by_id(detalle.factura_id)

    if not factura:
        return jsonify({'message': 'Factura no encontrada'}), 404

    # 3. Bloquear si está pagada
    if factura.estado_pago:
        return jsonify({
            'message': 'No se pueden modificar detalles de una factura pagada'
        }), 400

    # 4. Leer datos
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400

    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad')
    valor_unitario = data.get('valor_unitario')
    iva_porcentaje = data.get('iva_porcentaje')

    # 5. Validaciones obligatorias
    if not producto_id:
        return jsonify({'message': 'El producto es obligatorio'}), 400

    if cantidad is None:
        return jsonify({'message': 'La cantidad es obligatoria'}), 400

    if valor_unitario is None:
        return jsonify({'message': 'El valor unitario es obligatorio'}), 400

    if iva_porcentaje is None:
        return jsonify({'message': 'El IVA es obligatorio'}), 400

    # 6. Convertir tipos
    try:
        cantidad = int(cantidad)
        valor_unitario = Decimal(str(valor_unitario))
        iva_porcentaje = Decimal(str(iva_porcentaje))
    except (ValueError, InvalidOperation):
        return jsonify({'message': 'Valores numéricos inválidos'}), 400

    # 7. Validaciones de negocio
    if cantidad < 0:
        return jsonify({'message': 'La cantidad no puede ser negativa'}), 400

    if valor_unitario < 0:
        return jsonify({'message': 'El valor unitario no puede ser negativo'}), 400

    if iva_porcentaje < 0:
        return jsonify({'message': 'El IVA no puede ser negativo'}), 400

    # 8. Producto nuevo
    producto_nuevo = Productos.get_by_id(producto_id)

    if not producto_nuevo:
        return jsonify({'message': 'Producto no encontrado'}), 404

    # 9. Detectar cambio de producto
    producto_anterior = Productos.get_by_id(detalle.producto_id)

    cambio_producto = detalle.producto_id != producto_id

    
    # MISMO PRODUCTO
    
    if not cambio_producto:

        detalle.cantidad = cantidad
        detalle.valor_unitario = valor_unitario
        detalle.iva_porcentaje = iva_porcentaje

    # CAMBIO PRODUCTO
    
    else:

        # devolver stock del producto anterior
        producto_anterior.stock += detalle.cantidad
        producto_anterior.save()

        # validar stock del nuevo producto
        if producto_nuevo.stock < cantidad:
            return jsonify({'message': 'Stock insuficiente'}), 400

        # descontar stock nuevo
        producto_nuevo.stock -= cantidad
        producto_nuevo.save()

        # actualizar detalle
        detalle.producto_id = producto_id
        detalle.cantidad = cantidad
        detalle.valor_unitario = valor_unitario
        detalle.iva_porcentaje = iva_porcentaje

    # 10. Recalcular valores del detalle
    detalle.subtotal = detalle.cantidad * detalle.valor_unitario
    detalle.iva = detalle.subtotal * (detalle.iva_porcentaje / Decimal('100'))
    detalle.valor_total = detalle.subtotal + detalle.iva

    detalle.save()

    # 11. Recalcular factura
    detalles = DetalleFacturas.get_by_factura(factura.id)

    factura.recalcular_totales(detalles)

    factura.save()

    # 12. Respuesta
    detalle_dict = detalle.to_dict()
    detalle_dict['valor_unitario'] = str(detalle.valor_unitario)
    detalle_dict['subtotal'] = str(detalle.subtotal)
    detalle_dict['iva'] = str(detalle.iva)
    detalle_dict['iva_porcentaje'] = str(detalle.iva_porcentaje)
    detalle_dict['valor_total'] = str(detalle.valor_total)

    return jsonify({
        'message': 'Detalle actualizado correctamente',
        'detalle_factura': detalle_dict
    }), 200