# I know this isn't real rest, but your neither is your api.

from flask import Flask, request, jsonify, make_response, abort, Response, url_for
import db_functions
import util
import exceptions
from settings import Settings
import json
from typing import Dict, List

app = Flask(__name__)

settings = Settings()


def home_cor(obj):
	return_response = make_response(obj)
	return_response.headers['Access-Control-Allow-Origin'] = "*"
	return_response.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS,PUT,DELETE'
	return_response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Origin, Accept"
	return return_response


@app.errorhandler(400)
def http_400(code: int, message: str, fields: str):
	"""

	:param code: The error code
	:param message: A message explaining the error
	:param fields: The variable
	:return:
	"""
	"""
	Error Codes:
	"""
	response_object = home_cor(Response(json.dumps({
		'code': code,
		'message': message,
		'fields': fields
	}), 400))
	response_object.headers['Content-Type'] = 'application/json'
	return response_object


print(f'Using Database: {settings.database_address}')


@app.route('/events/create', methods=['OPTIONS', 'POST'])
def events_create():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	event_name = None

	if request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			event_name = data.get('event_name', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if event_name is None:
		return http_400(3, 'Required Parameter is Missing', 'event_name')

	event_id = db_functions.create_event(event_name)

	response['event_id'] = event_id
	return home_cor(jsonify(**response))


@app.route('/teams/all', methods=['OPTIONS', 'GET'])
def teams_all():
	pass


@app.route('/teams/create', methods=['OPTIONS', 'POST'])
def teams_create():
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

	try:
		db_functions.create_team(team_name, team_number)
	except exceptions.TeamNumberTaken:
		return http_400(4, 'Value Required To Be Unique Not Unique', 'team_number')

	response['success'] = True
	return home_cor(jsonify(**response))


@app.route('/team/matches', methods=['OPTIONS', 'POST'])
def team_matches():
	pass


@app.route('/team/details', methods=['OPTIONS', 'POST'])
def team_details():
	pass


@app.route('/team/events', methods=['OPTIONS', 'POST'])
def team_events():
	pass


@app.route('/team/notes/add', methods=['OPTIONS', 'POST'])
def team_notes_add():
	pass


@app.route('/team/note/edit', methods=['OPTIONS', 'POST'])
def team_note_edit():
	pass


@app.route('/event/teams/add', methods=['OPTIONS', 'POST'])
def event_teams_add():
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


@app.route('/matches/create', methods=['OPTIONS', 'POST'])
def matches_create():
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
		db_functions.create_match(event_id, match_number)
	except exceptions.InvalidEventId:
		return http_400(5, 'Invalid Value', 'event_id')

	response['success'] = True
	return home_cor(jsonify(**response))


@app.route('/match/add_team', methods=['OPTIONS', 'POST'])
def match_add_team():
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

	response['success'] = True
	return home_cor(jsonify(**response))


@app.route('/match/remove_team', methods=['OPTIONS', 'POST'])
def match_remove_team():
	pass


@app.route('/match/details', methods=['OPTIONS', 'POST'])
def match_details():
	pass


@app.route('/robots/add', methods=['OPTIONS', 'POST'])
def robots_add():
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


@app.route('/robots/notes/add', methods=['OPTIONS', 'POST'])
def robots_notes_add():
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


@app.route('/robots/note/edit', methods=['OPTIONS', 'POST'])
def robots_note_edit():
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


@app.route('/robot/edit', methods=['OPTIONS', 'POST'])
def robot_edit():
	


app.run(debug=True, host='0.0.0.0', port=8881)
