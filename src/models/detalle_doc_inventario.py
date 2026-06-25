from sqlalchemy import Column, Integer, Numeric, ForeignKey
from src.models import Base, session

class DetalleDocInventario(Base):
    __tablename__ = 'detalle_doc_inventario'

    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)
    valor_unitario = Column(Numeric(12, 2), nullable=False)
    valor_total = Column(Numeric(12, 2), nullable=False)
    documento_id = Column(Integer, ForeignKey('documento_inventario.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)

    def __init__(self, documento_id, producto_id, cantidad, valor_unitario):
        self.documento_id = documento_id
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
        detalles = session.query(DetalleDocInventario).all()
        return detalles
    
    def get_by_id(detalle_id):
        detalle = session.query(DetalleDocInventario).filter_by(id=detalle_id).first()
        return detalle