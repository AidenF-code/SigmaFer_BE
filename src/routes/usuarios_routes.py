from flask import Blueprint, jsonify, request
from src.models import session
from src.models.usuarios import Usuarios
from src.models.rol import Roles
from src.utils.auth import token_required, rol_required, generate_token

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])  # Todos los usuarios
@token_required
@rol_required('Administrador')
def get_usuarios():
    usuarios = Usuarios.get()
    usuarios_list = []
    for usuario in usuarios:
        usuarios_list.append({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'identificacion': usuario.identificacion,
            'correo': usuario.correo,
            'telefono': usuario.telefono,
            'estado': usuario.estado,
            'fecha_creacion': usuario.fecha_creacion.isoformat(),
            'rol_id': usuario.rol_id,
            'rol': usuario.rol.nombre if usuario.rol else None
        })
    return jsonify(usuarios_list), 200


@usuarios_bp.route('/<int:id>', methods=['GET'])  # Usuario por ID
@token_required
@rol_required('Administrador')
def get_usuario(id):
    usuario = Usuarios.get_by_id(id)
    if usuario:
        usuario_data = {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'identificacion': usuario.identificacion,
            'correo': usuario.correo,
            'telefono': usuario.telefono,
            'estado': usuario.estado,
            'fecha_creacion': usuario.fecha_creacion.isoformat(),
            'rol_id': usuario.rol_id,
            'rol': usuario.rol.nombre if usuario.rol else None
        }
        return jsonify(usuario_data), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404


@usuarios_bp.route('/', methods=['POST'])  # Crear usuario
@token_required
@rol_required('Administrador')
def crear_usuario():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'No se proporcionaron datos'
        }), 400

    nombre = data.get('nombre', '').strip()
    if not nombre:
        return jsonify({
            'message': 'El campo "nombre" es obligatorio'
        }), 400

    identificacion = str(data.get('identificacion', '')).strip()
    if not identificacion:
        return jsonify({
            'message': 'El campo "identificacion" es obligatorio'
        }), 400

    identificacion_existente = Usuarios.get_by_identificacion(identificacion)
    if identificacion_existente:
        return jsonify({
            'message': 'Ya existe un usuario con esa identificación'
        }), 400

    correo = data.get('correo', '').strip()
    if not correo:
        return jsonify({
            'message': 'El campo "correo" es obligatorio'
        }), 400

    correo_existente = Usuarios.get_by_correo(correo)
    if correo_existente:
        return jsonify({
            'message': 'Ya existe un usuario con ese correo'
        }), 400

    telefono = str(data.get('telefono', '')).strip()
    if not telefono:
        return jsonify({
            'message': 'El campo "telefono" es obligatorio'
        }), 400

    password = data.get('password', '').strip()
    if not password:
        return jsonify({
            'message': 'El campo "password" es obligatorio'
        }), 400

    rol_id = data.get('rol_id')
    if rol_id is None:
        return jsonify({
            'message': 'El campo "rol_id" es obligatorio'
        }), 400

    rol = Roles.get_by_id(rol_id)
    if not rol:
        return jsonify({
            'message': 'El rol especificado no existe'
        }), 404

    estado = data.get('estado', True)
    if isinstance(estado, str):
        if estado == '1':
            estado = True
        elif estado == '0':
            estado = False
        else:
            return jsonify({
                'message': 'El campo "estado" debe ser 1 o 0'
            }), 400

    try:
        nuevo_usuario = Usuarios(
            nombre=nombre,
            identificacion=identificacion,
            correo=correo,
            telefono=telefono,
            password=password,
            rol_id=rol_id,
            estado=estado
        )
        nuevo_usuario.set_password(password)
        nuevo_usuario.save()

        return jsonify({
            'message': 'Usuario creado correctamente',
            'usuario': nuevo_usuario.to_dict()
        }), 201

    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'Error al crear el usuario',
            'error': str(e)
        }), 500


