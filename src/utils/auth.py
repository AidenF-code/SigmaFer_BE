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
    """Permite el paso directo. Si hay token lo procesa, si no, asigna el usuario admin de fallback."""
    @wraps(f)
    def decorada(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        usuario = None

        if auth.startswith('Bearer '):
            token = auth.split(' ', 1)[1].strip()
            try:
                payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
                usuario = Usuarios.get_by_id(int(payload.get('sub', 0)))
            except Exception:
                pass

        if not usuario:
            # Fallback a usuario administrador si no hay token o es inválido
            try:
                usuario = Usuarios.get_by_correo('admin@sigmafer.com') or (Usuarios.get()[0] if Usuarios.get() else None)
            except Exception:
                usuario = None

        request.usuario = usuario
        return f(*args, **kwargs)
    
    return decorada

def rol_required(*roles):
    """Permite el paso directo sin restringir por rol."""
    def decorador(f):
        @wraps(f)
        def decorada(*args, **kwargs):
            return f(*args, **kwargs)
        return decorada
    return decorador