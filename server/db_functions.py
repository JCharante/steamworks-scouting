from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, MatchV1, MatchV2, MatchV3
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


def add_matchv3(match_id: str,
				event_name: str,
				team_number: int,
				match_number: int,
				auto_line_cross: bool,
				auto_low_goal: bool,
				auto_hopper: bool,
				auto_collect: bool,
				auto_gear_pos: str,
				auto_high_goal_pos: str,
				climb_rating: str,
				gear_rating: str,
				total_gears: int,
				gear_dispense_method: str,
				got_gear_from_human: bool,
				got_gear_from_floor: bool,
				high_goal_rating: str,
				high_goal_shoot_from_key: bool,
				high_goal_shoot_from_wall: bool,
				high_goal_shoot_from_afar: bool,
				low_goal_rating: str,
				total_hoppers: int,
				collected_from_hopper: bool,
				last_modified: str,
				notes: str) -> None:

	session = DBSession()
	stored_match = session.query(MatchV3).filter(MatchV3.match_id == match_id).first()
	if stored_match is not None:
		stored_match = stored_match  # type: MatchV3
		stored_match_last_modified_date = dateutil.parser.parse(stored_match.last_modified)
		new_match_last_modified_date = dateutil.parser.parse(last_modified)
		if stored_match_last_modified_date > new_match_last_modified_date:
			raise exceptions.MatchDataOutdated()
		else:
			session.query(MatchV3).filter(MatchV3.match_id == match_id).delete()
	session.add(MatchV3(
		match_id=match_id,
		event_name=event_name,
		team_number=team_number,
		match_number=match_number,
		auto_line_cross=auto_line_cross,
		auto_low_goal=auto_low_goal,
		auto_hopper=auto_hopper,
		auto_collect=auto_collect,
		auto_gear_pos=auto_gear_pos,
		auto_high_goal_pos=auto_high_goal_pos,
		climb_rating=climb_rating,
		gear_rating=gear_rating,
		total_gears=total_gears,
		gear_dispense_method=gear_dispense_method,
		got_gear_from_human=got_gear_from_human,
		got_gear_from_floor=got_gear_from_floor,
		high_goal_rating=high_goal_rating,
		high_goal_shoot_from_key=high_goal_shoot_from_key,
		high_goal_shoot_from_wall=high_goal_shoot_from_wall,
		high_goal_shoot_from_afar=high_goal_shoot_from_afar,
		low_goal_rating=low_goal_rating,
		total_hoppers=total_hoppers,
		collected_from_hopper=collected_from_hopper,
		last_modified=last_modified,
		notes=notes
	))
	session.commit()
	session.close()


def events_recorded():
	session = DBSession()
	events = [event_name for event_name in session.query(MatchV3.event_name).distinct()]
	session.close()
	return events


def matrix_data_for_event(event_name):
	session = DBSession()
	matrix = []
	header_row = ['Match ID', 'Event Name', 'Team Number', 'Match Number (Q)', 'Auto: Crossed Line', 'Auto: Scored Low Goal', 'Auto: Hopper', 'Auto: Collected from Hopper', 'Auto: Gear Position', 'Auto: High Goal Position',
				  'Climb Rating', 'Gear Rating', 'Total number of Gears', 'Gear Dispense Method', 'Got Gear from Human Play', 'Got Gear from Floor', 'High Goal Shooting Rating', 'Shot High Goal from Key',
				  'Shot High Goal from Wall', 'Shot High Goal from Afar', 'Low Goal Rating', 'Total number of Hoppers', 'Collected from Hopper', 'Data last Modified', 'Notes']
	matrix.append(header_row)
	for match in session.query(MatchV3).filter(MatchV3.event_name == event_name).all():  # type: MatchV3
		row = [match.match_id,
			   match.event_name,
			   match.team_number,
			   match.match_number,
			   match.auto_line_cross,
			   match.auto_low_goal,
			   match.auto_hopper,
			   match.auto_collect,
			   match.auto_gear_pos,
			   match.auto_high_goal_pos,
			   match.climb_rating,
			   match.gear_rating,
			   match.total_gears,
			   match.gear_dispense_method,
			   match.got_gear_from_human,
			   match.got_gear_from_floor,
			   match.high_goal_rating,
			   match.high_goal_shoot_from_key,
			   match.high_goal_shoot_from_wall,
			   match.high_goal_shoot_from_afar,
			   match.low_goal_rating,
			   match.total_hoppers,
			   match.collected_from_hopper,
			   match.last_modified,
			   match.notes]
		matrix.append(row)
	session.close()
	return matrix
