from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from decimal import Decimal
from src.models import Base, session


class DetalleFacturas(Base):
    __tablename__ = 'detalle_facturas'

    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)
    valor_unitario = Column(Numeric(12, 2), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)
    iva = Column(Numeric(12, 2), nullable=False)
    iva_porcentaje = Column(Numeric(5, 2), nullable=False)
    valor_total = Column(Numeric(12, 2), nullable=False)
    factura_id = Column(Integer, ForeignKey('facturas.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)

    producto = relationship('Productos', foreign_keys=[producto_id])

    def __init__(self, factura_id, producto_id, cantidad, valor_unitario, iva_porcentaje):
        self.factura_id = factura_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.valor_unitario = Decimal(str(valor_unitario))
        self.iva_porcentaje = Decimal(str(iva_porcentaje))

        self.subtotal = Decimal(str(cantidad)) * self.valor_unitario
        self.iva = self.subtotal * (self.iva_porcentaje / Decimal('100'))
        self.valor_total = self.subtotal + self.iva

    def save(self):
        session.add(self)
        session.commit()
    
    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        return session.query(DetalleFacturas).all()
    
    @staticmethod
    def get_by_id(detalle_id):
        return session.query(DetalleFacturas).filter_by(id=detalle_id).first()
    
    @staticmethod
    def get_by_factura(factura_id):
        return session.query(DetalleFacturas).filter_by(
            factura_id=factura_id
        ).all()
    
    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            if hasattr(val, '__float__'):
                result[column.name] = str(val)
            else:
                result[column.name] = val
        return result