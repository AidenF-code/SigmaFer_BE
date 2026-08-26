import time
from flask import Blueprint, request, jsonify
from sqlalchemy import text
from werkzeug.security import generate_password_hash

from src.models import engine
from src.models.usuarios import Usuarios
from src.models.rol import Roles
from src.utils.auth import generate_token, token_required

auth_bp = Blueprint('auth', __name__)

# Asegurar columna primer_ingreso en MySQL
def _asegurar_columna_primer_ingreso():
    try:
        with engine.connect() as conn:
            res = conn.execute(text("SHOW COLUMNS FROM usuarios LIKE 'primer_ingreso'")).fetchone()
            if not res:
                conn.execute(text("ALTER TABLE usuarios ADD COLUMN primer_ingreso TINYINT(1) NOT NULL DEFAULT 1"))
                conn.commit()
    except Exception as e:
        print("Aviso al verificar columna primer_ingreso en usuarios:", e)

_asegurar_columna_primer_ingreso()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    for campo in ('correo', 'password', 'nombre'):
        if not data.get(campo):
            return jsonify({'message': f'El campo {campo} es obligatorio'}), 400

    raw_password = str(data.get('password', ''))
    if len(raw_password) < 8:
        return jsonify({'message': 'La contraseña debe tener al menos 8 caracteres'}), 400

    correo = data['correo'].strip()
    if Usuarios.get_by_correo(correo):
        return jsonify({'message': 'Ese correo ya está registrado'}), 409

    # Resolver rol
    rol_id = data.get('rol_id')
    if not rol_id and data.get('rol'):
        rol_obj = Roles.get_by_nombre(str(data['rol']).strip())
        if rol_obj:
            rol_id = rol_obj.id

    if not rol_id:
        todos_roles = Roles.get()
        rol_id = todos_roles[0].id if todos_roles else 1

    identificacion = str(data.get('identificacion', '')).strip()
    if not identificacion:
        identificacion = f"USR-{int(time.time())}"

    telefono = str(data.get('telefono', '')).strip()
    if not telefono:
        telefono = "0000000000"

    # Encriptar la contraseña
    password_hasheada = generate_password_hash(raw_password)

    usuario = Usuarios(
        nombre=data['nombre'].strip(),
        correo=correo,
        telefono=telefono,
        password=password_hasheada,
        rol_id=rol_id,
        identificacion=identificacion,
        estado=True,
        primer_ingreso=True
    )
    usuario.save()

    return jsonify({
        'message': 'Usuario registrado exitosamente',
        'usuario': usuario.to_dict(),
        'access_token': generate_token(usuario),
        'token_type': 'Bearer'
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    correo = (data.get('correo') or data.get('email') or '').strip()
    password = data.get('password')

    if not correo or not password:
        return jsonify({'message': 'Correo y contraseña son obligatorios'}), 400

    usuario = Usuarios.get_by_correo(correo)

    if not usuario or not usuario.verificar_password(password):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    if not usuario.estado:
        return jsonify({'message': 'Usuario inactivo. Contacte al administrador'}), 403

    user_data = usuario.to_dict()

    # Si es el primer ingreso del usuario, interceptar y requerir cambio de contraseña
    if getattr(usuario, 'primer_ingreso', False):
        return jsonify({
            'primer_ingreso': True,
            'message': 'Debe cambiar su contraseña en el primer inicio de sesión',
            'temp_token': generate_token(usuario, horas=1),
            'usuario': user_data
        }), 200

    return jsonify({
        'access_token': generate_token(usuario),
        'token_type': 'Bearer',
        'expires_in': 28800,
        'usuario': user_data
    }), 200


@auth_bp.route('/cambiar_password_inicial', methods=['POST'])
@token_required
def cambiar_password_inicial():
    data = request.get_json() or {}
    nueva_password = str(data.get('password_nueva') or data.get('password') or '').strip()

    if not nueva_password:
        return jsonify({'message': 'La nueva contraseña es obligatoria'}), 400

    if len(nueva_password) < 8:
        return jsonify({'message': 'La contraseña debe tener al menos 8 caracteres'}), 400

    usuario = request.usuario
    usuario.set_password(nueva_password)
    usuario.primer_ingreso = False
    usuario.save()

    return jsonify({
        'message': 'Contraseña actualizada exitosamente. Inicie sesión con su nueva contraseña.',
        'usuario': usuario.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET', 'POST'])
@token_required
def me():
    return jsonify(request.usuario.to_dict()), 200