from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Date
from datetime import date
from src.models import Base, session


class Productos(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(50), unique=True, nullable=False)
    stock = Column(Integer, nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    stock_maximo = Column(Integer, nullable=False)
    precio = Column(Numeric(12, 2), nullable=False)
    estado = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(Date, nullable=False, default=date.today)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    proveedor_id = Column(Integer, ForeignKey('proveedores.id'), nullable=False)

    def __init__(self, nombre, codigo, stock, stock_minimo, stock_maximo, precio, categoria_id, proveedor_id):
        self.nombre = nombre
        self.codigo = codigo
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.stock_maximo = stock_maximo
        self.precio = precio
        self.categoria_id = categoria_id
        self.proveedor_id = proveedor_id

    def save(self):
        session.add(self)
        session.commit()
    
    def delete(self):
        session.delete(self)
        session.commit()

    def get():
        productos = session.query(Productos).all()
        return productos
    
    def get_by_id(producto_id):
        producto = session.query(Productos).filter_by(id=producto_id).first()
        return producto