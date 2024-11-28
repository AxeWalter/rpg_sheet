from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, BLOB, DateTime, select
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine("sqlite:///rpg_db")
conn = engine.connect()
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()



#data = session.query(Characters).all()
#print(data[0].name)