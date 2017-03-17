from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
import os


Base = declarative_base()


class MatchV1(Base):
	__tablename__ = 'MatchV1'
	pk = Column(Integer, primary_key=True)
	match_id = Column(String(36))
	event_name = Column(String(100))
	team_number = Column(Integer)
	match_number = Column(String(10))
	auto_line_cross = Column(Boolean)
	auto_low_goal = Column(Boolean)
	auto_hopper = Column(Boolean)
	auto_collect = Column(Boolean)
	auto_gear_pos = Column(String(10))
	auto_high_goal_pos = Column(String(10))
	climb_rating = Column(String(10))
	gear_rating = Column(String(10))
	total_gears = Column(Integer)
	gear_dispense_method = Column(String(15))
	got_gear_from_human = Column(Boolean)
	got_gear_from_floor = Column(Boolean)
	high_goal_rating = Column(String(10))
	high_goal_shoot_from_key = Column(Boolean)
	high_goal_shoot_from_wall = Column(Boolean)
	high_goal_shoot_from_afar = Column(Boolean)
	low_goal_rating = Column(String(10))
	total_hoppers = Column(Integer)
	collected_from_hopper = Column(Boolean)
	last_modified = Column(String(30))

engine = create_engine(os.environ['db_address'])
Base.metadata.create_all(engine)
