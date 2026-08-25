from flask import Blueprint, jsonify, request

from src.models.proveedores import Proveedores


proveedores_bp = Blueprint(
    'proveedores',
    __name__
)



# =========================================================
# GET - OBTENER TODOS LOS PROVEEDORES
# =========================================================

@proveedores_bp.route('/', methods=['GET'])
def get_proveedores():

    proveedores = Proveedores.get()

    proveedores_list = []

    for proveedor in proveedores:
        proveedores_list.append({
            'id': proveedor.id,
            'nombre': proveedor.nombre,
            'nit': proveedor.nit,
            'direccion': proveedor.direccion,
            'telefono': proveedor.telefono,
            'correo': proveedor.correo,
            'nombre_contacto': proveedor.nombre_contacto,
            'estado': proveedor.estado,
            'fecha_creacion': proveedor.fecha_creacion.isoformat()
        })

    return jsonify(proveedores_list), 200


# =========================================================
# GET - OBTENER PROVEEDOR POR ID
# =========================================================

@proveedores_bp.route('/<int:proveedor_id>', methods=['GET'])
def get_proveedor(proveedor_id):

    proveedor = Proveedores.get_by_id(proveedor_id)

    if not proveedor:
        return jsonify({
            'error': 'Proveedor no encontrado'
        }), 404

    return jsonify({
        'id': proveedor.id,
        'nombre': proveedor.nombre,
        'nit': proveedor.nit,
        'direccion': proveedor.direccion,
        'telefono': proveedor.telefono,
        'correo': proveedor.correo,
        'nombre_contacto': proveedor.nombre_contacto,
        'estado': proveedor.estado,
        'fecha_creacion': proveedor.fecha_creacion.isoformat()
    }), 200


# =========================================================
# POST - CREAR PROVEEDOR
# =========================================================

@proveedores_bp.route('/', methods=['POST'])
def create_proveedor():

    data = request.get_json()

    

    if not data:
        return jsonify({
            'error': 'No se recibieron datos'
        }), 400

    
    campos_requeridos = [
        'nombre',
        'nit',
        'direccion',
        'telefono',
        'correo',
        'nombre_contacto',
        'estado'
    ]

    for campo in campos_requeridos:

        if campo not in data or data[campo] is None or str(data[campo]).strip() == '':
            return jsonify({
                'error': f'El campo {campo} es obligatorio'
            }), 400

    # Validar NIT duplicado
    proveedores = Proveedores.get()

    for proveedor in proveedores:

        if proveedor.nit == data['nit']:
            return jsonify({
                'error': 'Ya existe un proveedor con ese NIT'
            }), 409

        if proveedor.correo == data['correo']:
            return jsonify({
                'error': 'Ya existe un proveedor con ese correo'
            }), 409

    try:

        estado = bool(int(data['estado']))

        proveedor = Proveedores(
            nombre=data['nombre'].strip(),
            nit=data['nit'].strip(),
            direccion=data['direccion'].strip(),
            telefono=data['telefono'].strip(),
            correo=data['correo'].strip(),
            nombre_contacto=data['nombre_contacto'].strip(),
            estado=estado
        )

        proveedor.save()

        return jsonify({
            'mensaje': 'Proveedor creado correctamente',
            'proveedor': {
                'id': proveedor.id,
                'nombre': proveedor.nombre,
                'nit': proveedor.nit,
                'direccion': proveedor.direccion,
                'telefono': proveedor.telefono,
                'correo': proveedor.correo,
                'nombre_contacto': proveedor.nombre_contacto,
                'estado': proveedor.estado,
                'fecha_creacion': proveedor.fecha_creacion.isoformat()
            }
        }), 201

    except Exception as e:

        return jsonify({
            'error': 'No fue posible crear el proveedor',
            'detalle': str(e)
        }), 500


# =========================================================
# PUT - ACTUALIZAR PROVEEDOR
# =========================================================

@proveedores_bp.route('/<int:proveedor_id>', methods=['PUT'])
def update_proveedor(proveedor_id):

    proveedor = Proveedores.get_by_id(proveedor_id)

    if not proveedor:
        return jsonify({
            'error': 'Proveedor no encontrado'
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'No se recibieron datos'
        }), 400

    # -----------------------------------------
    # Validar NIT
    # -----------------------------------------

    if 'nit' in data:

        nit = str(data['nit']).strip()

        if not nit:
            return jsonify({
                'error': 'El NIT no puede estar vacío'
            }), 400

        proveedores = Proveedores.get()

        for otro_proveedor in proveedores:

            if (
                otro_proveedor.id != proveedor_id
                and otro_proveedor.nit == nit
            ):
                return jsonify({
                    'error': 'Ya existe otro proveedor con ese NIT'
                }), 409

        proveedor.nit = nit

    # -----------------------------------------
    # Validar correo
    # -----------------------------------------

    if 'correo' in data:

        correo = str(data['correo']).strip()

        if not correo:
            return jsonify({
                'error': 'El correo no puede estar vacío'
            }), 400

        proveedores = Proveedores.get()

        for otro_proveedor in proveedores:

            if (
                otro_proveedor.id != proveedor_id
                and otro_proveedor.correo == correo
            ):
                return jsonify({
                    'error': 'Ya existe otro proveedor con ese correo'
                }), 409

        proveedor.correo = correo

    # -----------------------------------------
    # Actualizar campos
    # -----------------------------------------

    if 'nombre' in data:
        proveedor.nombre = str(data['nombre']).strip()

    if 'direccion' in data:
        proveedor.direccion = str(data['direccion']).strip()

    if 'telefono' in data:
        proveedor.telefono = str(data['telefono']).strip()

    if 'nombre_contacto' in data:
        proveedor.nombre_contacto = str(data['nombre_contacto']).strip()

    if 'estado' in data:
        estado_val = data['estado']
        if isinstance(estado_val, str):
            proveedor.estado = estado_val.lower() in ['1', 'true', 'activo']
        elif isinstance(estado_val, (int, bool)):
            proveedor.estado = bool(estado_val)


    try:

        from src.models import session

        session.commit()

        return jsonify({
            'mensaje': 'Proveedor actualizado correctamente',
            'proveedor': {
                'id': proveedor.id,
                'nombre': proveedor.nombre,
                'nit': proveedor.nit,
                'direccion': proveedor.direccion,
                'telefono': proveedor.telefono,
                'correo': proveedor.correo,
                'nombre_contacto': proveedor.nombre_contacto,
                'estado': proveedor.estado,
                'fecha_creacion': proveedor.fecha_creacion.isoformat()
            }
        }), 200

    except Exception as e:

        from src.models import session

        session.rollback()

        return jsonify({
            'error': 'No fue posible actualizar el proveedor',
            'detalle': str(e)
        }), 500


# =========================================================
# DELETE - ELIMINAR PROVEEDOR
# =========================================================

@proveedores_bp.route('/<int:proveedor_id>', methods=['DELETE'])
def delete_proveedor(proveedor_id):

    proveedor = Proveedores.get_by_id(proveedor_id)

    if not proveedor:
        return jsonify({
            'error': 'Proveedor no encontrado'
        }), 404

    try:

        proveedor.delete()

        return jsonify({
            'mensaje': 'Proveedor eliminado correctamente'
        }), 200

    except Exception as e:

        from src.models import session

        session.rollback()

        return jsonify({
            'error': 'No fue posible eliminar el proveedor',
            'detalle': str(e)
        }), 500