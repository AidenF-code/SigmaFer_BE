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

    def recalcular_totales(self, detalles_factura):
        self.subtotal = sum(detalle.subtotal for detalle in detalles_factura)
        self.iva = sum(detalle.iva for detalle in detalles_factura)
        self.total = sum(detalle.valor_total for detalle in detalles_factura)

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def get():
        return session.query(Facturas).all()

    def get_by_id(factura_id):
        return session.query(Facturas).filter_by(id=factura_id).first()

    def get_by_numero(numero_factura):
        return session.query(Facturas).filter_by(
            numero_factura=numero_factura
        ).first()
    
    @staticmethod
    def generar_numero_factura():
        ultima_factura = session.query(Facturas)\
            .order_by(Facturas.id.desc())\
            .first()
        if not ultima_factura:
            return "FV-000001"
        
        ultimo_numero = int(ultima_factura.numero_factura[3:])  # Extrae el número de la cadena "FV-000001"
        nuevo_numero = ultimo_numero + 1
        return f"FV-{nuevo_numero:06d}"


    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }