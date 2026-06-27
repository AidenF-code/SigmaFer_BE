from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from datetime import date
from src.models import Base, session

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    identificacion = Column(String(20), nullable=False, unique=True)
    correo = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    estado = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(Date, nullable=False, default=date.today)
    rol_id = Column(Integer, ForeignKey('rol.id'), nullable=False)

    def __init__(self, nombre, correo, password, rol_id, identificacion, estado=True):
        self.nombre = nombre
        self.correo = correo
        self.password = password
        self.rol_id = rol_id
        self.identificacion = identificacion
        self.estado = estado


    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def get():
        usuarios = session.query(Usuarios).all()
        return usuarios
    
    def get_by_id(usuario_id):
        usuario = session.query(Usuarios).filter_by(id=usuario_id).first()
        return usuario
    
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
        return{column.name: getattr(self, column.name) for column in self.__table__.columns}