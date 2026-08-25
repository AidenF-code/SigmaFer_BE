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

    @staticmethod
    def get():
        return session.query(MetodoPago).all()
    
    @staticmethod
    def get_by_id(metodo_id):
        return session.query(MetodoPago).filter_by(id=metodo_id).first()

    @staticmethod
    def get_by_nombre(nombre):
        return session.query(MetodoPago).filter_by(nombre=nombre).first()

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}