from sqlalchemy import Column, Integer, String, Boolean, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base
import os


Base = declarative_base()


class EventV1(Base):
	__tablename__ = 'EventV1'
	pk = Column(Integer, primary_key=True)
	key = Column(Text())
	official = Column(Boolean)
	has_ended = Column(Boolean)
	start_date = Column(Text())
	end_date = Column(Text())
	name = Column(Text())
	event_type_string = Column(Text())
	blacklisted = Column(Boolean)


class MatchV1(Base):
	__tablename__ = 'MatchV1'
	pk = Column(Integer, primary_key=True)
	event_code = Column(Text(collation='utf8_general_ci'))
	match_key = Column(Text(collation='utf8_general_ci'))
	has_played = Column(Boolean)
	taking_bets = Column(Boolean)
	blue_1 = Column(Integer)
	blue_2 = Column(Integer)
	blue_3 = Column(Integer)
	red_1 = Column(Integer)
	red_2 = Column(Integer)
	red_3 = Column(Integer)
	result = Column(Text())


class InviteCodeV1(Base):
	__tablename__ = 'InviteCodeV1'
	pk = Column(Integer, primary_key=True)
	code = Column(String(36))
	generated_by = Column(String(36))
	active = Column(Boolean)
	activated_by = Column(String(36))


class UserV1(Base):
	__tablename__ = 'UserV1'
	pk = Column(Integer, primary_key=True)
	uuid = Column(String(36))
	username = Column(Text(collation='utf8_general_ci'))
	balance = Column(Integer)


class BetV1(Base):
	__tablename__ = 'BetV1'
	pk = Column(Integer, primary_key=True)
	uuid = Column(String(36))
	amount = Column(Integer)
	match_key = Column(String(36))
	wagered_on = Column(Text())

engine = create_engine(os.environ['dba'])
Base.metadata.create_all(engine)
