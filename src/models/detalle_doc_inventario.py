from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from decimal import Decimal
from src.models import Base, session

class DetalleDocInventario(Base):
    __tablename__ = 'detalle_doc_inventario'

    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)
    valor_unitario = Column(Numeric(12, 2), nullable=False)
    valor_total = Column(Numeric(12, 2), nullable=False)
    documento_id = Column(Integer, ForeignKey('documento_inventario.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)

    producto = relationship('Productos', foreign_keys=[producto_id])

    def __init__(self, documento_id, producto_id, cantidad, valor_unitario):
        self.documento_id = documento_id
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
        return session.query(DetalleDocInventario).all()
    
    @staticmethod
    def get_by_id(detalle_id):
        return session.query(DetalleDocInventario).filter_by(id=detalle_id).first()

    @staticmethod
    def get_by_documento(documento_id):
        return session.query(DetalleDocInventario).filter_by(documento_id=documento_id).all()

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            if hasattr(val, '__float__'):
                result[column.name] = str(val)
            else:
                result[column.name] = val
        return result