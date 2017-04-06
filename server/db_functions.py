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


def upload_matches(matches: List[Dict], server_password) -> None:
	if server_password != os.environ['serverPassword']:
		raise exceptions.GenericException(3, 'Not Authorized', 'serverPassword')

	for match in matches:
		match_id = match.get('match_id', None)
		event_name = match.get('event_name', None)
		team_number = match.get('team_number', None)
		match_number = match.get('match_number', None)
		auto_line_cross = match.get('auto_line_cross', None)
		auto_low_goal = match.get('auto_low_goal', None)
		auto_hopper = match.get('auto_hopper', None)
		auto_collect = match.get('auto_collect', None)
		auto_gear_pos = match.get('auto_gear_pos', None)
		auto_kpa = match.get('auto_kpa', None)
		auto_high_goal_pos = match.get('auto_high_goal_pos', None)
		climb_rating = match.get('climb_rating', None)
		gear_rating = match.get('gear_rating', None)
		total_gears = match.get('total_gears', None)
		total_kpa = match.get('total_kpa', None)
		gear_dispense_method = match.get('gear_dispense_method', None)
		got_gear_from_human = match.get('got_gear_from_human', None)
		got_gear_from_floor = match.get('got_gear_from_floor', None)
		high_goal_rating = match.get('high_goal_rating', None)
		high_goal_shoot_from_key = match.get('high_goal_shoot_from_key', None)
		high_goal_shoot_from_wall = match.get('high_goal_shoot_from_wall', None)
		high_goal_shoot_from_afar = match.get('high_goal_shoot_from_afar', None)
		low_goal_rating = match.get('low_goal_rating', None)
		total_hoppers = match.get('total_hoppers', None)
		collected_from_hopper = match.get('collected_from_hopper', None)
		collected_fuel_from_floor = match.get('collected_fuel_from_floor', None)
		last_modified = match.get('last_modified', None)
		notes = match.get('notes', None)
		scout_name = match.get('scout_name', None)

		if type(match_id) is not str:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'match_id')
		match_id = match_id  # type: str
		if len(match_id) > 36:
			raise exceptions.GenericException(2, 'String Too Long', 'match_id')

		if type(event_name) is not str:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'event_name')
		event_name = event_name  # type: str
		if len(event_name) > 100:
			raise exceptions.GenericException(2, 'String Too Long', 'event_name')

		if type(team_number) is not int:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'team_number')
		team_number = team_number  # type: int

		if type(match_number) is not int:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'match_number')
		match_number = match_number  # type: int

		if type(auto_line_cross) is not bool:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'auto_line_cross')
		auto_line_cross = auto_line_cross  # type: bool

		if type(auto_low_goal) is not bool:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'auto_low_goal')
		auto_low_goal = auto_low_goal  # type: bool

		if type(auto_hopper) is not bool:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'auto_hopper')
		auto_hopper = auto_hopper  # type: bool

		if type(auto_collect) is not bool:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'auto_collect')
		auto_collect = auto_collect  # type: bool

		if type(auto_gear_pos) is not str:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'auto_gear_pos')
		auto_gear_pos = auto_gear_pos  # type: str
		if len(auto_gear_pos) > 10:
			raise exceptions.GenericException(2, 'String Too Long', 'auto_gear_pos')

		if type(auto_kpa) is not int:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'auto_kpa')
		auto_kpa = auto_kpa  # type: int

		if type(auto_high_goal_pos) is not str:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'auto_high_goal_pos')
		auto_high_goal_pos = auto_high_goal_pos  # type: str
		if len(auto_high_goal_pos) > 10:
			raise exceptions.GenericException(2, 'String Too Long', 'auto_high_goal_pos')

		if type(climb_rating) is not str:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'climb_rating')
		climb_rating = climb_rating  # type: str
		if len(climb_rating) > 10:
			raise exceptions.GenericException(2, 'String Too Long', 'climb_rating')

		if type(gear_rating) is not str:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'gear_rating')
		gear_rating = gear_rating  # type: str

		if type(total_gears) is not int:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'total_gears')
		total_gears = total_gears  # type: int

		if type(total_kpa) is not int:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'total_kpa')
		total_kpa = total_kpa  # type: int

		if type(gear_dispense_method) is not str:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'gear_dispense_method')
		gear_dispense_method = gear_dispense_method  # type: str

		if type(got_gear_from_human) is not bool:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'got_gear_from_human')
		got_gear_from_human = got_gear_from_human  # type: bool

		if type(got_gear_from_floor) is not bool:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'got_gear_from_floor')
		got_gear_from_floor = got_gear_from_floor  # type: bool

		if type(high_goal_rating) is not str:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'high_goal_rating')
		high_goal_rating = high_goal_rating  # type: str
		if len(high_goal_rating) > 10:
			raise exceptions.GenericException(2, 'String Too Long', 'high_goal_rating')

		if type(high_goal_shoot_from_key) is not bool:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'high_goal_shoot_from_key')
		high_goal_shoot_from_key = high_goal_shoot_from_key  # type: bool

		if type(high_goal_shoot_from_wall) is not bool:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'high_goal_shoot_from_wall')
		high_goal_shoot_from_wall = high_goal_shoot_from_wall  # type: bool

		if type(high_goal_shoot_from_afar) is not bool:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'high_goal_shoot_from_afar')
		high_goal_shoot_from_afar = high_goal_shoot_from_afar  # type: bool

		if type(low_goal_rating) is not str:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'low_goal_rating')
		low_goal_rating = low_goal_rating  # type: str
		if len(low_goal_rating) > 10:
			raise exceptions.GenericException(2, 'String Too Long', 'low_goal_rating')

		if type(total_hoppers) is not int:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'total_hoppers')
		total_hoppers = total_hoppers  # type: int

		if type(collected_from_hopper) is not bool:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'collected_from_hopper')
		collected_from_hopper = collected_from_hopper  # type: bool

		if type(collected_fuel_from_floor) is not bool:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'collected_fuel_from_floor')
		collected_fuel_from_floor = collected_fuel_from_floor  # type: bool

		if type(last_modified) is not str:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'last_modified')
		last_modified = last_modified  # type: str
		if len(last_modified) > 30:
			raise exceptions.GenericException(2, 'String Too Long', 'climb_rating')

		if type(notes) is not str:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'notes')
		notes = notes  # type: str
		if len(notes) > 200:
			raise exceptions.GenericException(2, 'String Too Long', 'notes')

		if type(scout_name) is not str:
			raise exceptions.GenericException(1, 'Invalid Data Type', 'scout_name')
		scout_name = scout_name  # type: str
		if len(scout_name) > 30:
			raise exceptions.GenericException(2, 'String Too Long', 'scout_name')

		try:
			add_matchv5(match_id=match_id,
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
						scout_name=scout_name)
		except exceptions.MatchDataOutdated:
			pass


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
			session.close()
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
