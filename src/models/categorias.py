from sqlalchemy import Column, Integer, String
from src.models import Base, session

class Categorias(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def get():
        categorias = session.query(Categorias).all()
        return categorias

    def get_by_id(categoria_id):
        categoria = session.query(Categorias).filter_by(id=categoria_id).first()
        return categoria
    
    def to_dict(self):
        return{column.name: getattr(self, column.name) for column in self.__table__.columns}