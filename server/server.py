from flask import Flask, request, make_response, Response, jsonify, render_template
import flask_excel as excel
import json
import os
from typing import List, Dict
import db_functions
import exceptions
import migration

migration.migrate_from_matchv1_to_matchv2()
migration.migrate_matchv2_to_matchv3()
migration.migrate_matchv3_to_matchv4()
migration.migrate_matchv4_to_matchv5()
app = Flask(__name__)


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


@app.route('/')
def api_root():
	return render_template('index.html')


@app.route('/match/upload', methods=['OPTIONS', 'POST'])
def api_match_upload():
	required_parameters = {
		'matches': {
			'valid_types': [list],
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

	matches = required_parameters['matches']['value']  # type: List[Dict]

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
			return http_400(1, 'Invalid Data Type', 'match_id')
		match_id = match_id  # type: str

		if type(event_name) is not str:
			return http_400(1, 'Invalid Data Type', 'event_name')
		event_name = event_name  # type: str

		if type(team_number) is not int:
			return http_400(1, 'Invalid Data Type', 'team_number')
		team_number = team_number  # type: int

		if type(match_number) is not int:
			return http_400(1, 'Invalid Data Type', 'match_number')
		match_number = match_number  # type: int

		if type(auto_line_cross) is not bool:
			return http_400(1, 'Invalid Data Type', 'auto_line_cross')
		auto_line_cross = auto_line_cross  # type: bool

		if type(auto_low_goal) is not bool:
			return http_400(1, 'Invalid Data Type', 'auto_low_goal')
		auto_low_goal = auto_low_goal  # type: bool

		if type(auto_hopper) is not bool:
			return http_400(1, 'Invalid Data Type', 'auto_hopper')
		auto_hopper = auto_hopper  # type: bool

		if type(auto_collect) is not bool:
			return http_400(1, 'Invalid Data Type', 'auto_collect')
		auto_collect = auto_collect  # type: bool

		if type(auto_gear_pos) is not str:
			return http_400(1, 'Invalid Data Type', 'auto_gear_pos')
		auto_gear_pos = auto_gear_pos  # type: str

		if type(auto_kpa) is not int:
			return http_400(1, 'Invalid Data Type', 'auto_kpa')
		auto_kpa = auto_kpa  # type: int

		if type(auto_high_goal_pos) is not str:
			return http_400(1, 'Invalid Data Type', 'auto_high_goal_pos')
		auto_high_goal_pos = auto_high_goal_pos  # type: str

		if type(climb_rating) is not str:
			return http_400(1, 'Invalid Data Type', 'climb_rating')
		climb_rating = climb_rating  # type: str

		if type(gear_rating) is not str:
			return http_400(1, 'Invalid Data Type', 'gear_rating')
		gear_rating = gear_rating  # type: str

		if type(total_gears) is not int:
			return http_400(1, 'Invalid Data Type', 'total_gears')
		total_gears = total_gears  # type: int

		if type(total_kpa) is not int:
			return http_400(1, 'Invalid Data Type', 'total_kpa')
		total_kpa = total_kpa  # type: int

		if type(gear_dispense_method) is not str:
			return http_400(1, 'Invalid Data Type', 'gear_dispense_method')
		gear_dispense_method = gear_dispense_method  # type: str

		if type(got_gear_from_human) is not bool:
			return http_400(1, 'Invalid Data Type', 'got_gear_from_human')
		got_gear_from_human = got_gear_from_human  # type: bool

		if type(got_gear_from_floor) is not bool:
			return http_400(1, 'Invalid Data Type', 'got_gear_from_floor')
		got_gear_from_floor = got_gear_from_floor  # type: bool

		if type(high_goal_rating) is not str:
			return http_400(1, 'Invalid Data Type', 'high_goal_rating')
		high_goal_rating = high_goal_rating  # type: str

		if type(high_goal_shoot_from_key) is not bool:
			return http_400(1, 'Invalid Data Type', 'high_goal_shoot_from_key')
		high_goal_shoot_from_key = high_goal_shoot_from_key  # type: bool

		if type(high_goal_shoot_from_wall) is not bool:
			return http_400(1, 'Invalid Data Type', 'high_goal_shoot_from_wall')
		high_goal_shoot_from_wall = high_goal_shoot_from_wall  # type: bool

		if type(high_goal_shoot_from_afar) is not bool:
			return http_400(1, 'Invalid Data Type', 'high_goal_shoot_from_afar')
		high_goal_shoot_from_afar = high_goal_shoot_from_afar  # type: bool

		if type(low_goal_rating) is not str:
			return http_400(1, 'Invalid Data Type', 'low_goal_rating')
		low_goal_rating = low_goal_rating  # type: str

		if type(total_hoppers) is not int:
			return http_400(1, 'Invalid Data Type', 'total_hoppers')
		total_hoppers = total_hoppers  # type: int

		if type(collected_from_hopper) is not bool:
			return http_400(1, 'Invalid Data Type', 'collected_from_hopper')
		collected_from_hopper = collected_from_hopper  # type: bool

		if type(collected_fuel_from_floor) is not bool:
			return http_400(1, 'Invalid Data Type', 'collected_fuel_from_floor')
		collected_fuel_from_floor = collected_fuel_from_floor  # type: bool

		if type(last_modified) is not str:
			return http_400(1, 'Invalid Data Type', 'last_modified')
		last_modified = last_modified  # type: str

		if type(notes) is not str:
			return http_400(1, 'Invalid Data Type', 'notes')
		notes = notes  # type: str

		if type(scout_name) is not str:
			return http_400(1, 'Invalid Data Type', 'scout_name')
		scout_name = scout_name  # type: str

		try:
			db_functions.add_matchv5(match_id=match_id,
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

	response['success'] = True
	return home_cor(jsonify(**response))


@app.route('/download')
def api_download():
	response = {
		'matches': db_functions.matches_array()
	}
	return home_cor(jsonify(**response))


@app.route('/events')
def api_events():
	response = {
		'events': db_functions.events_recorded()
	}
	return home_cor(jsonify(**response))


@app.route('/download_data/<event_name>.csv')
def api_download_data(event_name):
	data = db_functions.matrix_data_for_event(event_name)
	return excel.make_response_from_array(data, 'csv')

app.run(debug=True, host='0.0.0.0', port=80)
