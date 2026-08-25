from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date
from src.models import Base, session

class Proveedores(Base):
    __tablename__ = 'proveedores'

    productos = relationship('Productos', back_populates='proveedor')
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(20), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    nit = Column(String(25), nullable=False, unique=True)
    estado = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(Date, nullable=False, default=date.today)
    nombre_contacto = Column(String(100), nullable=False)
    

    def __init__(self, nombre, nit, direccion, telefono, estado, correo, nombre_contacto):
        self.nombre = nombre
        self.nit = nit
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.nombre_contacto = nombre_contacto
        self.estado = estado

    def save(self):
        session.add(self)
        session.commit()
    
    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        return session.query(Proveedores).all()
    
    @staticmethod
    def get_by_id(proveedor_id):
        return session.query(Proveedores).filter_by(id=proveedor_id).first()

    @staticmethod
    def get_by_nit(nit):
        return session.query(Proveedores).filter_by(nit=nit).first()

    @staticmethod
    def get_by_correo(correo):
        return session.query(Proveedores).filter_by(correo=correo).first()

    def to_dict(self):
        return {
            column.name: (
                getattr(self, column.name).isoformat()
                if isinstance(getattr(self, column.name), date)
                else getattr(self, column.name)
            )
            for column in self.__table__.columns
        }