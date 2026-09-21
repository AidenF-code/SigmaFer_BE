from decimal import Decimal, InvalidOperation
from flask import Blueprint, jsonify, request
from src.models import session
from src.models.orden_compra import OrdenCompra
from src.models.detalle_oc import DetalleOC
from src.models.proveedores import Proveedores
from src.models.usuarios import Usuarios
from src.models.productos import Productos
from src.utils.auth import token_required, rol_required

ordenes_compra_bp = Blueprint('ordenes_compra', __name__)


# =========================================================
# SIGUIENTE NÚMERO DE ORDEN DE COMPRA
# =========================================================

@ordenes_compra_bp.route('/siguiente_numero', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_siguiente_numero_oc():
    numero = OrdenCompra.generar_numero_orden()
    return jsonify({'numero_orden': numero}), 200


# =========================================================
# OBTENER TODAS LAS ÓRDENES DE COMPRA
# =========================================================

@ordenes_compra_bp.route('/', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_ordenes():
    ordenes = OrdenCompra.get()
    result = []
    for orden in ordenes:
        result.append({
            'id': orden.id,
            'numero_orden': orden.numero_orden,
            'fecha_creacion': orden.fecha_creacion.isoformat(),
            'observaciones': orden.observaciones,
            'estado': orden.estado,
            'subtotal': str(orden.subtotal),
            'total': str(orden.total),
            'proveedor_id': orden.proveedor_id,
            'proveedor': orden.proveedor.nombre if orden.proveedor else None,
            'usuario_id': orden.usuario_id,
            'usuario': orden.usuario.nombre if orden.usuario else None
        })
    return jsonify(result), 200



# =========================================================
# OBTENER ORDEN POR ID (INCLUYE DETALLES)
# =========================================================

@ordenes_compra_bp.route('/<int:id>', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_orden(id):
    orden = OrdenCompra.get_by_id(id)
    if not orden:
        return jsonify({'message': 'Orden de compra no encontrada'}), 404

    detalles = DetalleOC.get_by_orden(id)
    detalles_list = []
    for d in detalles:
        detalles_list.append({
            'id': d.id,
            'producto_id': d.producto_id,
            'producto': d.producto.nombre if d.producto else None,
            'codigo_producto': d.producto.codigo if d.producto else None,
            'cantidad': d.cantidad,
            'valor_unitario': str(d.valor_unitario),
            'valor_total': str(d.valor_total)
        })

    return jsonify({
        'id': orden.id,
        'numero_orden': orden.numero_orden,
        'fecha_creacion': orden.fecha_creacion.isoformat(),
        'observaciones': orden.observaciones,
        'estado': orden.estado,
        'subtotal': str(orden.subtotal),
        'total': str(orden.total),
        'proveedor_id': orden.proveedor_id,
        'proveedor': orden.proveedor.nombre if orden.proveedor else None,
        'usuario_id': orden.usuario_id,
        'usuario': orden.usuario.nombre if orden.usuario else None,
        'detalles': detalles_list
    }), 200


# =========================================================
# CREAR ORDEN DE COMPRA
# =========================================================

@ordenes_compra_bp.route('/', methods=['POST'])
@token_required
@rol_required('Administrador')
def create_orden():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No se proporcionaron datos'}), 400

    proveedor_id = data.get('proveedor_id')
    if not proveedor_id or not Proveedores.get_by_id(proveedor_id):
        return jsonify({'message': 'El proveedor es obligatorio y debe existir'}), 400

    usuario_id = data.get('usuario_id')
    if not usuario_id or not Usuarios.get_by_id(usuario_id):
        primer_usuario = Usuarios.get_all() if hasattr(Usuarios, 'get_all') else Usuarios.get()
        if primer_usuario:
            usuario_id = primer_usuario[0].id
        else:
            return jsonify({'message': 'El usuario es obligatorio y debe existir'}), 400

    observaciones = (data.get('observaciones') or '').strip()
    numero_orden = (data.get('numero_orden') or '').strip()
    if not numero_orden:
        numero_orden = OrdenCompra.generar_numero_orden()

    try:
        orden = OrdenCompra(
            numero_orden=numero_orden,
            proveedor_id=proveedor_id,
            usuario_id=usuario_id,
            observaciones=observaciones
        )
        orden.save()

        # Si se envían detalles en la creación
        detalles_data = data.get('detalles', [])
        for item in detalles_data:
            producto_id = item.get('producto_id')
            cantidad = item.get('cantidad')
            valor_unitario = item.get('valor_unitario')

            if producto_id and cantidad and valor_unitario is not None:
                producto = Productos.get_by_id(producto_id)
                if producto:
                    detalle = DetalleOC(
                        orden_compra_id=orden.id,
                        producto_id=producto_id,
                        cantidad=int(cantidad),
                        valor_unitario=float(valor_unitario)
                    )
                    detalle.save()

        # Recalcular totales
        detalles = DetalleOC.get_by_orden(orden.id)
        orden.recalcular_totales(detalles)
        orden.save()

        return jsonify({
            'message': 'Orden de compra creada exitosamente',
            'orden': orden.to_dict()
        }), 201

    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Error al crear la orden de compra', 'error': str(e)}), 500



# =========================================================
# ACTUALIZAR ORDEN DE COMPRA
# =========================================================

@ordenes_compra_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('Administrador')
def update_orden(id):
    orden = OrdenCompra.get_by_id(id)
    if not orden:
        return jsonify({'message': 'Orden de compra no encontrada'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400

    if 'proveedor_id' in data:
        if not Proveedores.get_by_id(data['proveedor_id']):
            return jsonify({'message': 'El proveedor no existe'}), 404
        orden.proveedor_id = data['proveedor_id']

    if 'usuario_id' in data:
        if not Usuarios.get_by_id(data['usuario_id']):
            return jsonify({'message': 'El usuario no existe'}), 404
        orden.usuario_id = data['usuario_id']

    if 'observaciones' in data:
        orden.observaciones = (data['observaciones'] or '').strip()

    if 'estado' in data:
        estado = data['estado']
        if estado in ['0', '1', 0, 1, True, False]:
            orden.estado = bool(int(estado))

    if 'detalles' in data:
        detalles_data = data.get('detalles', [])
        try:
            # Eliminar detalles previos
            detalles_previos = DetalleOC.get_by_orden(id)
            for d in detalles_previos:
                d.delete()

            # Insertar nuevos detalles
            for item in detalles_data:
                producto_id = item.get('producto_id')
                cantidad = item.get('cantidad')
                valor_unitario = item.get('valor_unitario')

                if producto_id and cantidad and valor_unitario is not None:
                    producto = Productos.get_by_id(producto_id)
                    if producto:
                        detalle = DetalleOC(
                            orden_compra_id=orden.id,
                            producto_id=producto_id,
                            cantidad=int(cantidad),
                            valor_unitario=float(valor_unitario)
                        )
                        detalle.save()

            # Recalcular totales
            detalles = DetalleOC.get_by_orden(orden.id)
            orden.recalcular_totales(detalles)
        except Exception as e:
            session.rollback()
            return jsonify({'message': 'Error al actualizar los productos de la orden de compra', 'error': str(e)}), 500

    try:
        orden.save()
        return jsonify({
            'message': 'Orden de compra actualizada exitosamente',
            'orden': orden.to_dict()
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Error al actualizar la orden de compra', 'error': str(e)}), 500


# =========================================================
# ELIMINAR ORDEN DE COMPRA
# =========================================================

@ordenes_compra_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('Administrador')
def delete_orden(id):
    orden = OrdenCompra.get_by_id(id)
    if not orden:
        return jsonify({'message': 'Orden de compra no encontrada'}), 404

    try:
        detalles = DetalleOC.get_by_orden(id)
        for d in detalles:
            d.delete()
        orden.delete()
        return jsonify({'message': 'Orden de compra eliminada exitosamente'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Error al eliminar la orden de compra', 'error': str(e)}), 500


# =========================================================
# AGREGAR DETALLE A UNA ORDEN DE COMPRA
# =========================================================

@ordenes_compra_bp.route('/<int:orden_id>/detalles', methods=['POST'])
@token_required
@rol_required('Administrador')
def add_detalle_orden(orden_id):
    orden = OrdenCompra.get_by_id(orden_id)
    if not orden:
        return jsonify({'message': 'Orden de compra no encontrada'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400

    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad')
    valor_unitario = data.get('valor_unitario')

    if not producto_id or not Productos.get_by_id(producto_id):
        return jsonify({'message': 'El producto es obligatorio y debe existir'}), 400

    try:
        cantidad = int(cantidad)
        valor_unitario = Decimal(str(valor_unitario))
    except (ValueError, InvalidOperation, TypeError):
        return jsonify({'message': 'Cantidad y valor unitario deben ser numéricos válidos'}), 400

    if cantidad <= 0 or valor_unitario < 0:
        return jsonify({'message': 'Cantidad debe ser > 0 y valor unitario >= 0'}), 400

    try:
        detalle = DetalleOC(
            orden_compra_id=orden.id,
            producto_id=producto_id,
            cantidad=cantidad,
            valor_unitario=valor_unitario
        )
        detalle.save()

        detalles = DetalleOC.get_by_orden(orden.id)
        orden.recalcular_totales(detalles)
        orden.save()

        return jsonify({
            'message': 'Detalle agregado exitosamente',
            'detalle': detalle.to_dict(),
            'orden': orden.to_dict()
        }), 201

    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Error al agregar detalle', 'error': str(e)}), 500


# =========================================================
# ELIMINAR DETALLE DE ORDEN DE COMPRA
# =========================================================

@ordenes_compra_bp.route('/detalles/<int:detalle_id>', methods=['DELETE'])
@token_required
@rol_required('Administrador')
def delete_detalle_orden(detalle_id):
    detalle = DetalleOC.get_by_id(detalle_id)
    if not detalle:
        return jsonify({'message': 'Detalle no encontrado'}), 404

    orden_id = detalle.orden_compra_id
    try:
        detalle.delete()
        orden = OrdenCompra.get_by_id(orden_id)
        if orden:
            detalles = DetalleOC.get_by_orden(orden_id)
            orden.recalcular_totales(detalles)
            orden.save()

        return jsonify({'message': 'Detalle eliminado exitosamente'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Error al eliminar detalle', 'error': str(e)}), 500
