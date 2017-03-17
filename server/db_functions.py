from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, MatchV1
import util
import uuid
from typing import Tuple, List, Dict
import exceptions
import os
from datetime import datetime
import dateutil.parser


# Connects to the database
engine = create_engine(os.environ['db_address'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def add_matchv1(match_id: str, event_name: str, team_number: int, match_number: str, auto_line_cross: bool,
				auto_low_goal: bool, auto_hopper: bool, auto_collect: bool, auto_gear_pos: str,
				auto_high_goal_pos: str, climb_rating: str, gear_rating: str, total_gears: int,
				gear_dispense_method: str, got_gear_from_human: bool, got_gear_from_floor: bool,
				high_goal_rating: str, high_goal_shoot_from_key: bool, high_goal_shoot_from_wall: bool,
				high_goal_shoot_from_afar: bool, low_goal_rating: str, total_hoppers: int, collected_from_hopper: bool,
				last_modified: str) -> None:
	session = DBSession()
	stored_match = session.query(MatchV1).filter(MatchV1.match_id == match_id).first()
	if stored_match is not None:
		stored_match = stored_match  # type: MatchV1
		stored_match_last_modified_date = dateutil.parser.parse(stored_match.last_modified)
		new_match_last_modified_date = dateutil.parser.parse(last_modified)
		if stored_match_last_modified_date > new_match_last_modified_date:
			raise exceptions.MatchDataOutdated()
		else:
			session.query(MatchV1).filter(MatchV1.match_id == match_id).delete()
	session.add(MatchV1(
		match_id=match_id, event_name=event_name, team_number=team_number, match_number=match_number,
		auto_line_cross=auto_line_cross, auto_low_goal=auto_low_goal, auto_hopper=auto_hopper,
		auto_collect=auto_collect, auto_gear_pos=auto_gear_pos, auto_high_goal_pos=auto_high_goal_pos,
		climb_rating=climb_rating, gear_rating=gear_rating, total_gears=total_gears,
		gear_dispense_method=gear_dispense_method, got_gear_from_human=got_gear_from_human,
		got_gear_from_floor=got_gear_from_floor, high_goal_rating=high_goal_rating,
		high_goal_shoot_from_key=high_goal_shoot_from_key, high_goal_shoot_from_wall=high_goal_shoot_from_wall,
		high_goal_shoot_from_afar=high_goal_shoot_from_afar, low_goal_rating=low_goal_rating,
		total_hoppers=total_hoppers, collected_from_hopper=collected_from_hopper, last_modified=last_modified
	))
	session.commit()
	session.close()
