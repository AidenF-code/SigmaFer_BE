from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from datetime import date
from src.models import Base, session

class OrdenCompra(Base):
    __tablename__ = 'orden_compra'

    id = Column(Integer, primary_key=True)
    numero_orden = Column(String(50), unique=True, nullable=False)
    fecha_creacion = Column(Date, nullable=False, default=date.today)
    observaciones = Column(String(200), nullable=True)
    estado = Column(Boolean, nullable=False, default=True)
    subtotal = Column(Integer, nullable=False, default=0)
    total = Column(Integer, nullable=False, default=0)
    proveedor_id = Column(Integer, ForeignKey('proveedores.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    def __init__(self, numero_orden, proveedor_id, usuario_id, observaciones=None):
        self.numero_orden = numero_orden
        self.proveedor_id = proveedor_id
        self.usuario_id = usuario_id
        self.observaciones = observaciones

    def save(self):
        session.add(self)
        session.commit()
            
    def delete(self):
        session.delete(self)
        session.commit()

    def get():
        ordenes = session.query(OrdenCompra).all()
        return ordenes
    
    def get_by_id(orden_id):
        orden = session.query(OrdenCompra).filter_by(id=orden_id).first()
        return orden