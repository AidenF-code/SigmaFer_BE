from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from datetime import date
from src.models import Base, session

class OrdenCompra(Base):
    __tablename__ = 'orden_compra'

    id = Column(Integer, primary_key=True)
    numero_orden = Column(String(50), unique=True, nullable=False)
    fecha_creacion = Column(Date, nullable=False, default=date.today)
    observaciones = Column(String(200), nullable=True)
    estado = Column(Boolean, nullable=False, default=True)
    subtotal = Column(Numeric(12, 2), nullable=False, default=0)
    total = Column(Numeric(12, 2), nullable=False, default=0)
    proveedor_id = Column(Integer, ForeignKey('proveedores.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    proveedor = relationship('Proveedores', foreign_keys=[proveedor_id])
    usuario = relationship('Usuarios', foreign_keys=[usuario_id])

    def __init__(self, numero_orden, proveedor_id, usuario_id, observaciones=None, estado=True):
        self.numero_orden = numero_orden
        self.proveedor_id = proveedor_id
        self.usuario_id = usuario_id
        self.observaciones = observaciones
        self.estado = estado

    def recalcular_totales(self, detalles):
        self.subtotal = sum(d.valor_total for d in detalles)
        self.total = self.subtotal

    def save(self):
        session.add(self)
        session.commit()
            
    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        return session.query(OrdenCompra).all()
    
    @staticmethod
    def get_by_id(orden_id):
        return session.query(OrdenCompra).filter_by(id=orden_id).first()

    @staticmethod
    def get_by_numero(numero_orden):
        return session.query(OrdenCompra).filter_by(numero_orden=numero_orden).first()

    @staticmethod
    def generar_numero_orden():
        ultima_orden = session.query(OrdenCompra).order_by(OrdenCompra.id.desc()).first()
        if not ultima_orden:
            return "OC-00001"
        try:
            import re
            nums = re.findall(r'\d+', str(ultima_orden.numero_orden))
            if nums:
                ultimo_num = int(nums[-1])
                return f"OC-{ultimo_num + 1:05d}"
            return "OC-00001"
        except Exception:
            return f"OC-{(ultima_orden.id or 0) + 1:05d}"


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