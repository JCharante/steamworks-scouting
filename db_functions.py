from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db_setup import Base, MatchV1, TeamAtEventV1, TeamV1, TeamAtMatchV1, EventV1, RobotNoteV1, RobotV1, TeamNoteV1
import util
import uuid
from settings import Settings
from typing import Tuple, List, Dict
import exceptions


settings = Settings()
# Connects to the database
engine = create_engine(settings.database_address)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def create_event(event_name: str) -> str:
	"""
	Creates an event and returns the event id
	:param event_name: The name of the event 
	:return: The event id
	"""
	session = DBSession()
	event_id = str(uuid.uuid4())
	session.add(EventV1(event_name=event_name,
						event_id=event_id))
	session.commit()
	session.close()
	return event_id


def unique_team_number(team_number: int) -> bool:
	"""
	Checks if a team number is unique in the database
	:param team_number: The number of the team
	:return: 
	"""
	session = DBSession()
	team = session.query(TeamV1).filter(TeamV1.team_number == team_number).first()
	session.close()
	return team is None


def create_team(team_name: str, team_number: int) -> None:
	"""
	Creates a team
	:param team_name: The name of the team 
	:param team_number: The team number (eg 5687)
	:return: 
	"""
	session = DBSession()
	if unique_team_number(team_number) is False:
		session.close()
		raise exceptions.TeamNumberTaken()
	session.add(TeamV1(
		team_name=team_name,
		team_number=team_number
	))
	session.commit()
	session.close()


def valid_team_number(team_number: int) -> bool:
	session = DBSession()
	team = session.query(TeamV1).filter(TeamV1.team_number == team_number).first()
	session.close()
	return team is not None


def valid_event_id(event_id: str) -> bool:
	session = DBSession()
	event = session.query(EventV1).filter(EventV1.event_id == event_id).first()
	session.close()
	return event is not None


def valid_match_id(match_id: str) -> bool:
	session = DBSession()
	match = session.query(MatchV1).filter(MatchV1.match_id == match_id).first()
	session.close()
	return match is not None


def valid_robot_id(robot_id: str) -> bool:
	session = DBSession()
	robot = session.query(RobotV1).filter(RobotV1.robot_id == robot_id).first()
	session.close()
	return robot is not None


def valid_team_note_id(team_note_id: str) -> bool:
	session = DBSession()
	note = session.query(TeamNoteV1).filter(TeamNoteV1.note_id == team_note_id).first()
	session.close()
	return note is not None


def valid_robot_note_id(robot_note_id: str) -> bool:
	session = DBSession()
	note = session.query(RobotNoteV1).filter(RobotNoteV1.note_id == robot_note_id).first()
	session.close()
	return note is not None


def register_team_at_event(team_number: int, event_id: str) -> None:
	if valid_team_number(team_number) is False:
		raise exceptions.InvalidTeamNumber()
	if valid_event_id(event_id) is False:
		raise exceptions.InvalidEventId()
	session = DBSession()
	session.add(TeamAtEventV1(
		team_number=team_number,
		event_id=event_id
	))
	session.commit()
	session.close()


def create_match(event_id: str, match_number: int) -> str:
	if valid_event_id(event_id) is False:
		raise exceptions.InvalidEventId()
	session = DBSession()
	match_id = str(uuid.uuid4())
	session.add(MatchV1(
		blue_score=0,
		red_score=0,
		match_id=match_id,
		match_number=match_number,
		event_id=event_id
	))
	session.commit()
	session.close()
	return match_id


def assign_team_to_match(match_id: str, team_number: int, side: str) -> None:
	if valid_match_id(match_id) is False:
		raise exceptions.InvalidMatchId()
	if valid_team_number(team_number) is False:
		raise exceptions.InvalidTeamNumber()
	session = DBSession()
	if session.query(TeamAtMatchV1).filter(TeamAtMatchV1.match_id == match_id).filter(TeamAtMatchV1.team_number == team_number).first() is not None:
		raise exceptions.TeamIsAlreadyInMatch()
	session.add(TeamAtMatchV1(
		team_number=team_number,
		match_id=match_id,
		cycle_time=0.0,
		rp=0,
		side=side
	))
	session.commit()
	session.close()


