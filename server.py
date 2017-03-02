# I know this isn't real rest, but your neither is your api.

from flask import Flask, request, jsonify, make_response, Response, url_for, render_template, redirect
import db_functions
import util
import exceptions
from settings import Settings
import json
from typing import Dict, List

server = Flask(__name__)

settings = Settings()


def home_cor(obj):
	return_response = make_response(obj)
	return_response.headers['Access-Control-Allow-Origin'] = "*"
	return_response.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS,PUT,DELETE'
	return_response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Origin, Accept"
	return return_response


@server.errorhandler(400)
def http_400(code: int, message: str, fields: str):
	"""

	:param code: The error code
	:param message: A message explaining the error
	:param fields: The variable
	:return:
	"""
	"""
	Error Codes:
	2 - Required JSON object missing in body
	3 - Required Parameter is Missing
	10 - Invalid Type for Required Parameter
	11 - Required Parameter Cannot Be Blank
	13 - Unique Value Required
	14 - Already Participating in Match
	15 - Team must register at Event first
	"""
	response_object = home_cor(Response(json.dumps({
		'code': code,
		'message': message,
		'fields': fields
	}), 400))
	response_object.headers['Content-Type'] = 'application/json'
	return response_object


@server.route('/api/events/create', methods=['OPTIONS', 'POST'])
def api_events_create():
	required_parameters = {
		'event_name': {
			'valid_types': [str],
			'value': None
		}
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				if type(parameter_value) in required_parameters[parameter_name]['valid_types'] is False:
					return http_400(10, 'Invalid Type for Required Parameter!', parameter_name)
				else:
					required_parameters[parameter_name]['value'] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	event_name = required_parameters['event_name']['value']  # type: str

	try:
		event_id = db_functions.create_event(event_name)
	except exceptions.EventNameMustBeUnique:
		return http_400(13, 'Unique Value Required', 'event_name')
	response['event_id'] = event_id
	return home_cor(jsonify(**response))


@server.route('/api/events/event/delete', methods=['OPTIONS', 'POST'])
def api_events_event_delete():
	required_parameters = {
		'event_id': {
			'valid_types': [str],
			'value': None
		}
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				if type(parameter_value) in required_parameters[parameter_name]['valid_types'] is False:
					return http_400(10, 'Invalid Type for Required Parameter!', parameter_name)
				else:
					required_parameters[parameter_name]['value'] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	event_id = required_parameters['event_id']['value']  # type: str

	db_functions.delete_event(event_id)

	response['success'] = True
	return home_cor(jsonify(**response))


@server.route('/api/events/all', methods=['OPTIONS', 'GET'])
def api_events_all():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	events = db_functions.all_events()

	response['events'] = events
	return home_cor(jsonify(**response))


@server.route('/api/event/details', methods=['OPTIONS', 'POST'])
def api_event_details():
	required_parameters = {
		'event_id': None
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				else:
					required_parameters[parameter_name] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	event_id = required_parameters['event_id']  # type: str

	try:
		event_details = db_functions.event_details(event_id)
	except exceptions.InvalidEventId:
		return http_400(5, 'Invalid Value', 'event_id')

	response['details'] = event_details
	return home_cor(jsonify(**response))


@server.route('/api/teams/all', methods=['OPTIONS', 'GET'])
def api_teams_all():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	response['teams'] = db_functions.all_teams()
	return home_cor(jsonify(**response))


@server.route('/api/teams/create', methods=['OPTIONS', 'POST'])
def api_teams_create():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	team_name = None
	team_number = None

	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			team_name = data.get('team_name', None)
			team_number = data.get('team_number', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if team_name is None:
		return http_400(3, 'Required Parameter is Missing', 'team_name')
	if team_number is None:
		return http_400(3, 'Required Parameter is Missing', 'team_number')

	team_name = team_name  # type: str
	try:
		team_number = int(team_number)
	except ValueError:
		return http_400(10, 'Required Parameter is not an Integer!', 'team_number')

	try:
		db_functions.create_team(team_name, team_number)
	except exceptions.TeamNumberTaken:
		return http_400(4, 'Value Required To Be Unique Not Unique', 'team_number')

	response['success'] = True
	return home_cor(jsonify(**response))


@server.route('/api/team/matches', methods=['OPTIONS', 'POST'])
def api_team_matches():
	required_parameters = {
		'team_number': None
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				else:
					required_parameters[parameter_name] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	team_number = required_parameters['team_number']  # type: int

	try:
		events = db_functions.team_matches(team_number)
	except exceptions.InvalidTeamNumber:
		return http_400(5, 'Invalid Value', 'team_number')

	response['events'] = events
	return home_cor(jsonify(**response))


@server.route('/api/team/details', methods=['OPTIONS', 'POST'])
def api_team_details():
	required_parameters = {
		'team_number': None
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				else:
					required_parameters[parameter_name] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	team_number = required_parameters['team_number']  # type: int

	try:
		details = db_functions.team_details(team_number)
	except exceptions.InvalidTeamNumber:
		return http_400(5, 'Invalid Value', 'team_number')

	response['details'] = details
	return home_cor(jsonify(**response))


@server.route('/api/team/events', methods=['OPTIONS', 'POST'])
def api_team_events():
	required_parameters = {
		'team_number': None
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				else:
					required_parameters[parameter_name] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	team_number = required_parameters['team_number']  # type: int

	try:
		events = db_functions.team_events(team_number)
	except exceptions.InvalidTeamNumber:
		return http_400(5, 'Invalid Value', 'team_number')

	response['events'] = events
	return home_cor(jsonify(**response))


@server.route('/api/team/notes/add', methods=['OPTIONS', 'POST'])
def api_team_notes_add():
	required_parameters = {
		'team_number': None,
		'message': None
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				else:
					required_parameters[parameter_name] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	team_number = required_parameters['team_number']  # type: int
	message = required_parameters['message']  # type: str

	try:
		note_id = db_functions.add_team_note(team_number, message)
	except exceptions.InvalidTeamNumber:
		return http_400(5, 'Invalid Value', 'team_number')

	response['note_id'] = note_id
	return home_cor(jsonify(**response))


@server.route('/api/team/note/edit', methods=['OPTIONS', 'POST'])
def api_team_note_edit():
	required_parameters = {
		'note_id': None,
		'message': None
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				else:
					required_parameters[parameter_name] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	note_id = required_parameters['note_id']  # type: str
	message = required_parameters['message']  # type: str

	try:
		note_id = db_functions.modify_team_note(note_id, message)
	except exceptions.InvalidTeamNoteId:
		return http_400(5, 'Invalid Value', 'note_id')

	response['success'] = True
	return home_cor(jsonify(**response))


@server.route('/api/event/teams/add', methods=['OPTIONS', 'POST'])
def api_event_teams_add():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	event_id = None
	team_number = None

	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			event_id = data.get('event_id', None)
			team_number = data.get('team_number', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if event_id is None:
		return http_400(3, 'Required Parameter is Missing', 'event_id')
	if team_number is None:
		return http_400(3, 'Required Parameter is Missing', 'team_number')

	try:
		db_functions.register_team_at_event(team_number, event_id)
	except exceptions.InvalidTeamNumber:
		return http_400(5, 'Invalid Value', 'team_number')
	except exceptions.InvalidEventId:
		return http_400(5, 'Invalid Value', 'event_id')

	response['success'] = True
	return home_cor(jsonify(**response))


@server.route('/api/matches/create', methods=['OPTIONS', 'POST'])
def api_matches_create():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	event_id = None
	match_number = None

	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			event_id = data.get('event_id', None)
			match_number = data.get('match_number', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if event_id is None:
		return http_400(3, 'Required Parameter is Missing', 'event_id')
	if match_number is None:
		return http_400(3, 'Required Parameter is Missing', 'match_number')

	try:
		match_number = int(match_number)
	except ValueError:
		return http_400(10, 'Required Parameter is not an Integer!', 'match_number')

	try:
		db_functions.create_match(event_id, match_number)
	except exceptions.InvalidEventId:
		return http_400(5, 'Invalid Value', 'event_id')

	response['success'] = True
	return home_cor(jsonify(**response))


@server.route('/api/match/add_team', methods=['OPTIONS', 'POST'])
def api_match_add_team():
	required_parameters = {
		'match_id': None,
		'team_number': None,
		'side': None
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				else:
					required_parameters[parameter_name] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	match_id = required_parameters['match_id']  # type: str
	team_number = required_parameters['team_number']  # type: int
	side = required_parameters['side']  # type: str

	try:
		db_functions.assign_team_to_match(match_id, team_number, side)
	except exceptions.InvalidMatchId:
		return http_400(5, 'Invalid Value', 'match_id')
	except exceptions.InvalidTeamNumber:
		return http_400(5, 'Invalid Value', 'team_number')
	except exceptions.TeamIsAlreadyInMatch:
		return http_400(14, 'Already Participating', 'team_number')
	except exceptions.TeamNeedsToBeRegisteredAtEvent:
		return http_400(15, 'Team Needs To Be Registered At Event', 'team_number')

	response['success'] = True
	return home_cor(jsonify(**response))


@server.route('/api/match/remove_team', methods=['OPTIONS', 'POST'])
def api_match_remove_team():
	required_parameters = {
		'match_id': None,
		'team_number': None
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				else:
					required_parameters[parameter_name] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	match_id = required_parameters['match_id']  # type: str
	team_number = required_parameters['team_number']  # type: int

	try:
		db_functions.remove_team_from_match(match_id, team_number)
	except exceptions.InvalidMatchId:
		return http_400(5, 'Invalid Value', 'match_id')
	except exceptions.InvalidTeamNumber:
		return http_400(5, 'Invalid Value', 'team_number')

	response['success'] = True
	return home_cor(jsonify(**response))


@server.route('/api/match/details', methods=['OPTIONS', 'POST'])
def api_match_details():
	required_parameters = {
		'match_id': None
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				else:
					required_parameters[parameter_name] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	match_id = required_parameters['match_id']  # type: str

	try:
		details = db_functions.match_details(match_id)
	except exceptions.InvalidMatchId:
		return http_400(5, 'Invalid Value', 'match_id')

	response['details'] = details
	return home_cor(jsonify(**response))


@server.route('/api/robots/add', methods=['OPTIONS', 'POST'])
def api_robots_add():
	required_parameters = {
		'robot_name': None,
		'team_number': None,
		'robot_type': None,
		'climbing_ability': None,
		'uses_actuated_gear_mechanism': None
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				else:
					required_parameters[parameter_name] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	robot_name = required_parameters['robot_name']  # type: str
	team_number = required_parameters['team_number']  # type: int
	robot_type = required_parameters['robot_type']  # type: str
	climbing_ability = required_parameters['climbing_ability']  # type: str
	uses_actuated_gear_mechanism = required_parameters['uses_actuated_gear_mechanism']  # type: bool

	try:
		robot_id = db_functions.create_robot(robot_name,
											 team_number,
											 robot_type,
											 climbing_ability,
											 uses_actuated_gear_mechanism)
	except exceptions.InvalidTeamNumber:
		return http_400(5, 'Invalid Value', 'team_number')

	response['robot_id'] = robot_id
	return home_cor(jsonify(**response))


@server.route('/api/robots/notes/add', methods=['OPTIONS', 'POST'])
def api_robots_notes_add():
	required_parameters = {
		'robot_id': None,
		'message': None
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				else:
					required_parameters[parameter_name] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	robot_id = required_parameters['robot_id']  # type: str
	message = required_parameters['message']  # type: str

	try:
		db_functions.add_robot_note(robot_id, message)
	except exceptions.InvalidRobotId:
		return http_400(5, 'Invalid Value', 'robot_id')

	response['success'] = True
	return home_cor(jsonify(**response))


@server.route('/api/robots/note/edit', methods=['OPTIONS', 'POST'])
def api_robots_note_edit():
	required_parameters = {
		'note_id': None,
		'message': None
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				else:
					required_parameters[parameter_name] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	note_id = required_parameters['note_id']  # type: str
	message = required_parameters['message']  # type: str

	try:
		db_functions.modify_robot_note(note_id, message)
	except exceptions.InvalidRobotNoteId:
		return http_400(5, 'Invalid Value', 'note_id')

	response['success'] = True
	return home_cor(jsonify(**response))


@server.route('/api/robot/edit', methods=['OPTIONS', 'POST'])
def api_robot_edit():
	required_parameters = {
		'robot_id': {
			'valid_types': [str],
			'value': None
		},
		'robot_name': {
			'valid_types': [str],
			'value': None
		},
		'team_number': {
			'valid_types': [int],
			'value': None
		},
		'robot_type': {
			'valid_types': [str],
			'value': None
		},
		'has_actuated_gear_mechanism': {
			'valid_types': [bool],
			'value': None
		}
	}

	# Generic Start #
	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(3, 'Required Parameter is Missing', parameter_name)
				if type(parameter_value) in required_parameters[parameter_name]['valid_types'] is False:
					return http_400(10, 'Invalid Type for Required Parameter!', parameter_name)
				else:
					required_parameters[parameter_name]['value'] = parameter_value
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	robot_id = required_parameters['robot_id']['value']  # type: str
	robot_name = required_parameters['robot_name']['value']  # type: str
	team_number = required_parameters['team_number']['value']  # type: int
	robot_type = required_parameters['robot_type']['value']  # type: str
	has_actuated_gear_mechanism = required_parameters['has_actuated_gear_mechanism']['value']  # type: bool

	try:
		db_functions.modify_robot_details(robot_id,
										  robot_name=robot_name,
										  robot_type=robot_type,
										  team_number=team_number,
										  has_actuated_gear_mechanism=has_actuated_gear_mechanism)
	except exceptions.InvalidRobotId:
		return http_400(5, 'Invalid Value', 'robot_id')

	response['robot_id'] = robot_id
	return home_cor(jsonify(**response))


@server.route('/app/')
@server.route('/app/home')
@server.route('/')
def app():
	return render_template('homepage/index.html')


@server.route('/app/events/all')
@server.route('/app/events')
def app_events():
	return render_template('events/all/index.html')


@server.route('/app/teams')
def app_teams():
	return render_template('teams/index.html')


@server.route('/app/teams/team')
def app_teams_team():
	return render_template('teams/team/index.html')


@server.route('/app/teams/create')
def app_teams_create():
	return render_template('teams/create/index.html')


@server.route('/app/events/create')
def app_events_create():
	return render_template('events/create/index.html')


@server.route('/app/events/event')
def app_events_event():
	return render_template('events/event/index.html')


@server.route('/app/matches/match')
def app_matches_match():
	return render_template('matches/match/index.html')


print(f'Using Database: {settings.database_address}')

server.run(debug=True, host='0.0.0.0', port=8881)
