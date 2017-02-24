from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from settings import Settings

Base = declarative_base()

# The naming convention for {table_name}V{table_version} will be used once we finish the mvp. Until then they will stay
# at V1 and you will have to continue to drop the tables until we have our first release.


class GroupV1(Base):
	__tablename__ = 'GroupV1'
	pk = Column(Integer, primary_key=True)
	group_id = Column(String(36))
	name = Column(String(100))
	owner_aid = Column(String(36))
	invite_code = Column(String(6))


class GroupMemberV1(Base):
	__tablename__ = 'GroupMemberV1'
	pk = Column(Integer, primary_key=True)
	group_id = Column(String(36))
	member_aid = Column(String(36))


class TeamV1(Base):
	__tablename__ = 'TeamV1'
	pk = Column(Integer, primary_key=True)
	team_name = Column(String(100))
	team_number = Column(Integer)


class EventV1(Base):
	__tablename__ = 'EventV1'
	pk = Column(Integer, primary_key=True)
	event_name = Column(String(100))
	event_id = Column(String(36))


class TeamAtEventV1(Base):
	__tablename__ = 'TeamAtEventV1'
	pk = Column(Integer, primary_key=True)
	team_number = Column(Integer)
	event_id = Column(String(36))


class MatchV1(Base):
	__tablename__ = 'MatchV1'
	pk = Column(Integer, primary_key=True)
	blue_score = Column(Integer)
	red_score = Column(Integer)
	match_id = Column(String(36))


class MatchAtEventV1(Base):
	__tablename__ = 'MatchAtEventV1'
	pk = Column(Integer, primary_key=True)
	match_number = Column(Integer)
	event_id = Column(String(36))
	match_id = Column(String(36))


class TeamAtMatchV1(Base):
	__tablename__ = 'TeamAtMatchV1'
	pk = Column(Integer, primary_key=True)
	team_number = Column(Integer)
	match_id = Column(String(36))


settings = Settings()
engine = create_engine(settings.database_address)
Base.metadata.create_all(engine)