def remove_team_from_match(match_id: str, team_number: int) -> None:
	if valid_match_id(match_id) is False:
		raise exceptions.InvalidMatchId()
	if valid_team_number(team_number) is False:
		raise exceptions.InvalidTeamNumber()
	session = DBSession()
	session.query(TeamAtMatchV1).filter(TeamAtMatchV1.match_id == match_id).filter(TeamAtMatchV1.team_number == team_number).delete()
	session.commit()
	session.close()


def create_robot(robot_name: str, team_number: int, robot_type: str, climbing_ability: str,
				 uses_actuated_gear_mechanism: bool) -> str:
	if valid_team_number(team_number) is False:
		raise exceptions.InvalidTeamNumber()
	robot_id = str(uuid.uuid4())
	session = DBSession()
	session.add(RobotV1(
		robot_name=robot_name,
		robot_id=robot_id,
		team_number=team_number,
		robot_type=robot_type,
		climbing_ability=climbing_ability,
		uses_actuated_gear_mechanism=uses_actuated_gear_mechanism
	))
	session.commit()
	session.close()
	return robot_id


def add_team_note(team_number: int, message: str):
	if valid_team_number(team_number) is False:
		raise exceptions.InvalidTeamNumber()
	note_id = str(uuid.uuid4())
	session = DBSession()
	session.add(TeamNoteV1(
		team_number=team_number,
		note=message,
		note_id=note_id
	))
	session.commit()
	session.close()
	return note_id


def add_robot_note(robot_id: str, message: str):
	if valid_robot_id(robot_id) is False:
		raise exceptions.InvalidRobotId()
	note_id = str(uuid.uuid4())
	session = DBSession()
	session.add(RobotNoteV1(
		robot_id=robot_id,
		note=message,
		note_id=note_id
	))
	session.commit()
	session.close()
	return note_id


def modify_robot_details(robot_id: str, robot_name=None, robot_type=None, team_number=None, climbing_ability=None,
						 uses_actuated_gear_mechanism=None):
	if valid_robot_id(robot_id) is False:
		raise exceptions.InvalidRobotId()
	session = DBSession()
	robot = session.query(RobotV1).filter(RobotV1.robot_id == robot_id).first()  # type: RobotV1
	if robot_name is not None:
		robot.robot_name = robot_name
	if robot_type is not None:
		robot.robot_type = robot_type
	if team_number is not None:
		robot.team_number = team_number
	if climbing_ability is not None:
		robot.climbing_ability = climbing_ability
	if uses_actuated_gear_mechanism is not None:
		robot.uses_actuated_gear_mechanism = uses_actuated_gear_mechanism
	session.commit()
	session.close()


def modify_team_note(note_id: str, new_message: str):
	if valid_team_note_id(note_id) is False:
		raise exceptions.InvalidTeamNoteId()
	session = DBSession()
	note = session.query(TeamNoteV1).filter(TeamNoteV1.note_id == note_id).first()  # type: TeamNoteV1
	note.note = new_message
	session.commit()
	session.close()


def modify_robot_note(note_id: str, new_message: str):
	if valid_robot_note_id(note_id) is False:
		raise exceptions.InvalidRobotNoteId()
	session = DBSession()
	note = session.query(RobotNoteV1).filter(RobotNoteV1.note_id == note_id).first()  # type: RobotNoteV1
	note.note = new_message
	session.commit()
	session.close()


def all_teams():
	session = DBSession()
	teams = []
	for team in session.query(TeamV1).all():
		team = team  # type: TeamV1
		teams.append({
			'team_number': team.team_number,
			'team_name': team.team_name
		})
	session.close()
	return teams


def teams_at_event(event_id: str):
	if valid_event_id(event_id) is False:
		raise exceptions.InvalidEventId()
	teams = []
	session = DBSession()
	for team_at_event_v1 in session.query(TeamAtEventV1).filter(TeamAtEventV1.event_id == event_id).all():  # type: TeamAtEventV1
		team = session.query(TeamV1).filter(TeamV1.team_number == team_at_event_v1.team_number).first()
		teams.append({
			'team_number': team.team_number,
			'team_name': team.team_name
		})
	session.close()
	return teams


def team_matches(team_number: int):
	if valid_team_number(team_number) is False:
		raise exceptions.InvalidTeamNumber()
	session = DBSession()
	matches = {}
	for team_at_match in session.query(TeamAtMatchV1).filter(TeamAtMatchV1.team_number == team_number).all():  # type: TeamAtMatchV1
		match = session.query(MatchV1).filter(MatchV1.match_id == team_at_match.match_id).first()  # type: MatchV1
		event = session.query(EventV1).filter(EventV1.event_id == match.event_id).first()  # type: EventV1
		matches[event.event_id] = {
			'event_id': event.event_id,
			'event_name': event.event_name,
			'matches': matches.get(event.event_id, {}).get('matches', []).append({
				'match_id': match.match_id,
				'match_number': match.match_number
			})
		}
		session.close()
	return matches


def match_details(match_id: str):
	if valid_match_id(match_id) is False:
		raise exceptions.InvalidMatchId()
	session = DBSession()
	details = {
		'blue_team': [],
		'red_team': []
	}
	for team_at_match in session.query(TeamAtMatchV1).filter(TeamAtMatchV1.match_id == match_id).all():  # type: TeamAtMatchV1
		if team_at_match.side == 'red':
			details['red_team'].append(team_at_match.team_number)
		if team_at_match.side == 'blue':
			details['blue_team'].append(team_at_match.team_number)
	match = session.query(MatchV1).filter(MatchV1.match_id == match_id).first()  # type: MatchV1
	event = session.query(EventV1).filter(EventV1.event_id == match.event_id).first()  # type: EventV1
	details['event_id'] = match.event_id
	details['event_name'] = event.event_name
	details['match_number'] = match.match_number
	details['match_id'] = match_id
	details['score'] = {
		'red_score': match.red_score,
		'blue_score': match.blue_score
	}
	session.close()
	return details


def all_events():
	session = DBSession()
	events = []
	for event in session.query(EventV1).all():  # type: EventV1
		events.append({
			'event_id': event.event_id,
			'event_name': event.event_name
		})
	return events


def matches_at_event(event_id: str):
	if valid_event_id(event_id) is False:
		raise exceptions.InvalidEventId()
	session = DBSession()
	matches = []
	for match in session.query(MatchV1).filter(MatchV1.event_id == event_id).all():  # type: MatchV1
		matches.append({
			'match_id': match.match_id,
			'match_number': match.match_number
		})
	session.close()
	return matches


def event_details(event_id: str):
	if valid_event_id(event_id) is False:
		raise exceptions.InvalidMatchId()
	session = DBSession()
	event_detail = dict()
	event_detail['matches'] = matches_at_event(event_id)
	event = session.query(EventV1).filter(EventV1.event_id == event_id).first()  # type: EventV1
	event_detail['name'] = event.event_name
	event_detail['event_id'] = event.event_id
	session.close()
	return event_detail


def team_events(team_number: int) -> List[Dict[str, str]]:
	"""
	Get the events that a team is in
	:param team_number:
	:return:
	"""
	if valid_team_number(team_number) is False:
		raise exceptions.InvalidTeamNumber()
	session = DBSession()
	events = []
	for team_at_event_v1 in session.query(TeamAtEventV1).filter(TeamAtEventV1.team_number == team_number).all():  # type: TeamAtEventV1
		event = session.query(EventV1).filter(EventV1.event_id == team_at_event_v1.event_id).first()
		events.append({
			'event_name': event.event_name,
			'event_id': event.event_id
		})
	session.close()
	return events


def team_details(team_number: int):
	if valid_team_number(team_number) is False:
		raise exceptions.InvalidTeamNumber()
	session = DBSession()
	team = session.query(TeamV1).filter(TeamV1.team_number == team_number).first()
	session.close()
	return {
		'team_number': team.team_number,
		'team_name': team.team_name
	}

