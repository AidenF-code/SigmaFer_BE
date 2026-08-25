from decimal import Decimal, InvalidOperation
from flask import Blueprint, jsonify, request
from src.models import session
from src.models.documento_inventarios import DocumentoInventarios, TipoDocumento
from src.models.detalle_doc_inventario import DetalleDocInventario
from src.models.clientes import Clientes
from src.models.proveedores import Proveedores
from src.models.usuarios import Usuarios
from src.models.productos import Productos

documentos_inventario_bp = Blueprint('documentos_inventario', __name__)


# =========================================================
# OBTENER TODOS LOS DOCUMENTOS DE INVENTARIO
# =========================================================

@documentos_inventario_bp.route('/', methods=['GET'])
def get_documentos():
    import unicodedata
    def clean_txt(t):
        if not t: return ''
        return unicodedata.normalize('NFKD', str(t)).encode('ASCII', 'ignore').decode('utf-8').lower()

    tipo_filtro = (request.args.get('tipo') or '').strip()
    tipo_filtro_clean = clean_txt(tipo_filtro)
    documentos = DocumentoInventarios.get()
    
    result = []
    for doc in documentos:
        doc_tipo = doc.tipo_documento.value if hasattr(doc.tipo_documento, 'value') else str(doc.tipo_documento)
        if tipo_filtro_clean:
            doc_tipo_clean = clean_txt(doc_tipo)
            if doc_tipo_clean != tipo_filtro_clean and tipo_filtro_clean not in doc_tipo_clean:
                continue
        result.append({
            'id': doc.id,
            'numero_documento': doc.numero_documento,
            'tipo_documento': doc_tipo,
            'fecha_creacion': doc.fecha_creacion.isoformat(),
            'observaciones': doc.observaciones,
            'estado': doc.estado,
            'cliente_id': doc.cliente_id,
            'cliente': doc.cliente.razon_social if doc.cliente else None,
            'proveedor_id': doc.proveedor_id,
            'proveedor': doc.proveedor.nombre if doc.proveedor else None,
            'usuario_id': doc.usuario_id,
            'usuario': doc.usuario.nombre if doc.usuario else None
        })
    return jsonify(result), 200


# =========================================================
# OBTENER DOCUMENTO POR ID (INCLUYE DETALLES)
# =========================================================

@documentos_inventario_bp.route('/<int:id>', methods=['GET'])
def get_documento(id):
    doc = DocumentoInventarios.get_by_id(id)
    if not doc:
        return jsonify({'message': 'Documento de inventario no encontrado'}), 404

    detalles = DetalleDocInventario.get_by_documento(id)
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
        'id': doc.id,
        'numero_documento': doc.numero_documento,
        'tipo_documento': doc.tipo_documento.value if hasattr(doc.tipo_documento, 'value') else str(doc.tipo_documento),
        'fecha_creacion': doc.fecha_creacion.isoformat(),
        'observaciones': doc.observaciones,
        'estado': doc.estado,
        'cliente_id': doc.cliente_id,
        'cliente': doc.cliente.razon_social if doc.cliente else None,
        'cliente_nit': doc.cliente.numero_identificacion if doc.cliente else None,
        'cliente_direccion': doc.cliente.direccion if doc.cliente else None,
        'cliente_telefono': doc.cliente.telefono if doc.cliente else None,
        'cliente_correo': doc.cliente.correo if doc.cliente else None,
        'cliente_contacto': doc.cliente.nombre if doc.cliente else None,
        'proveedor_id': doc.proveedor_id,
        'proveedor': doc.proveedor.nombre if doc.proveedor else None,
        'usuario_id': doc.usuario_id,
        'usuario': doc.usuario.nombre if doc.usuario else None,
        'detalles': detalles_list
    }), 200



# =========================================================
# SIGUIENTE NÚMERO DE DOCUMENTO
# =========================================================

@documentos_inventario_bp.route('/siguiente_numero', methods=['GET'])
def get_siguiente_numero():
    tipo = request.args.get('tipo', 'CO')
    numero = DocumentoInventarios.generar_numero_documento(tipo)
    return jsonify({'numero_documento': numero}), 200


# =========================================================
# CREAR DOCUMENTO DE INVENTARIO (CON AJUSTE DE STOCK)
# =========================================================

