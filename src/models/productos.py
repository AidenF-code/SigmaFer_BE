from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date
from src.models import Base, session


class Productos(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(50), unique=True, nullable=False)
    stock = Column(Numeric(12, 2), nullable=False)
    stock_minimo = Column(Numeric(12, 2), nullable=False)
    stock_maximo = Column(Numeric(12, 2))
    precio = Column(Numeric(12, 2), nullable=False)
    estado = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(Date, nullable=False, default=date.today)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    proveedor_id = Column(Integer, ForeignKey('proveedores.id'), nullable=False)
    proveedor = relationship('Proveedores', back_populates='productos')
    categoria = relationship('Categorias')

    def __init__(self, nombre, codigo, stock, stock_minimo, stock_maximo, precio, estado, categoria_id, proveedor_id):
        self.nombre = nombre
        self.codigo = codigo
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.stock_maximo = stock_maximo
        self.precio = precio
        self.estado = estado
        self.categoria_id = categoria_id
        self.proveedor_id = proveedor_id

    def save(self):
        session.add(self)
        session.commit()
    
    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        return session.query(Productos).all()
    
    @staticmethod
    def get_by_id(producto_id):
        return session.query(Productos).filter_by(id=producto_id).first()
    
    @staticmethod
    def get_by_codigo(codigo):
        return session.query(Productos).filter_by(codigo=codigo).first()

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            if isinstance(val, date):
                result[column.name] = val.isoformat()
            elif hasattr(val, '__float__'):
                result[column.name] = str(val)
            else:
                result[column.name] = val
        return result