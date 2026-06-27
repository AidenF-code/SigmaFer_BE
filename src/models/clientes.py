from sqlalchemy import Column, Integer, String, Boolean, Date
from datetime import date
from src.models import Base, session

class Clientes(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    razonsocial = Column(String(150), nullable=False)
    nombre = Column(String(100), nullable=False)
    identificacion = Column(String(20), nullable=False, unique=True)
    correo = Column(String(100), nullable=False, unique=True)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=False)
    nit = Column(String(25), nullable=False, unique=True)
    estado = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(Date, nullable=False, default=date.today)

    def __init__(self, razonsocial, nombre, identificacion, correo, telefono, direccion, nit):
        self.razonsocial = razonsocial
        self.nombre = nombre
        self.identificacion = identificacion
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion
        self.nit = nit

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def get():
        clientes = session.query(Clientes).all()
        return clientes
    '''
    def get_by_id(cliente_id):
        cliente = session.query(Clientes).filter_by(id=cliente_id).first()
        return cliente
    '''
    
    @staticmethod
    def get_by_id(cliente_id):
        return session.query(Clientes).filter_by(id=cliente_id).first()

    @staticmethod
    def get_by_razonsocial(razonsocial):
        return session.query(Clientes).filter_by(
            razonsocial=razonsocial
        ).first()

    @staticmethod
    def get_by_nit(nit):
        return session.query(Clientes).filter_by(
            nit=nit
        ).first()

    @staticmethod
    def get_by_identificacion(identificacion):
        return session.query(Clientes).filter_by(
            identificacion=identificacion
        ).first()

    @staticmethod
    def get_by_correo(correo):
        return session.query(Clientes).filter_by(
            correo=correo
        ).first()

    @staticmethod
    def get_by_telefono(telefono):
        return session.query(Clientes).filter_by(
            telefono=telefono
        ).first()

    @staticmethod
    def get_by_direccion(direccion):
        return session.query(Clientes).filter_by(
            direccion=direccion
        ).first()

    
    def to_dict(self):
        return{column.name: getattr(self, column.name) for column in self.__table__.columns}