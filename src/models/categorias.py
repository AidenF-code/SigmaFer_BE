from sqlalchemy import Column, Integer, String
from src.models import Base, session

class Categorias(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    estado = Column(String(20), default='Activo', nullable=True)

    def __init__(self, nombre, estado='Activo'):
        self.nombre = nombre
        self.estado = estado or 'Activo'

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        return session.query(Categorias).all()

    @staticmethod
    def get_by_id(categoria_id):
        return session.query(Categorias).filter_by(id=categoria_id).first()

    @staticmethod
    def get_by_nombre(nombre):
        return session.query(Categorias).filter_by(nombre=nombre).first()
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'estado': self.estado or 'Activo'
        }