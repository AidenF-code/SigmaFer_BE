from flask import Blueprint, jsonify, request
from src.models.clientes import Clientes
from src.models.usuarios import Usuarios
from src.models.metodo_pago import MetodoPago
from src.models.facturas import Facturas

facturas_bp = Blueprint('facturas', __name__)

@facturas_bp.route('/', methods=['GET'])
def get_facturas():
    facturas_list = Facturas.get()
    result = []
    for factura in facturas_list:
        result.append({
            'id': factura.id,
            'numero_factura': factura.numero_factura,
            'fecha_emision': factura.fecha_emision.isoformat(),
            'subtotal': str(factura.subtotal),
            'iva': str(factura.iva),
            'total': str(factura.total),
            'observaciones': factura.observaciones,
            'estado_pago': factura.estado_pago,
            'cliente_id': factura.cliente_id,
            'usuario_id': factura.usuario_id,
            'metodo_pago_id': factura.metodo_pago_id
        })
    return jsonify(result), 200

@facturas_bp.route('/<int:factura_id>', methods=['GET'])
def get_factura_by_id(factura_id):
    factura = Facturas.get_by_id(factura_id)
    if factura:
        result = {
            'id': factura.id,
            'numero_factura': factura.numero_factura,
            'fecha_emision': factura.fecha_emision.isoformat(),
            'subtotal': str(factura.subtotal),
            'iva': str(factura.iva),
            'total': str(factura.total),
            'observaciones': factura.observaciones,
            'estado_pago': factura.estado_pago,
            'cliente_id': factura.cliente_id,
            'usuario_id': factura.usuario_id,
            'metodo_pago_id': factura.metodo_pago_id
        }
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Factura no encontrada'}), 404
    

#Crear Factura    
@facturas_bp.route('/', methods=['POST'])
def create_factura():

    data = request.get_json()

    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400
    
    cliente_id = data.get('cliente_id')

    if not cliente_id:
        return jsonify({'message': 'El cliente es obligatorio'}), 400
    
    usuario_id = data.get('usuario_id')

    if not usuario_id:
        return jsonify({'message': 'El usuario es obligatorio'}), 400
    
    metodo_pago_id = data.get('metodo_pago_id')

    if not metodo_pago_id:
        return jsonify({'message': 'El método de pago es obligatorio'}), 400
    
    observaciones = data.get('observaciones', '').strip()

    numero_factura = Facturas.generar_numero_factura()
    
    factura = Facturas(
        numero_factura=numero_factura,
        cliente_id=cliente_id,
        usuario_id=usuario_id,
        metodo_pago_id=metodo_pago_id,
        observaciones=observaciones
    )

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




@facturas_bp.route('/<int:id>', methods=['PUT'])
def update_factura(id):

    factura = Facturas.get_by_id(id)

    if not factura:
        return jsonify({'message': 'Factura no encontrada'}), 404

    data = request.get_json()

    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400

    # Validar cliente
    if 'cliente_id' not in data or not data['cliente_id']:
        return jsonify({'message': 'El cliente es obligatorio'}), 400

    cliente = Clientes.get_by_id(data['cliente_id'])

    if not cliente:
        return jsonify({'message': 'El cliente no existe'}), 404

    # Validar usuario
    if 'usuario_id' not in data or not data['usuario_id']:
        return jsonify({'message': 'El usuario es obligatorio'}), 400

    usuario = Usuarios.get_by_id(data['usuario_id'])

    if not usuario:
        return jsonify({'message': 'El usuario no existe'}), 404

    # Validar método de pago
    if 'metodo_pago_id' not in data or not data['metodo_pago_id']:
        return jsonify({'message': 'El método de pago es obligatorio'}), 400

    metodo_pago = MetodoPago.get_by_id(data['metodo_pago_id'])

    if not metodo_pago:
        return jsonify({'message': 'El método de pago no existe'}), 404

    # Actualizar datos
    factura.cliente_id = cliente.id
    factura.usuario_id = usuario.id
    factura.metodo_pago_id = metodo_pago.id

    # Observaciones (opcional)
    if 'observaciones' in data:
        factura.observaciones = data['observaciones'].strip()

    # Estado de pago (opcional)
    if 'estado_pago' in data:
        factura.estado_pago = data['estado_pago']

    factura.save()

    factura_dict = factura.to_dict()
    factura_dict['fecha_emision'] = factura.fecha_emision.isoformat()
    factura_dict['subtotal'] = str(factura.subtotal)
    factura_dict['iva'] = str(factura.iva)
    factura_dict['total'] = str(factura.total)

    return jsonify({
        'message': 'Factura actualizada exitosamente',
        'factura': factura_dict
    }), 200