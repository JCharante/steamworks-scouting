from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, MatchV5
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


def add_matchv5(match_id: str,
				event_name: str,
				team_number: int,
				match_number: int,
				auto_line_cross: bool,
				auto_low_goal: bool,
				auto_hopper: bool,
				auto_collect: bool,
				auto_gear_pos: str,
				auto_high_goal_pos: str,
				auto_kpa: int,
				climb_rating: str,
				gear_rating: str,
				total_gears: int,
				total_kpa: int,
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
				collected_fuel_from_floor: bool,
				last_modified: str,
				notes: str,
                scout_name: str) -> None:

	session = DBSession()
	stored_match = session.query(MatchV5).filter(MatchV5.match_id == match_id).first()
	if stored_match is not None:
		stored_match = stored_match  # type: MatchV5
		stored_match_last_modified_date = dateutil.parser.parse(stored_match.last_modified)
		new_match_last_modified_date = dateutil.parser.parse(last_modified)
		if stored_match_last_modified_date > new_match_last_modified_date:
			raise exceptions.MatchDataOutdated()
		else:
			session.query(MatchV5).filter(MatchV5.match_id == match_id).delete()
	session.add(MatchV5(
		match_id=match_id,
		event_name=event_name,
		team_number=team_number,
		match_number=match_number,
		auto_line_cross=auto_line_cross,
		auto_low_goal=auto_low_goal,
		auto_hopper=auto_hopper,
		auto_collect=auto_collect,
		auto_gear_pos=auto_gear_pos,
		auto_kpa=auto_kpa,
		auto_high_goal_pos=auto_high_goal_pos,
		climb_rating=climb_rating,
		gear_rating=gear_rating,
		total_gears=total_gears,
		total_kpa=total_kpa,
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
		collected_fuel_from_floor=collected_fuel_from_floor,
		last_modified=last_modified,
		notes=notes,
		scout_name=scout_name
	))
	session.commit()
	session.close()


def events_recorded():
	session = DBSession()
	events = [event_name for event_name in session.query(MatchV5.event_name).distinct()]
	session.close()
	return events


def matrix_data_for_event(event_name):
	session = DBSession()
	matrix = []
	header_row = ['Match ID',
				  'Event Name',
				  'Team Number',
				  'Match Number (Q)',
				  'Auto: Crossed Line',
				  'Auto: Scored Low Goal',
				  'Auto: Hopper',
				  'Auto: Collected from Hopper',
				  'Auto: Gear Position',
				  'Auto: kPa',
				  'Auto: High Goal Position',
				  'Climb Rating',
				  'Gear Rating',
				  'Total number of Gears',
				  'Total kPa',
				  'Gear Dispense Method',
				  'Got Gear from Human Play',
				  'Got Gear from Floor',
				  'High Goal Shooting Rating',
				  'Shot High Goal from Key',
				  'Shot High Goal from Wall',
				  'Shot High Goal from Afar',
				  'Low Goal Rating',
				  'Total number of Hoppers',
				  'Collected from Hopper',
				  'Collected Fuel from Floor',
				  'Data last Modified',
				  'Notes',
	              'Scout Name']
	matrix.append(header_row)
	for match in session.query(MatchV5).filter(MatchV5.event_name == event_name).all():  # type: MatchV5
		row = [match.match_id,
			   match.event_name,
			   match.team_number,
			   match.match_number,
			   match.auto_line_cross,
			   match.auto_low_goal,
			   match.auto_hopper,
			   match.auto_collect,
			   match.auto_gear_pos,
			   match.auto_kpa,
			   match.auto_high_goal_pos,
			   match.climb_rating,
			   match.gear_rating,
			   match.total_gears,
			   match.total_kpa,
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
			   match.collected_fuel_from_floor,
			   match.last_modified,
			   match.notes,
		       match.scout_name]
		matrix.append(row)
	session.close()
	return matrix


def matches_array():
	session = DBSession()
	matches = []
	for match in session.query(MatchV5).all():
		matches.append({
			'match_id': match.match_id,
			'event_name': match.event_name,
			'team_number': match.team_number,
			'match_number': match.match_number,
			'auto_line_cross': match.auto_line_cross,
			'auto_low_goal': match.auto_low_goal,
			'auto_hopper': match.auto_hopper,
			'auto_collect': match.auto_collect,
			'auto_gear_pos': match.auto_gear_pos,
			'auto_kpa': match.auto_kpa,
			'auto_high_goal_pos': match.auto_high_goal_pos,
			'climb_rating': match.climb_rating,
			'gear_rating': match.gear_rating,
			'total_gears': match.total_gears,
			'total_kpa': match.total_kpa,
			'gear_dispense_method': match.gear_dispense_method,
			'got_gear_from_human': match.got_gear_from_human,
			'got_gear_from_floor': match.got_gear_from_floor,
			'high_goal_rating': match.high_goal_rating,
			'high_goal_shoot_from_key': match.high_goal_shoot_from_key,
			'high_goal_shoot_from_wall': match.high_goal_shoot_from_wall,
			'high_goal_shoot_from_afar': match.high_goal_shoot_from_afar,
			'low_goal_rating': match.low_goal_rating,
			'total_hoppers': match.total_hoppers,
			'collected_from_hopper': match.collected_from_hopper,
			'collected_fuel_from_floor': match.collected_fuel_from_floor,
			'last_modified': match.last_modified,
			'notes': match.notes,
			'scout_name': match.scout_name
		})
	session.close()
	return matches
