from sqlalchemy import Column, Integer, String, Boolean, Date
from datetime import date
from src.models import Base, session


class Clientes(Base):

    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    razon_social = Column(String(150), nullable=False)
    nombre = Column(String(100), nullable=False)
    tipo_documento = Column(String(10), nullable=False)
    numero_identificacion = Column(String(20), nullable=False, unique=True)
    correo = Column(String(100), nullable=False, unique=True)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=False)
    estado = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(Date, nullable=False, default=date.today)

    def __init__(
        self,
        razon_social,
        nombre,
        tipo_documento,
        numero_identificacion,
        correo,
        telefono,
        estado,
        direccion
    ):
        self.razon_social = razon_social
        self.nombre = nombre
        self.tipo_documento = tipo_documento
        self.numero_identificacion = numero_identificacion
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion
        self.estado = estado

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        return session.query(Clientes).all()

    @staticmethod
    def get_by_id(cliente_id):
        return session.query(Clientes).filter_by(
            id=cliente_id
        ).first()

    @staticmethod
    def get_by_razon_social(razon_social):
        return session.query(Clientes).filter_by(
            razon_social=razon_social
        ).first()

    @staticmethod
    def get_by_identificacion(numero_identificacion):
        return session.query(Clientes).filter_by(
            numero_identificacion=numero_identificacion
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
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }