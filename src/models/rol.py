from sqlalchemy import Column, Integer, String
from src.models import Base, session

class Roles(Base):
    __tablename__ = 'rol'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def get():
        roles = session.query(Roles).all()
        return roles
    
    def get_by_id(rol_id):
        rol = session.query(Roles).filter_by(id=rol_id).first()
        return rol
    
    def to_dict(self):
        return{column.name: getattr(self, column.name) for column in self.__table__.columns}