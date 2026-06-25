from sqlalchemy import Column, Integer, Numeric, ForeignKey
from src.models import Base, session

class DetalleOC(Base):
    __tablename__ = 'detalle_oc'

    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)
    valor_unitario = Column(Numeric(12, 2), nullable=False)
    valor_total = Column(Numeric(12, 2), nullable=False)
    orden_compra_id = Column(Integer, ForeignKey('orden_compra.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)

    def __init__(self, orden_compra_id, producto_id, cantidad, valor_unitario):
        self.orden_compra_id = orden_compra_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.valor_unitario = valor_unitario
        self.valor_total = cantidad * valor_unitario

    def save(self):
        session.add(self)
        session.commit()
    
    def delete(self):
        session.delete(self)
        session.commit()

    def get():
        detalles = session.query(DetalleOC).all()
        return detalles
    
    def get_by_id(detalle_id):
        detalle = session.query(DetalleOC).filter_by(id=detalle_id).first()
        return detalle