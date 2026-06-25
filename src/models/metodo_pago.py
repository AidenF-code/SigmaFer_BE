from sqlalchemy import Boolean, Column, Integer, String
from src.models import Base, session

class MetodoPago(Base):
    __tablename__ = 'metodo_pago'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    estado = Column(Boolean, nullable=False, default=1)

    def __init__(self, nombre, estado=True):
        self.nombre = nombre
        self.estado = estado

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def get():
        metodos_pago = session.query(MetodoPago).all()
        return metodos_pago
    
    def get_by_id(metodo_id):
        metodo = session.query(MetodoPago).filter_by(id=metodo_id).first()
        return metodo