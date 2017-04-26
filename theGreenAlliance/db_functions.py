import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, MatchV1, InviteCodeV1, UserV1, BetV1

engine = create_engine(os.environ['dba'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
