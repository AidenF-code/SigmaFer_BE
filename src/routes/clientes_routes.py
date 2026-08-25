from flask import Blueprint, jsonify, request
from src.models.clientes import Clientes

clientes_bp = Blueprint('clientes', __name__)

# =========================================================

# OBTENER TODOS LOS CLIENTES

# =========================================================

@clientes_bp.route('/', methods=['GET'])
def get_clientes():
    clientes = Clientes.get()
    clientes_list = []

    for cliente in clientes:

        clientes_list.append({
            'id': cliente.id,
            'razon_social': cliente.razon_social,
            'nombre': cliente.nombre,
            'tipo_documento': cliente.tipo_documento,
            'numero_identificacion': cliente.numero_identificacion,
            'correo': cliente.correo,
            'telefono': cliente.telefono,
            'direccion': cliente.direccion,
            'estado': cliente.estado,
            'fecha_creacion': cliente.fecha_creacion.isoformat()
        })

    return jsonify(clientes_list), 200


# =========================================================

# OBTENER CLIENTE POR ID

# =========================================================

@clientes_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):

    cliente = Clientes.get_by_id(id)

    if cliente:

        cliente_data = {
            'id': cliente.id,
            'razon_social': cliente.razon_social,
            'nombre': cliente.nombre,
            'tipo_documento': cliente.tipo_documento,
            'numero_identificacion': cliente.numero_identificacion,
            'correo': cliente.correo,
            'telefono': cliente.telefono,
            'direccion': cliente.direccion,
            'estado': cliente.estado,
            'fecha_creacion': cliente.fecha_creacion.isoformat()
        }

        return jsonify(cliente_data), 200

    else:

        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404


# =========================================================

# CREAR CLIENTE

# =========================================================

@clientes_bp.route('/', methods=['POST'])
def create_cliente():
    data = request.get_json()

    if not data:
        return jsonify({
        'message': 'No se proporcionaron datos'
        }), 400


# -----------------------------------------------------
# Tipo de documento
# -----------------------------------------------------

    tipo_documento = data.get('tipo_documento','').strip().upper()

    if not tipo_documento:
        return jsonify({'message': 'El tipo de documento es obligatorio'}), 400

    tipos_validos = ['CC', 'CE', 'NIT']

    if tipo_documento not in tipos_validos:
        return jsonify({
            'message': 'Tipo de documento inválido'
        }), 400


# -----------------------------------------------------
# Razón social
# -----------------------------------------------------

    razon_social = data.get(
        'razon_social',
        ''
    ).strip()

    if not razon_social:
        return jsonify({
            'message': 'El campo "razon social" es obligatorio'
        }), 400

    razon_social_existente = Clientes.get_by_razon_social(
        razon_social
    )

    if razon_social_existente:
        return jsonify({
            'message': 'Ya existe un cliente con esa razón social'
        }), 400


# -----------------------------------------------------
# Nombre
# -----------------------------------------------------

    nombre = data.get(
        'nombre',
        ''
    ).strip()

    if not nombre:
        return jsonify({
            'message': 'El campo "nombre" es obligatorio'
        }), 400


# -----------------------------------------------------
# Número de identificación
# -----------------------------------------------------

    numero_identificacion = data.get(
        'numero_identificacion',
        ''
    ).strip()

    if not numero_identificacion:
        return jsonify({
            'message': 'El campo "numero_identificacion" es obligatorio'
        }), 400

    identificacion_existente = Clientes.get_by_identificacion(
        numero_identificacion
    )

    if identificacion_existente:
        return jsonify({
            'message': 'Ya existe un cliente con ese número de identificación'
        }), 400


# -----------------------------------------------------
# Correo
# -----------------------------------------------------

    correo = data.get(
        'correo',
        ''
    ).strip()

    if not correo:
        return jsonify({
            'message': 'El campo "correo" es obligatorio'
        }), 400

    correo_existente = Clientes.get_by_correo(correo)

    if correo_existente:
        return jsonify({
            'message': 'Ya existe un cliente con ese correo'
        }), 400


# -----------------------------------------------------
# Teléfono
# -----------------------------------------------------

    telefono = data.get(
        'telefono',
        ''
    ).strip()

    if not telefono:
        return jsonify({
            'message': 'El campo "telefono" es obligatorio'
        }), 400

    telefono_existente = Clientes.get_by_telefono(telefono)

    if telefono_existente:
        return jsonify({
            'message': 'Ya existe un cliente con ese número de teléfono'
        }), 400


# -----------------------------------------------------
# Dirección
# -----------------------------------------------------

    direccion = data.get(
        'direccion',
        ''
    ).strip()

    if not direccion:
        return jsonify({
            'message': 'El campo "direccion" es obligatorio'
        }), 400

    direccion_existente = Clientes.get_by_direccion(direccion)

    if direccion_existente:
        return jsonify({
            'message': 'Ya existe un cliente con esa dirección'
        }), 400

    # Validación del estado
    estado = data.get('estado')
    
    if estado not in ['0', '1', 0, 1, True, False]:
        return jsonify({'message': 'El estado debe ser válido'}), 400
    
    estado = bool(int(estado))


