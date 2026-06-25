from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey, Date
from enum import Enum as PyEnum
from datetime import date
from src.models import Base, session

class TipoDocumento(PyEnum):
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

    def __init__(self, numero_documento, tipo_documento, observaciones=None, cliente_id=None, proveedor_id=None, usuario_id=None):
        self.numero_documento = numero_documento
        self.tipo_documento = tipo_documento
        self.observaciones = observaciones
        self.cliente_id = cliente_id
        self.proveedor_id = proveedor_id
        self.usuario_id = usuario_id

    def save(self):
        session.add(self)
        session.commit()
    
    def delete(self):
        session.delete(self)
        session.commit()

    def get():
        documentos = session.query(DocumentoInventarios).all()
        return documentos
    
    def get_by_id(documento_id):
        documento = session.query(DocumentoInventarios).filter_by(id=documento_id).first()
        return documento