@documentos_inventario_bp.route('/', methods=['POST'])
def create_documento():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No se proporcionaron datos'}), 400

    tipo_str = (data.get('tipo_documento') or 'Entrada').strip()
    import unicodedata
    def clean_txt(t):
        if not t: return ''
        return unicodedata.normalize('NFKD', str(t)).encode('ASCII', 'ignore').decode('utf-8').lower()

    tipo_clean = clean_txt(tipo_str)
    tipo_enum = None
    for t in TipoDocumento:
        t_clean = clean_txt(t.value)
        t_name_clean = clean_txt(t.name)
        if t_clean == tipo_clean or t_name_clean == tipo_clean or tipo_clean in t_clean:
            tipo_enum = t
            break

    if not tipo_enum:
        tipo_enum = TipoDocumento.ENTRADA

    usuario_id = data.get('usuario_id')
    if not usuario_id or not Usuarios.get_by_id(usuario_id):
        # Fallback al primer usuario si no se envió
        primer_usuario = Usuarios.get_all()
        if primer_usuario:
            usuario_id = primer_usuario[0].id
        else:
            return jsonify({'message': 'No hay usuarios registrados en el sistema'}), 400


    cliente_id = data.get('cliente_id')
    if cliente_id and not Clientes.get_by_id(cliente_id):
        cliente_id = None

    proveedor_id = data.get('proveedor_id')
    if proveedor_id and not Proveedores.get_by_id(proveedor_id):
        proveedor_id = None

    observaciones = (data.get('observaciones') or '').strip()
    numero_doc = (data.get('numero_documento') or '').strip()
    if not numero_doc:
        if tipo_enum == TipoDocumento.ENTRADA:
            prefijo = "CO"
        elif tipo_enum == TipoDocumento.SALIDA:
            prefijo = "SA"
        elif tipo_enum == TipoDocumento.DEVOLUCION:
            prefijo = "DE"
        else:
            prefijo = "EN"
        numero_doc = DocumentoInventarios.generar_numero_documento(prefijo)

    detalles_data = data.get('detalles', [])



    # Validar stock previo si es SALIDA
    if tipo_enum == TipoDocumento.SALIDA:
        for item in detalles_data:
            p_id = item.get('producto_id')
            cant = int(item.get('cantidad', 0))
            prod = Productos.get_by_id(p_id)
            if not prod:
                return jsonify({'message': f'Producto ID {p_id} no encontrado'}), 404
            stock_act = prod.stock if prod.stock is not None else 0
            if stock_act < cant:
                return jsonify({'message': f'Stock insuficiente para el producto {prod.nombre}. Stock actual: {stock_act}'}), 400

    try:
        doc = DocumentoInventarios(
            numero_documento=numero_doc,
            tipo_documento=tipo_enum,
            observaciones=observaciones,
            cliente_id=cliente_id,
            proveedor_id=proveedor_id,
            usuario_id=usuario_id
        )
        doc.save()

        # Procesar detalles y actualizar stock
        for item in detalles_data:
            p_id = item.get('producto_id')
            cant = int(item.get('cantidad', 0))
            val_u = item.get('valor_unitario', 0)

            if p_id and cant > 0:
                prod = Productos.get_by_id(p_id)
                if prod:
                    detalle = DetalleDocInventario(
                        documento_id=doc.id,
                        producto_id=p_id,
                        cantidad=cant,
                        valor_unitario=val_u
                    )
                    detalle.save()

                    stock_act = prod.stock if prod.stock is not None else 0
                    # Actualización de inventario según el tipo
                    if tipo_enum in [TipoDocumento.ENTRADA, TipoDocumento.DEVOLUCION]:
                        prod.stock = stock_act + cant
                    elif tipo_enum == TipoDocumento.SALIDA:
                        prod.stock = max(0, stock_act - cant)
                    elif tipo_enum == TipoDocumento.AJUSTE:
                        prod.stock = stock_act + cant
                    prod.save()

        return jsonify({
            'message': 'Documento de inventario creado exitosamente',
            'documento': doc.to_dict()
        }), 201

    except Exception as e:
        session.rollback()

        return jsonify({'message': 'Error al crear el documento de inventario', 'error': str(e)}), 500


# =========================================================
# ACTUALIZAR DOCUMENTO DE INVENTARIO
# =========================================================

@documentos_inventario_bp.route('/<int:id>', methods=['PUT'])
def update_documento(id):
    doc = DocumentoInventarios.get_by_id(id)
    if not doc:
        return jsonify({'message': 'Documento de inventario no encontrado'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400

    if 'observaciones' in data:
        doc.observaciones = (data['observaciones'] or '').strip()

    if 'estado' in data:
        estado = data['estado']
        if estado in ['0', '1', 0, 1, True, False]:
            doc.estado = bool(int(estado))

    try:
        doc.save()
        return jsonify({
            'message': 'Documento de inventario actualizado exitosamente',
            'documento': doc.to_dict()
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Error al actualizar el documento', 'error': str(e)}), 500


# =========================================================
# ELIMINAR / ANULAR DOCUMENTO DE INVENTARIO (REVIERTE STOCK)
# =========================================================

@documentos_inventario_bp.route('/<int:id>', methods=['DELETE'])
def delete_documento(id):
    doc = DocumentoInventarios.get_by_id(id)
    if not doc:
        return jsonify({'message': 'Documento de inventario no encontrado'}), 404

    try:
        detalles = DetalleDocInventario.get_by_documento(id)
        # Revertir stock según el tipo
        for d in detalles:
            prod = Productos.get_by_id(d.producto_id)
            if prod:
                if doc.tipo_documento in [TipoDocumento.ENTRADA, TipoDocumento.DEVOLUCION]:
                    prod.stock -= d.cantidad
                elif doc.tipo_documento == TipoDocumento.SALIDA:
                    prod.stock += d.cantidad
                elif doc.tipo_documento == TipoDocumento.AJUSTE:
                    prod.stock -= d.cantidad
                prod.save()
            d.delete()

        doc.delete()
        return jsonify({'message': 'Documento de inventario eliminado exitosamente y stock revertido'}), 200

    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Error al eliminar el documento', 'error': str(e)}), 500
