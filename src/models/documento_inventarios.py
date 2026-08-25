from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from datetime import date
from src.models import Base, session

class TipoDocumento(str, PyEnum):
    ENTRADA = "Entrada"
    SALIDA = "Salida"
    DEVOLUCION = "Devolución"
    AJUSTE = "Ajuste"

class DocumentoInventarios(Base):
    __tablename__ = 'documento_inventario'

    id = Column(Integer, primary_key=True)
    numero_documento = Column(String(50), unique=True, nullable=False)
    tipo_documento = Column(Enum(TipoDocumento), nullable=False)
    fecha_creacion = Column(Date, nullable=False, default=date.today)
    observaciones = Column(String(200), nullable=True)
    estado = Column(Boolean, nullable=False, default=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=True)
    proveedor_id = Column(Integer, ForeignKey('proveedores.id'), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    cliente = relationship('Clientes', foreign_keys=[cliente_id])
    proveedor = relationship('Proveedores', foreign_keys=[proveedor_id])
    usuario = relationship('Usuarios', foreign_keys=[usuario_id])

    def __init__(self, numero_documento, tipo_documento, observaciones=None, cliente_id=None, proveedor_id=None, usuario_id=None, estado=True):
        self.numero_documento = numero_documento
        self.tipo_documento = tipo_documento
        self.observaciones = observaciones
        self.cliente_id = cliente_id
        self.proveedor_id = proveedor_id
        self.usuario_id = usuario_id
        self.estado = estado

    def save(self):
        session.add(self)
        session.commit()
    
    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        return session.query(DocumentoInventarios).all()
    
    @staticmethod
    def get_by_id(documento_id):
        return session.query(DocumentoInventarios).filter_by(id=documento_id).first()

    @staticmethod
    def get_by_numero(numero_documento):
        return session.query(DocumentoInventarios).filter_by(numero_documento=numero_documento).first()

    @staticmethod
    def generar_numero_documento(tipo="CO"):
        prefijo = "CO"
        if isinstance(tipo, str):
            t_upper = tipo.upper()
            if "COMPRA" in t_upper or t_upper == "CO":
                prefijo = "CO"
            elif "AJUSTE" in t_upper or "AJ" in t_upper or "EN" in t_upper or "ENTRADA" in t_upper:
                prefijo = "EN"
            elif "SALIDA" in t_upper or "SAL" in t_upper or t_upper == "SA":
                prefijo = "SA"
            elif "DEVOLU" in t_upper or "DEV" in t_upper or t_upper == "DE":
                prefijo = "DE"
        
        ultimo_doc = session.query(DocumentoInventarios).filter(
            DocumentoInventarios.numero_documento.like(f"{prefijo}-%")
        ).order_by(DocumentoInventarios.id.desc()).first()




        if not ultimo_doc:
            return f"{prefijo}-00001"
        try:
            import re
            nums = re.findall(r'\d+', str(ultimo_doc.numero_documento))
            if nums:
                ultimo_num = int(nums[-1])
                return f"{prefijo}-{ultimo_num + 1:05d}"
            return f"{prefijo}-00001"
        except Exception:
            return f"{prefijo}-{(ultimo_doc.id or 0) + 1:05d}"


    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            if isinstance(val, date):
                result[column.name] = val.isoformat()
            elif isinstance(val, PyEnum):
                result[column.name] = val.value
            else:
                result[column.name] = val
        return result