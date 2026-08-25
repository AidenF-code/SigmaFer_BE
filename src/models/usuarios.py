from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import Base, session
from src.models.rol import Roles


class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    identificacion = Column(String(20), nullable=False, unique=True)
    correo = Column(String(100), nullable=False, unique=True)
    telefono = Column(String(20), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    estado = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(Date, nullable=False, default=date.today)
    rol_id = Column(Integer, ForeignKey('rol.id'), nullable=False)

    rol = relationship('Roles', foreign_keys=[rol_id])

    def __init__(self, nombre, correo, telefono, password, rol_id, identificacion, estado=True):
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.password = password
        self.rol_id = rol_id
        self.identificacion = identificacion
        self.estado = estado

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def verificar_password(self, raw_password):
        if not self.password:
            return False
        # Si la contraseña está hasheada con werkzeug
        if self.password.startswith('scrypt:') or self.password.startswith('pbkdf2:') or self.password.startswith('argon2:'):
            return check_password_hash(self.password, raw_password)
        # Soporte para contraseñas existentes en texto plano con actualización automática a hash
        es_valida = (self.password == raw_password)
        if es_valida:
            self.set_password(raw_password)
            self.save()
        return es_valida

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        return session.query(Usuarios).all()
    
    @staticmethod
    def get_by_id(usuario_id):
        return session.query(Usuarios).filter_by(id=usuario_id).first()
    
    @staticmethod
    def get_by_identificacion(identificacion):
        return session.query(Usuarios).filter_by(
            identificacion=identificacion
        ).first()
    
    @staticmethod
    def get_by_correo(correo):
        return session.query(Usuarios).filter_by(
            correo=correo
        ).first()
    
    def to_dict(self):
        data = {}
        for column in self.__table__.columns:
            if column.name == 'password':
                continue
            val = getattr(self, column.name)
            if isinstance(val, date):
                data[column.name] = val.isoformat()
            else:
                data[column.name] = val
        data['rol'] = self.rol.nombre if self.rol else None
        return data