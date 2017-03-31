from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, MatchV1, MatchV2, MatchV3, MatchV4, MatchV5
import util
import uuid
from typing import Tuple, List, Dict
import exceptions
import os
from datetime import datetime
import dateutil.parser
import re


# Connects to the database
engine = create_engine(os.environ['db_address'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def migrate_from_matchv1_to_matchv2():
	session = DBSession()
	migrated_matches = []  # type: List[str]
	for match in session.query(MatchV1).all():  # type: MatchV1
		session.add(MatchV2(
			match_id=match.match_id, event_name=match.event_name, team_number=match.team_number,
			match_number=int(re.sub("[^0-9]", "", match.match_number)),
			auto_line_cross=match.auto_line_cross, auto_low_goal=match.auto_low_goal, auto_hopper=match.auto_hopper,
			auto_collect=match.auto_collect, auto_gear_pos=match.auto_gear_pos, auto_high_goal_pos=match.auto_high_goal_pos,
			climb_rating=match.climb_rating, gear_rating=match.gear_rating, total_gears=match.total_gears,
			gear_dispense_method=match.gear_dispense_method, got_gear_from_human=match.got_gear_from_human,
			got_gear_from_floor=match.got_gear_from_floor, high_goal_rating=match.high_goal_rating,
			high_goal_shoot_from_key=match.high_goal_shoot_from_key, high_goal_shoot_from_wall=match.high_goal_shoot_from_wall,
			high_goal_shoot_from_afar=match.high_goal_shoot_from_afar, low_goal_rating=match.low_goal_rating,
			total_hoppers=match.total_hoppers, collected_from_hopper=match.collected_from_hopper, last_modified=match.last_modified
		))
		migrated_matches.append(match.match_id)
	for migrated_match_id in migrated_matches:
		session.query(MatchV1).filter(MatchV1.match_id == migrated_match_id).delete()
	session.commit()
	session.close()


def migrate_matchv2_to_matchv3():
	session = DBSession()
	migrated_matches = []  # type: List[str]
	for match in session.query(MatchV2).all():  # type: MatchV2
		session.add(MatchV3(
			match_id=match.match_id,
			event_name=match.event_name,
			team_number=match.team_number,
			match_number=match.match_number,
			auto_line_cross=match.auto_line_cross,
			auto_low_goal=match.auto_low_goal,
			auto_hopper=match.auto_hopper,
			auto_collect=match.auto_collect,
			auto_gear_pos=match.auto_gear_pos,
			auto_high_goal_pos=match.auto_high_goal_pos,
			climb_rating=match.climb_rating,
			gear_rating=match.gear_rating,
			total_gears=match.total_gears,
			gear_dispense_method=match.gear_dispense_method,
			got_gear_from_human=match.got_gear_from_human,
			got_gear_from_floor=match.got_gear_from_floor,
			high_goal_rating=match.high_goal_rating,
			high_goal_shoot_from_key=match.high_goal_shoot_from_key,
			high_goal_shoot_from_wall=match.high_goal_shoot_from_wall,
			high_goal_shoot_from_afar=match.high_goal_shoot_from_afar,
			low_goal_rating=match.low_goal_rating,
			total_hoppers=match.total_hoppers,
			collected_from_hopper=match.collected_from_hopper,
			last_modified=match.last_modified,
			notes=''
		))
		migrated_matches.append(match.match_id)
	for migrated_match_id in migrated_matches:
		session.query(MatchV2).filter(MatchV2.match_id == migrated_match_id).delete()
	session.commit()
	session.close()


def migrate_matchv3_to_matchv4():
	session = DBSession()
	migrated_matches = []  # type: List[str]
	for match in session.query(MatchV3).all():  # type: MatchV3
		session.add(MatchV4(
			match_id=match.match_id,
			event_name=match.event_name,
			team_number=match.team_number,
			match_number=match.match_number,
			auto_line_cross=match.auto_line_cross,
			auto_low_goal=match.auto_low_goal,
			auto_hopper=match.auto_hopper,
			auto_collect=match.auto_collect,
			auto_gear_pos=match.auto_gear_pos,
			auto_high_goal_pos=match.auto_high_goal_pos,
			auto_kpa=0,
			climb_rating=match.climb_rating,
			gear_rating=match.gear_rating,
			total_gears=match.total_gears,
			total_kpa=0,
			gear_dispense_method=match.gear_dispense_method,
			got_gear_from_human=match.got_gear_from_human,
			got_gear_from_floor=match.got_gear_from_floor,
			high_goal_rating=match.high_goal_rating,
			high_goal_shoot_from_key=match.high_goal_shoot_from_key,
			high_goal_shoot_from_wall=match.high_goal_shoot_from_wall,
			high_goal_shoot_from_afar=match.high_goal_shoot_from_afar,
			low_goal_rating=match.low_goal_rating,
			total_hoppers=match.total_hoppers,
			collected_from_hopper=match.collected_from_hopper,
			collected_fuel_from_floor=False,
			last_modified=match.last_modified,
			notes=''
		))
		migrated_matches.append(match.match_id)
	for migrated_match_id in migrated_matches:
		session.query(MatchV3).filter(MatchV3.match_id == migrated_match_id).delete()
	session.commit()
	session.close()


def migrate_matchv4_to_matchv5():
	session = DBSession()
	migrated_matches = []  # type: List[str]
	for match in session.query(MatchV4).all():  # type: MatchV4
		session.add(MatchV5(
			match_id=match.match_id,
			event_name=match.event_name,
			team_number=match.team_number,
			match_number=match.match_number,
			auto_line_cross=match.auto_line_cross,
			auto_low_goal=match.auto_low_goal,
			auto_hopper=match.auto_hopper,
			auto_collect=match.auto_collect,
			auto_gear_pos=match.auto_gear_pos,
			auto_high_goal_pos=match.auto_high_goal_pos,
			auto_kpa=match.auto_kpa,
			climb_rating=match.climb_rating,
			gear_rating=match.gear_rating,
			total_gears=match.total_gears,
			total_kpa=match.total_kpa,
			gear_dispense_method=match.gear_dispense_method,
			got_gear_from_human=match.got_gear_from_human,
			got_gear_from_floor=match.got_gear_from_floor,
			high_goal_rating=match.high_goal_rating,
			high_goal_shoot_from_key=match.high_goal_shoot_from_key,
			high_goal_shoot_from_wall=match.high_goal_shoot_from_wall,
			high_goal_shoot_from_afar=match.high_goal_shoot_from_afar,
			low_goal_rating=match.low_goal_rating,
			total_hoppers=match.total_hoppers,
			collected_from_hopper=match.collected_from_hopper,
			collected_fuel_from_floor=match.collected_fuel_from_floor,
			last_modified=match.last_modified,
			notes=match.notes,
			scout_name='unknown'
		))
		migrated_matches.append(match.match_id)
	for migrated_match_id in migrated_matches:
		session.query(MatchV4).filter(MatchV4.match_id == migrated_match_id).delete()
	session.commit()
	session.close()
