import json
from sqlalchemy import Column, Integer, String, JSON
from src.models import Base, session

class Roles(Base):
    __tablename__ = 'rol'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    permisos = Column(JSON, nullable=True)

    def __init__(self, nombre, permisos=None):
        self.nombre = nombre
        self.permisos = permisos if permisos is not None else {}

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        return session.query(Roles).all()
    
    @staticmethod
    def get_by_id(rol_id):
        return session.query(Roles).filter_by(id=rol_id).first()

    @staticmethod
    def get_by_nombre(nombre):
        return session.query(Roles).filter_by(nombre=nombre).first()

    def get_permisos(self):
        if not self.permisos:
            return {}
        if isinstance(self.permisos, dict):
            return self.permisos
        try:
            return json.loads(self.permisos)
        except Exception:
            return {}

    def has_permission(self, modulo, recurso, accion):
        if self.nombre and self.nombre.lower() in ['administrador', 'admin', 'superadmin']:
            return True
        perms = self.get_permisos()
        return bool(perms.get(modulo, {}).get(recurso, {}).get(accion, False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'permisos': self.get_permisos()
        }