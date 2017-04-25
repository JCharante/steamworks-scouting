from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine, Text
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


class TrueSkillMatchV1(Base):
	__tablename__ = 'TrueSkillMatchV1'
	pk = Column(Integer, primary_key=True)
	winning_alliance = Column(String(4))
	blue_1 = Column(Integer)
	blue_2 = Column(Integer)
	blue_3 = Column(Integer)
	red_1 = Column(Integer)
	red_2 = Column(Integer)
	red_3 = Column(Integer)
	event_key = Column(String(10))
	match_key = Column(String(20))


class TrueSkillTeamV1(Base):
	__tablename__ = 'TrueSkillTeamV1'
	pk = Column(Integer, primary_key=True)
	team_number = Column(Integer)
	mu = Column(Float)
	sigma = Column(Float)


class GraphTeamInfoV4(Base):
	__tablename__ = 'GraphTeamInfoV4'
	pk = Column(Integer, primary_key=True)
	team_number = Column(Integer)
	region = Column(Text(collation='utf8_general_ci'))
	nickname = Column(Text(collation='utf8_general_ci'))


settings = Settings()
engine = create_engine(settings.database_address)
Base.metadata.create_all(engine)
