from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
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


class RobotV1(Base):
	__tablename__ = 'RobotV1'
	pk = Column(Integer, primary_key=True)
	robot_name = Column(String(100))
	robot_id = Column(String(36))
	team_number = Column(Integer)
	robot_type = Column(String(100))
	climbing_ability = Column(String(100))
	uses_actuated_gear_mechanism = Column(Boolean)


class RobotNoteV1(Base):
	__tablename__ = 'RobotNoteV1'
	pk = Column(Integer, primary_key=True)
	robot_id = Column(String(36))
	note = Column(String(1000))
	note_id = Column(String(36))


class TeamNoteV1(Base):
	__tablename__ = 'TeamNoteV1'
	pk = Column(Integer, primary_key=True)
	note_id = Column(String(36))
	team_number = Column(Integer)
	note = Column(String(1000))


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
	match_number = Column(Integer)
	event_id = Column(String(36))


class TeamAtMatchV1(Base):
	__tablename__ = 'TeamAtMatchV1'
	pk = Column(Integer, primary_key=True)
	side = Column(String(4))
	team_number = Column(Integer)
	match_id = Column(String(36))
	cycle_time = Column(Float)
	rp = Column(Integer)


class TeamAtMatchV2(Base):
	__tablename__ = 'TeamAtMatchV2'
	pk = Column(Integer, primary_key=True)
	match_id = Column(String(36))
	side = Column(String(4))
	team_number = Column(Integer)
	low_goal = Column(Integer)
	high_goal = Column(Integer)
	gears = Column(Integer)
	auto_gear_position = Column(String(6))
	climbing_rating = Column(Integer)

settings = Settings()
engine = create_engine(settings.database_address)
Base.metadata.create_all(engine)