# -----------------------------------------------------
# Crear cliente
# -----------------------------------------------------

    cliente = Clientes(
        razon_social=razon_social,
        nombre=nombre,
        tipo_documento=tipo_documento,
        numero_identificacion=numero_identificacion,
        correo=correo,
        telefono=telefono,
        direccion=direccion,
        estado=estado
    )

    cliente.save()

    return jsonify({
        'message': 'Cliente creado exitosamente',
        'cliente': cliente.to_dict()
    }), 201


# =========================================================

# ACTUALIZAR CLIENTE

# =========================================================

@clientes_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):

    cliente = Clientes.get_by_id(id)

    if not cliente:
        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Datos inválidos'
        }), 400

    # -----------------------------------------------------
    # Tipo de documento
    # -----------------------------------------------------
    tipo_documento = data.get('tipo_documento', cliente.tipo_documento).strip().upper()
    tipos_validos = ['CC', 'CE', 'NIT']
    if tipo_documento not in tipos_validos:
        return jsonify({
            'message': 'Tipo de documento inválido'
        }), 400

    # -----------------------------------------------------
    # Razón social
    # -----------------------------------------------------
    razon_social = (data.get('razon_social') or data.get('razonsocial') or cliente.razon_social).strip()
    if not razon_social:
        return jsonify({
            'message': 'El campo "razon_social" es obligatorio'
        }), 400

    razon_social_existente = Clientes.get_by_razon_social(razon_social)
    if razon_social_existente and razon_social_existente.id != id:
        return jsonify({
            'message': 'Ya existe un cliente con esa razón social'
        }), 400

    # -----------------------------------------------------
    # Nombre
    # -----------------------------------------------------
    nombre = data.get('nombre', cliente.nombre).strip()
    if not nombre:
        return jsonify({
            'message': 'El campo "nombre" es obligatorio'
        }), 400

    # -----------------------------------------------------
    # Número de identificación
    # -----------------------------------------------------
    numero_identificacion = data.get('numero_identificacion', cliente.numero_identificacion).strip()
    if not numero_identificacion:
        return jsonify({
            'message': 'El campo "numero_identificacion" es obligatorio'
        }), 400

    identificacion_existente = Clientes.get_by_identificacion(numero_identificacion)
    if identificacion_existente and identificacion_existente.id != id:
        return jsonify({
            'message': 'Ya existe un cliente con ese número de identificación'
        }), 400

    # -----------------------------------------------------
    # Correo
    # -----------------------------------------------------
    correo = data.get('correo', cliente.correo).strip()
    if not correo:
        return jsonify({
            'message': 'El campo "correo" es obligatorio'
        }), 400

    correo_existente = Clientes.get_by_correo(correo)
    if correo_existente and correo_existente.id != id:
        return jsonify({
            'message': 'Ya existe un cliente con ese correo'
        }), 400

    # -----------------------------------------------------
    # Teléfono
    # -----------------------------------------------------
    telefono = data.get('telefono', cliente.telefono).strip()
    if not telefono:
        return jsonify({
            'message': 'El campo "telefono" es obligatorio'
        }), 400

    telefono_existente = Clientes.get_by_telefono(telefono)
    if telefono_existente and telefono_existente.id != id:
        return jsonify({
            'message': 'Ya existe un cliente con ese número de teléfono'
        }), 400

    # -----------------------------------------------------
    # Dirección
    # -----------------------------------------------------
    direccion = data.get('direccion', cliente.direccion).strip()
    if not direccion:
        return jsonify({
            'message': 'El campo "direccion" es obligatorio'
        }), 400

    direccion_existente = Clientes.get_by_direccion(direccion)
    if direccion_existente and direccion_existente.id != id:
        return jsonify({
            'message': 'Ya existe un cliente con esa dirección'
        }), 400

    # -----------------------------------------------------
    # Estado
    # -----------------------------------------------------
    if 'estado' in data:
        estado = data.get('estado')
        if estado in ['0', '1', 0, 1, True, False]:
            cliente.estado = bool(int(estado))

    # -----------------------------------------------------
    # Actualizar cliente
    # -----------------------------------------------------
    cliente.razon_social = razon_social
    cliente.nombre = nombre
    cliente.tipo_documento = tipo_documento
    cliente.numero_identificacion = numero_identificacion
    cliente.correo = correo
    cliente.telefono = telefono
    cliente.direccion = direccion

    cliente.save()

    return jsonify({
        'message': 'Cliente actualizado exitosamente',
        'cliente': cliente.to_dict()
    }), 200


# =========================================================
# ELIMINAR CLIENTE
# =========================================================

@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Clientes.get_by_id(id)
    if not cliente:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    try:
        cliente.delete()
        return jsonify({'message': 'Cliente eliminado exitosamente'}), 200
    except Exception as e:
        from src.models import session
        session.rollback()
        return jsonify({
            'message': 'No se pudo eliminar el cliente (puede tener registros asociados)',
            'error': str(e)
        }), 500


