from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base
import util
import uuid
from typing import Tuple, List, Dict
import exceptions
import os


# Connects to the database
engine = create_engine(os.environ['db_address'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