@usuarios_bp.route('/<int:id>', methods=['PUT'])  # Actualizar usuario
@token_required
@rol_required('Administrador')
def update_usuario(id):
    usuario = Usuarios.get_by_id(id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400

    nombre = data.get('nombre', usuario.nombre).strip()
    if not nombre:
        return jsonify({'message': 'El campo "nombre" es obligatorio'}), 400

    identificacion = str(data.get('identificacion', usuario.identificacion)).strip()
    if not identificacion:
        return jsonify({'message': 'El campo "identificacion" es obligatorio'}), 400

    ident_exist = Usuarios.get_by_identificacion(identificacion)
    if ident_exist and ident_exist.id != id:
        return jsonify({'message': 'Ya existe un usuario con esa identificación'}), 400

    correo = data.get('correo', usuario.correo).strip()
    if not correo:
        return jsonify({'message': 'El campo "correo" es obligatorio'}), 400

    correo_exist = Usuarios.get_by_correo(correo)
    if correo_exist and correo_exist.id != id:
        return jsonify({'message': 'Ya existe un usuario con ese correo'}), 400

    telefono = str(data.get('telefono', usuario.telefono)).strip()
    if not telefono:
        return jsonify({'message': 'El campo "telefono" es obligatorio'}), 400

    if 'password' in data and str(data['password']).strip():
        usuario.set_password(str(data['password']).strip())

    if 'rol_id' in data and data['rol_id'] is not None:
        rol = Roles.get_by_id(data['rol_id'])
        if not rol:
            return jsonify({'message': 'El rol especificado no existe'}), 404
        usuario.rol_id = data['rol_id']

    if 'estado' in data:
        estado = data.get('estado')
        if estado in ['0', '1', 0, 1, True, False]:
            usuario.estado = bool(int(estado))

    usuario.nombre = nombre
    usuario.identificacion = identificacion
    usuario.correo = correo
    usuario.telefono = telefono

    try:
        usuario.save()
        return jsonify({
            'message': 'Usuario actualizado exitosamente',
            'usuario': usuario.to_dict()
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'Error al actualizar usuario',
            'error': str(e)
        }), 500


@usuarios_bp.route('/<int:id>', methods=['DELETE'])  # Eliminar usuario
@token_required
@rol_required('Administrador')
def delete_usuario(id):
    usuario = Usuarios.get_by_id(id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    try:
        usuario.delete()
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'No se pudo eliminar el usuario (puede tener registros vinculados)',
            'error': str(e)
        }), 500


@usuarios_bp.route('/login', methods=['POST'])  # Autenticación de usuario
def login_usuario():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Credenciales no proporcionadas'}), 400

    correo = (data.get('correo') or data.get('email') or '').strip()
    password = data.get('password', '').strip()

    if not correo or not password:
        return jsonify({'message': 'Correo y contraseña son obligatorios'}), 400

    usuario = Usuarios.get_by_correo(correo)
    if not usuario or not usuario.verificar_password(password):
        return jsonify({'message': 'Correo o contraseña incorrectos'}), 401

    if not usuario.estado:
        return jsonify({'message': 'El usuario se encuentra inactivo'}), 403

    user_data = usuario.to_dict()
    user_data.pop('password', None)
    if usuario.rol:
        user_data['rol'] = usuario.rol.nombre

    # Si es el primer ingreso del usuario, requerir cambio de contraseña
    if getattr(usuario, 'primer_ingreso', False):
        return jsonify({
            'primer_ingreso': True,
            'message': 'Debe cambiar su contraseña en el primer inicio de sesión',
            'temp_token': generate_token(usuario, horas=1),
            'usuario': user_data
        }), 200

    return jsonify({
        'message': 'Inicio de sesión exitoso',
        'access_token': generate_token(usuario),
        'token_type': 'Bearer',
        'usuario': user_data
    }), 200

