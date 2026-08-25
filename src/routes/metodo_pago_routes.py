from flask import Blueprint, jsonify, request
from src.models import session
from src.models.metodo_pago import MetodoPago


metodos_pago_bp = Blueprint(
    'metodos_pago',
    __name__
)


# =========================================================
# OBTENER TODOS LOS MÉTODOS DE PAGO
# =========================================================

@metodos_pago_bp.route('/', methods=['GET'])
def get_metodos_pago():

    metodos_pago = MetodoPago.get()

    metodos_list = []

    for metodo in metodos_pago:

        metodos_list.append({
            'id': metodo.id,
            'nombre': metodo.nombre,
            'estado': metodo.estado
        })

    return jsonify(metodos_list), 200


# =========================================================
# OBTENER MÉTODO DE PAGO POR ID
# =========================================================

@metodos_pago_bp.route('/<int:metodo_id>', methods=['GET'])
def get_metodo_pago(metodo_id):

    metodo = MetodoPago.get_by_id(metodo_id)

    if not metodo:

        return jsonify({
            'message': 'Método de pago no encontrado'
        }), 404


    metodo_data = {
        'id': metodo.id,
        'nombre': metodo.nombre,
        'estado': metodo.estado
    }


    return jsonify(metodo_data), 200


# =========================================================
# CREAR MÉTODO DE PAGO
# =========================================================

@metodos_pago_bp.route('/', methods=['POST'])
def create_metodo_pago():

    data = request.get_json()

    if not data:

        return jsonify({
            'message': 'No se proporcionaron datos'
        }), 400


    # -----------------------------------------------------
    # Validar nombre
    # -----------------------------------------------------

    nombre = (
        data.get('nombre', '')
        .strip()
    )


    if not nombre:

        return jsonify({
            'message': 'El campo "nombre" es obligatorio'
        }), 400


    # -----------------------------------------------------
    # Verificar duplicado
    # -----------------------------------------------------

    metodos_pago = MetodoPago.get()

    nombre_existente = next(
        (
            metodo
            for metodo in metodos_pago
            if metodo.nombre.lower() == nombre.lower()
        ),
        None
    )


    if nombre_existente:

        return jsonify({
            'message': 'Ya existe un método de pago con ese nombre'
        }), 400


    # -----------------------------------------------------
    # Validar estado
    # -----------------------------------------------------

    estado = data.get(
        'estado',
        True
    )


    if isinstance(estado, str):

        if estado == '1':

            estado = True

        elif estado == '0':

            estado = False

        else:

            return jsonify({
                'message': 'El estado debe ser 1 o 0'
            }), 400


    if not isinstance(estado, bool):

        return jsonify({
            'message': 'El estado debe ser booleano'
        }), 400


    # -----------------------------------------------------
    # Crear método
    # -----------------------------------------------------

    try:

        metodo = MetodoPago(
            nombre=nombre,
            estado=estado
        )

        metodo.save()


        return jsonify({
            'message': 'Método de pago creado exitosamente',
            'metodo_pago': {
                'id': metodo.id,
                'nombre': metodo.nombre,
                'estado': metodo.estado
            }
        }), 201


    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Error al crear el método de pago',
            'error': str(e)
        }), 500


# =========================================================
# ACTUALIZAR MÉTODO DE PAGO
# =========================================================

@metodos_pago_bp.route('/<int:metodo_id>', methods=['PUT'])
def update_metodo_pago(metodo_id):

    metodo = MetodoPago.get_by_id(
        metodo_id
    )


    if not metodo:

        return jsonify({
            'message': 'Método de pago no encontrado'
        }), 404


    data = request.get_json()


    if not data:

        return jsonify({
            'message': 'Datos inválidos'
        }), 400


    # -----------------------------------------------------
    # Validar nombre
    # -----------------------------------------------------

    nombre = (
        data.get('nombre', '')
        .strip()
    )


    if not nombre:

        return jsonify({
            'message': 'El campo "nombre" es obligatorio'
        }), 400


    # -----------------------------------------------------
    # Verificar duplicado
    # -----------------------------------------------------

    metodos_pago = MetodoPago.get()

    nombre_existente = next(
        (
            item
            for item in metodos_pago
            if (
                item.nombre.lower() == nombre.lower()
                and item.id != metodo.id
            )
        ),
        None
    )


    if nombre_existente:

        return jsonify({
            'message': 'Ya existe otro método de pago con ese nombre'
        }), 400


    # -----------------------------------------------------
    # Validar estado
    # -----------------------------------------------------

    estado = data.get(
        'estado',
        metodo.estado
    )


    if isinstance(estado, str):

        if estado == '1':

            estado = True

        elif estado == '0':

            estado = False

        else:

            return jsonify({
                'message': 'El estado debe ser 1 o 0'
            }), 400


    if not isinstance(estado, bool):

        return jsonify({
            'message': 'El estado debe ser booleano'
        }), 400


    # -----------------------------------------------------
    # Actualizar
    # -----------------------------------------------------

    try:

        metodo.nombre = nombre
        metodo.estado = estado

        metodo.save()


        return jsonify({
            'message': 'Método de pago actualizado exitosamente',
            'metodo_pago': {
                'id': metodo.id,
                'nombre': metodo.nombre,
                'estado': metodo.estado
            }
        }), 200


    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Error al actualizar el método de pago',
            'error': str(e)
        }), 500


# =========================================================
# ELIMINAR MÉTODO DE PAGO
# =========================================================

@metodos_pago_bp.route('/<int:metodo_id>', methods=['DELETE'])
def delete_metodo_pago(metodo_id):

    metodo = MetodoPago.get_by_id(
        metodo_id
    )


    if not metodo:

        return jsonify({
            'message': 'Método de pago no encontrado'
        }), 404


    try:

        metodo.delete()


        return jsonify({
            'message': 'Método de pago eliminado exitosamente'
        }), 200


    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'No se puede eliminar el método de pago',
            'error': str(e)
        }), 500