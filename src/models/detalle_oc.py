from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from decimal import Decimal
from src.models import Base, session

class DetalleOC(Base):
    __tablename__ = 'detalle_oc'

    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)
    valor_unitario = Column(Numeric(12, 2), nullable=False)
    valor_total = Column(Numeric(12, 2), nullable=False)
    orden_compra_id = Column(Integer, ForeignKey('orden_compra.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)

    producto = relationship('Productos', foreign_keys=[producto_id])

    def __init__(self, orden_compra_id, producto_id, cantidad, valor_unitario):
        self.orden_compra_id = orden_compra_id
        self.producto_id = producto_id
        self.cantidad = int(cantidad)
        self.valor_unitario = Decimal(str(valor_unitario))
        self.valor_total = self.cantidad * self.valor_unitario

    def save(self):
        session.add(self)
        session.commit()
    
    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        return session.query(DetalleOC).all()
    
    @staticmethod
    def get_by_id(detalle_id):
        return session.query(DetalleOC).filter_by(id=detalle_id).first()

    @staticmethod
    def get_by_orden(orden_compra_id):
        return session.query(DetalleOC).filter_by(orden_compra_id=orden_compra_id).all()

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            if hasattr(val, '__float__'):
                result[column.name] = str(val)
            else:
                result[column.name] = val
        return result