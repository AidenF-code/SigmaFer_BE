from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Date
from datetime import date
from src.models import Base, session

class Proveedores(Base):
    __tablename__ = 'proveedores'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(20), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    nit = Column(String(25), nullable=False, unique=True)
    estado = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(Date, nullable=False, default=date.today)
    nombre_contacto = Column(String(100), nullable=False)

    def __init__(self, nombre, nit, direccion, telefono, correo, nombre_contacto):
        self.nombre = nombre
        self.nit = nit
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.nombre_contacto = nombre_contacto

    def save(self):
        session.add(self)
        session.commit()
    
    def delete(self):
        session.delete(self)
        session.commit()

    def get():
        proveedores = session.query(Proveedores).all()
        return proveedores
    
    def get_by_id(proveedor_id):
        proveedor = session.query(Proveedores).filter_by(id=proveedor_id).first()
        return proveedor