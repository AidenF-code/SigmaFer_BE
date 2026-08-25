import os
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
import pymysql

DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root@localhost:3306/sigmafer2?charset=utf8mb4')

engine = create_engine(DATABASE_URL)

Session = scoped_session(sessionmaker(bind=engine))

session = Session

Base = declarative_base()

