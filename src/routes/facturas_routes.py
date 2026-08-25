from decimal import Decimal, InvalidOperation
from flask import Blueprint, jsonify, request
from src.models import session

from src.models.clientes import Clientes
from src.models.usuarios import Usuarios
from src.models.metodo_pago import MetodoPago
from src.models.facturas import Facturas
from src.models.detalle_facturas import DetalleFacturas
from src.models.productos import Productos




facturas_bp = Blueprint(
    'facturas',
    __name__
)


# =========================================================
# OBTENER TODAS LAS FACTURAS
# =========================================================

@facturas_bp.route('/', methods=['GET'])
def get_facturas():

    try:

        facturas_list = Facturas.get()

        result = []

        for factura in facturas_list:

            result.append({

                'id': factura.id,

                'numero_factura':
                    factura.numero_factura,

                'fecha_emision':
                    factura.fecha_emision.isoformat() if factura.fecha_emision else None,

                'fecha':
                    factura.fecha_emision.strftime('%Y-%m-%d %H:%M') if factura.fecha_emision else '',

                'cliente':
                    factura.cliente.razon_social if factura.cliente else None,

                'cliente_id':
                    factura.cliente_id,

                'cliente_nit':
                    factura.cliente.numero_identificacion if factura.cliente else '',

                'cliente_contacto':
                    factura.cliente.nombre if factura.cliente else '',

                'cliente_direccion':
                    factura.cliente.direccion if factura.cliente else '',

                'cliente_telefono':
                    factura.cliente.telefono if factura.cliente else '',

                'cliente_correo':
                    factura.cliente.correo if factura.cliente else '',

                'vendedor':
                    factura.usuario.nombre if factura.usuario else None,


                'usuario_id':
                    factura.usuario_id,

                'metodo_pago':
                    factura.metodo_pago.nombre if factura.metodo_pago else None,

                'metodo_pago_id':
                    factura.metodo_pago_id,

                'subtotal':
                    str(factura.subtotal),

                'iva':
                    str(factura.iva),

                'total':
                    str(factura.total),

                'observaciones':
                    factura.observaciones,

                'estado_pago':
                    factura.estado_pago

            })

        return jsonify(result), 200



    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Error al obtener las facturas',
            'error': str(e)
        }), 500


# =========================================================
# OBTENER FACTURA POR ID
# =========================================================

@facturas_bp.route('/<int:factura_id>', methods=['GET'])
def get_factura_by_id(factura_id):

    factura = Facturas.get_by_id(
        factura_id
    )


    if not factura:

        return jsonify({
            'message': 'Factura no encontrada'
        }), 404


    result = {

        'id':
            factura.id,

        'numero_factura':
            factura.numero_factura,

        'fecha_emision':
            factura.fecha_emision.isoformat(),

        'subtotal':
            str(factura.subtotal),

        'iva':
            str(factura.iva),

        'total':
            str(factura.total),

        'observaciones':
            factura.observaciones,

        'estado_pago':
            factura.estado_pago,


        # Cliente

        'cliente_id':
            factura.cliente_id,

        'cliente':
            factura.cliente.razon_social,


        # Usuario / vendedor

        'usuario_id':
            factura.usuario_id,

        'vendedor':
            factura.usuario.nombre,


        # Método de pago

        'metodo_pago_id':
            factura.metodo_pago_id,

        'metodo_pago':
            factura.metodo_pago.nombre

    }


    return jsonify(result), 200

@facturas_bp.route('/siguiente_numero', methods=['GET'])
def get_siguiente_numero():
    numero = Facturas.generar_numero_factura()
    return jsonify({'numero_factura': numero}), 200


# =========================================================
# CREAR FACTURA
# =========================================================

@facturas_bp.route('/', methods=['POST'])
def create_factura():

    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Datos inválidos'
        }), 400

    # =====================================================
    # CLIENTE
    # =====================================================

    cliente_id = data.get('cliente_id')
    if cliente_id is None:
        return jsonify({'message': 'El cliente es obligatorio'}), 400

    cliente = Clientes.get_by_id(cliente_id)
    if not cliente:
        return jsonify({'message': 'El cliente no existe'}), 404

    if not cliente.estado:
        return jsonify({'message': 'El cliente se encuentra inactivo'}), 400

    # =====================================================
    # USUARIO / VENDEDOR
    # =====================================================

    usuario_id = data.get('usuario_id')
    if usuario_id is None:
        return jsonify({'message': 'El vendedor es obligatorio'}), 400

    usuario = Usuarios.get_by_id(usuario_id)
    if not usuario:
        return jsonify({'message': 'El usuario no existe'}), 404

    if not usuario.estado:
        return jsonify({'message': 'El usuario se encuentra inactivo'}), 400

    # =====================================================
    # MÉTODO DE PAGO
    # =====================================================

    metodo_pago_id = data.get('metodo_pago_id')
    if metodo_pago_id is None:
        return jsonify({'message': 'El método de pago es obligatorio'}), 400

    metodo_pago = MetodoPago.get_by_id(metodo_pago_id)
    if not metodo_pago:
        return jsonify({'message': 'El método de pago no existe'}), 404

    if not metodo_pago.estado:
        return jsonify({'message': 'El método de pago se encuentra inactivo'}), 400

    # =====================================================
    # OBSERVACIONES
    # =====================================================

    observaciones = (data.get('observaciones') or '').strip()

    # =====================================================
    # DETERMINAR ESTADO DE PAGO SEGÚN MÉTODO DE PAGO
    # (Efectivo -> Pagada automáticamente)
    # =====================================================
    es_efectivo = (metodo_pago.nombre or '').strip().lower() == 'efectivo'
    if es_efectivo:
        estado_pago = True
    elif 'estado_pago' in data:
        estado_pago = bool(int(data.get('estado_pago', 0))) if isinstance(data.get('estado_pago'), (int, str)) and str(data.get('estado_pago')).isdigit() else bool(data.get('estado_pago'))
    else:
        estado_pago = False

    # =====================================================
    # GENERAR CONSECUTIVO
    # =====================================================

    numero_factura = Facturas.generar_numero_factura()

    # =====================================================
    # CREAR FACTURA Y SUS DETALLES
    # =====================================================

    detalles_data = data.get('detalles', [])

    # Validar stock previo si hay detalles
    for item in detalles_data:
        p_id = item.get('producto_id')
        cant = int(item.get('cantidad', 0))
        if p_id and cant > 0:
            prod = Productos.get_by_id(p_id)
            if not prod:
                return jsonify({'message': f'Producto ID {p_id} no encontrado'}), 404
            stock_actual = prod.stock if prod.stock is not None else 0
            if stock_actual < cant:
                return jsonify({
                    'message': f'Stock insuficiente para "{prod.nombre}". Stock disponible: {stock_actual}'
                }), 400

    try:

        factura = Facturas(
            numero_factura=numero_factura,
            cliente_id=cliente.id,
            usuario_id=usuario.id,
            metodo_pago_id=metodo_pago.id,
            observaciones=observaciones,
            estado_pago=estado_pago
        )

        factura.save()

        # Guardar cada detalle y actualizar el stock del producto
        for item in detalles_data:
            p_id = item.get('producto_id')
            cant = int(item.get('cantidad', 0))
            v_unit = item.get('valor_unitario')
            iva_pct = item.get('iva_porcentaje', 19)

            if p_id and cant > 0:
                prod = Productos.get_by_id(p_id)
                if prod:
                    detalle = DetalleFacturas(
                        factura_id=factura.id,
                        producto_id=p_id,
                        cantidad=cant,
                        valor_unitario=Decimal(str(v_unit)),
                        iva_porcentaje=Decimal(str(iva_pct))
                    )
                    detalle.save()
                    stock_actual = prod.stock if prod.stock is not None else 0
                    prod.stock = max(0, stock_actual - cant)
                    prod.save()

        # Recalcular totales de la factura con sus detalles
        detalles = DetalleFacturas.get_by_factura(factura.id)
        if detalles:
            factura.recalcular_totales(detalles)
            factura.save()


        factura_dict = factura.to_dict()
        factura_dict['fecha_emision'] = factura.fecha_emision.isoformat()
        factura_dict['subtotal'] = str(factura.subtotal)
        factura_dict['iva'] = str(factura.iva)
        factura_dict['total'] = str(factura.total)

        return jsonify({
            'message': 'Factura creada exitosamente',
            'factura': factura_dict
        }), 201



    except Exception as e:

        session.rollback()

        return jsonify({

            'message':
                'Error al crear la factura',

            'error':
                str(e)

        }), 500


# =========================================================
# ACTUALIZAR FACTURA
# =========================================================

