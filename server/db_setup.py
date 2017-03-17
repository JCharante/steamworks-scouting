from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
import os


Base = declarative_base()

engine = create_engine(os.environ['db_address'])
Base.metadata.create_all(engine)
