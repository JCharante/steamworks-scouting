from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from settings import Settings

Base = declarative_base()


class RankingV1(Base):
	__tablename__ = 'RankingV1'
	pk = Column(Integer, primary_key=True)
	event_code = Column(String(20))
	ranking = Column(Integer)
	team = Column(String(40))  # Some teams have letters in them, lol blue alliance
	won = Column(Boolean)


settings = Settings()
engine = create_engine(settings.database_address)
Base.metadata.create_all(engine)