@facturas_bp.route('/<int:id>', methods=['PUT'])
def update_factura(id):

    factura = Facturas.get_by_id(id)
    if not factura:
        return jsonify({'message': 'Factura no encontrada'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400

    if 'cliente_id' in data and data['cliente_id'] is not None:
        cliente = Clientes.get_by_id(data['cliente_id'])
        if not cliente:
            return jsonify({'message': 'El cliente no existe'}), 404
        factura.cliente_id = cliente.id

    if 'usuario_id' in data and data['usuario_id'] is not None:
        usuario = Usuarios.get_by_id(data['usuario_id'])
        if not usuario:
            return jsonify({'message': 'El usuario no existe'}), 404
        factura.usuario_id = usuario.id

    if 'metodo_pago_id' in data and data['metodo_pago_id'] is not None:
        metodo_pago = MetodoPago.get_by_id(data['metodo_pago_id'])
        if not metodo_pago:
            return jsonify({'message': 'El método de pago no existe'}), 404
        factura.metodo_pago_id = metodo_pago.id

    if 'detalles' in data:
        detalles_data = data.get('detalles', [])
        
        # 1. Obtener detalles previos
        detalles_actuales = DetalleFacturas.get_by_factura(id)
        
        # 2. Devolver temporalmente el stock de los productos previos
        for d in detalles_actuales:
            prod = Productos.get_by_id(d.producto_id)
            if prod:
                stock_prev = prod.stock if prod.stock is not None else 0
                prod.stock = stock_prev + d.cantidad
                prod.save()

        # 3. Validar stock de los nuevos productos
        for item in detalles_data:
            p_id = item.get('producto_id')
            cant = int(item.get('cantidad', 0))
            if p_id and cant > 0:
                prod = Productos.get_by_id(p_id)
                if not prod:
                    session.rollback()
                    return jsonify({'message': f'Producto ID {p_id} no encontrado'}), 404
                stock_actual = prod.stock if prod.stock is not None else 0
                if stock_actual < cant:
                    session.rollback()
                    return jsonify({
                        'message': f'Stock insuficiente para "{prod.nombre}". Stock disponible: {stock_actual}'
                    }), 400

        # 4. Eliminar detalles anteriores de la base de datos
        for d in detalles_actuales:
            d.delete()

        # 5. Insertar nuevos detalles y descontar stock
        for item in detalles_data:
            p_id = item.get('producto_id')
            cant = int(item.get('cantidad', 0))
            v_unit = item.get('valor_unitario')
            iva_pct = item.get('iva_porcentaje', 19)

            if p_id and cant > 0:
                prod = Productos.get_by_id(p_id)
                if prod:
                    detalle = DetalleFacturas(
                        factura_id=factura.id,
                        producto_id=p_id,
                        cantidad=cant,
                        valor_unitario=Decimal(str(v_unit)),
                        iva_porcentaje=Decimal(str(iva_pct))
                    )
                    detalle.save()
                    stock_actual = prod.stock if prod.stock is not None else 0
                    prod.stock = max(0, stock_actual - cant)
                    prod.save()

        # 6. Recalcular totales
        detalles_nuevos = DetalleFacturas.get_by_factura(factura.id)
        if detalles_nuevos:
            factura.recalcular_totales(detalles_nuevos)

    try:
        factura.save()
        factura_dict = factura.to_dict()
        factura_dict['fecha_emision'] = factura.fecha_emision.isoformat() if hasattr(factura.fecha_emision, 'isoformat') else str(factura.fecha_emision)
        factura_dict['subtotal'] = str(factura.subtotal)
        factura_dict['iva'] = str(factura.iva)
        factura_dict['total'] = str(factura.total)

        return jsonify({
            'message': 'Factura actualizada exitosamente',
            'factura': factura_dict
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'Error al actualizar la factura',
            'error': str(e)
        }), 500



# =========================================================
# ELIMINAR / ANULAR FACTURA
# =========================================================

@facturas_bp.route('/<int:id>', methods=['DELETE'])
def delete_factura(id):
    factura = Facturas.get_by_id(id)
    if not factura:
        return jsonify({'message': 'Factura no encontrada'}), 404

    try:
        # Obtener detalles asociados
        detalles = DetalleFacturas.get_by_factura(id)
        # Devolver stock de los productos
        for detalle in detalles:
            producto = Productos.get_by_id(detalle.producto_id)
            if producto:
                producto.stock += detalle.cantidad
                producto.save()
            detalle.delete()

        factura.delete()
        return jsonify({'message': 'Factura eliminada exitosamente y stock restituido'}), 200

    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'Error al eliminar la factura',
            'error': str(e)
        }), 500