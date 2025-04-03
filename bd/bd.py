from sqlalchemy.orm import Session, sessionmaker, declarative_base, relationship
from sqlalchemy import Integer, String, Column, create_engine, ForeignKey
from config import url

base=declarative_base()
engine=create_engine(url=url, echo=True)

def get_db():
    Session=sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session=Session()
    return session

class tableGolosov(base):
    __tablename__= "golocov"

    id=Column(Integer, primary_key=True)
    pocemon_id = Column(Integer, ForeignKey('pocemon.id'))
    amount = Column(Integer)

    pocemon_sv = relationship("tablePocemons", back_populates="golosov_sv")

class tablePocemons(base):
    __tablename__="pocemon"

    id=Column(Integer, primary_key=True)
    pocemon=Column(String)

    golosov_sv = relationship("tableGolosov", back_populates="pocemon_sv")

base.metadata.create_all(bind=engine)



