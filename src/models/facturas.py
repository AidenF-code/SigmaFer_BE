from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    ForeignKey,
    Date
)

from sqlalchemy.orm import relationship

from datetime import date

from src.models import Base, session


class Facturas(Base):

    __tablename__ = 'facturas'


    # =====================================================
    # CAMPOS
    # =====================================================

    id = Column(
        Integer,
        primary_key=True
    )

    numero_factura = Column(
        String(50),
        unique=True,
        nullable=False
    )

    fecha_emision = Column(
        Date,
        nullable=False,
        default=date.today
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    iva = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    total = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    observaciones = Column(
        String(200),
        nullable=True
    )

    estado_pago = Column(
        Boolean,
        nullable=False,
        default=False
    )


    # =====================================================
    # CLAVES FORÁNEAS
    # =====================================================

    cliente_id = Column(
        Integer,
        ForeignKey('clientes.id'),
        nullable=False
    )

    usuario_id = Column(
        Integer,
        ForeignKey('usuarios.id'),
        nullable=False
    )

    metodo_pago_id = Column(
        Integer,
        ForeignKey('metodo_pago.id'),
        nullable=False
    )


    # =====================================================
    # RELACIONES
    # =====================================================

    cliente = relationship(
        'Clientes',
        foreign_keys=[cliente_id]
    )

    usuario = relationship(
        'Usuarios',
        foreign_keys=[usuario_id]
    )

    metodo_pago = relationship(
        'MetodoPago',
        foreign_keys=[metodo_pago_id]
    )


    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(
        self,
        numero_factura,
        cliente_id,
        usuario_id,
        metodo_pago_id,
        observaciones=None,
        estado_pago=False,
        fecha_emision=None
    ):

        self.numero_factura = numero_factura
        self.cliente_id = cliente_id
        self.usuario_id = usuario_id
        self.metodo_pago_id = metodo_pago_id
        self.observaciones = observaciones
        self.estado_pago = bool(estado_pago)
        if fecha_emision:
            self.fecha_emision = fecha_emision



    # =====================================================
    # RECALCULAR TOTALES
    # =====================================================

    def recalcular_totales(
        self,
        detalles_factura
    ):

        self.subtotal = sum(
            detalle.subtotal
            for detalle in detalles_factura
        )

        self.iva = sum(
            detalle.iva
            for detalle in detalles_factura
        )

        self.total = sum(
            detalle.valor_total
            for detalle in detalles_factura
        )


    # =====================================================
    # GUARDAR
    # =====================================================

    def save(self):

        session.add(self)
        session.commit()


    # =====================================================
    # ELIMINAR
    # =====================================================

    def delete(self):

        session.delete(self)
        session.commit()


    # =====================================================
    # OBTENER TODAS (DE LA ÚLTIMA A LA PRIMERA)
    # =====================================================

    @staticmethod
    def get():

        return session.query(
            Facturas
        ).order_by(Facturas.id.desc()).all()


    # =====================================================
    # OBTENER POR ID
    # =====================================================

    @staticmethod
    def get_by_id(factura_id):

        return session.query(
            Facturas
        ).filter_by(
            id=factura_id
        ).first()


    # =====================================================
    # OBTENER POR NÚMERO
    # =====================================================

    @staticmethod
    def get_by_numero(
        numero_factura
    ):

        return session.query(
            Facturas
        ).filter_by(
            numero_factura=numero_factura
        ).first()


    # =====================================================
    # GENERAR CONSECUTIVO
    # =====================================================

    @staticmethod
    def generar_numero_factura():
        import re
        ultima_factura = (
            session.query(Facturas)
            .order_by(Facturas.id.desc())
            .first()
        )

        if not ultima_factura or not ultima_factura.numero_factura:
            return "FV-000001"

        numeros = re.findall(r'\d+', str(ultima_factura.numero_factura))
        if numeros:
            try:
                ultimo_numero = int(numeros[-1])
                return f"FV-{ultimo_numero + 1:06d}"
            except ValueError:
                pass

        return f"FV-{(ultima_factura.id or 0) + 1:06d}"



    # =====================================================
    # SERIALIZACIÓN
    # =====================================================

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            if hasattr(val, 'isoformat'):
                result[column.name] = val.isoformat()
            elif hasattr(val, '__float__') and not isinstance(val, (int, float, bool)):
                result[column.name] = str(val)
            else:
                result[column.name] = val
        return result