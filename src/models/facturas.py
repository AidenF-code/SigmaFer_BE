from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Date
from datetime import date
from src.models import Base, session


class Facturas(Base):
    __tablename__ = 'facturas'

    id = Column(Integer, primary_key=True)
    numero_factura = Column(String(50), unique=True, nullable=False)
    fecha_emision = Column(Date, nullable=False, default=date.today)
    subtotal = Column(Numeric(10, 2), nullable=False, default=0)
    iva = Column(Numeric(10, 2), nullable=False, default=0)
    total = Column(Numeric(10, 2), nullable=False, default=0)
    observaciones = Column(String(200), nullable=True)
    estado_pago = Column(Boolean, nullable=False, default=False)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    metodo_pago_id = Column(Integer, ForeignKey('metodo_pago.id'), nullable=False)

    def __init__(self, numero_factura, cliente_id, usuario_id, metodo_pago_id, observaciones=None):
        self.numero_factura = numero_factura
        self.cliente_id = cliente_id
        self.usuario_id = usuario_id
        self.metodo_pago_id = metodo_pago_id
        self.observaciones = observaciones

    def recalcular_totales(self, detalles):
        self.subtotal = sum(det.subtotal for det in detalles)
        self.iva = sum(det.iva for det in detalles)
        self.total = sum(det.valor_total for det in detalles)

    def save(self):
        session.add(self)
        session.commit()
    
    def delete(self):
        session.delete(self)
        session.commit()

    def get():
        facturas = session.query(Facturas).all()
        return facturas
    
    def get_by_id(factura_id):
        factura = session.query(Facturas).filter_by(id=factura_id).first()
        return factura