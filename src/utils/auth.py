from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, request, jsonify

from src.models.usuarios import Usuarios

def generate_token(usuario, horas=8):
    rol_nombre = usuario.rol.nombre if (hasattr(usuario, 'rol') and usuario.rol and hasattr(usuario.rol, 'nombre')) else str(usuario.rol_id)
    payload = {
        'sub': str(usuario.id),  # A quién pertenece el token
        'correo': usuario.correo,
        'nombre': usuario.nombre,
        'rol': rol_nombre,
        'rol_id': usuario.rol_id,
        'iat': datetime.now(timezone.utc),  # emitido
        'exp': datetime.now(timezone.utc) + timedelta(hours=horas)  # expira
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def token_required(f):
    """Protege una ruta. Deja el usuario en request.usuario"""
    @wraps(f)
    def decorada(*args, **kwargs):
        auth = request.headers.get('Authorization', '')

        if not auth.startswith('Bearer '):
            return jsonify({'message': 'Token faltante o mal formado'}), 401

        token = auth.split(' ', 1)[1].strip()

        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado, inicia sesión de nuevo'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        usuario = Usuarios.get_by_id(int(payload['sub']))
        if not usuario:
            return jsonify({'message': 'Usuario no encontrado'}), 401

        request.usuario = usuario
        return f(*args, **kwargs)
    
    return decorada

def rol_required(*roles):
    """Se usa después de @token_required para validar roles por nombre o id"""
    def decorador(f):
        @wraps(f)
        def decorada(*args, **kwargs):
            usuario = getattr(request, 'usuario', None)
            if not usuario:
                return jsonify({'message': 'No autenticado'}), 401

            rol_nombre = usuario.rol.nombre if (usuario.rol and hasattr(usuario.rol, 'nombre')) else ''
            rol_id = usuario.rol_id

            roles_normalizados = [str(r).lower() for r in roles]

            coincide = (
                str(rol_nombre).lower() in roles_normalizados or
                str(rol_id) in roles_normalizados or
                rol_id in roles
            )

            if not coincide:
                return jsonify({'message': 'No tiene permisos para esta acción'}), 403
            return f(*args, **kwargs)
        return decorada
    return decorador