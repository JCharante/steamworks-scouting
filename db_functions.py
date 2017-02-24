from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db_setup import Base, MatchV1, MatchAtEventV1, TeamAtEventV1, TeamV1, TeamAtMatchV1
import util
import uuid
from settings import Settings
from typing import Tuple, List, Dict
import exceptions


settings = Settings()
# Connects to the database
engine = create_engine(settings.database_address)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

