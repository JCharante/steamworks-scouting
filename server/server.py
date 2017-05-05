from flask import Flask, request, make_response, Response, jsonify, render_template
import flask_excel as excel
import json
import os
from typing import List, Dict
import db_functions
import exceptions
import migration
import sys
import datetime

if 'serverPassword' in os.environ is False:
	print('Environmental Variable serverPassword not set.')
	print('Exiting with Status Code -1')
	sys.exit(-1)

migration.migrate_from_matchv1_to_matchv2()
migration.migrate_matchv2_to_matchv3()
migration.migrate_matchv3_to_matchv4()
migration.migrate_matchv4_to_matchv5()
migration.migrate_matchv5_to_matchv6()
migration.migrate_matchv6_to_matchv7()
app = Flask(__name__)


def home_cor(obj):
	return_response = make_response(obj)
	return_response.headers['Access-Control-Allow-Origin'] = "*"
	return_response.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS,PUT,DELETE'
	return_response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Origin, Accept"
	return return_response


def http_400(response: Dict):
	response_object = home_cor(jsonify(**response))
	response_object.status_code = 400
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
		},
		'serverPassword': {
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
					return http_400({
						"error": {
							"error_code": 3,
							"message": 'Required Parameter is Missing',
							"fields": parameter_name
						}
					})
				if type(parameter_value) in required_parameters[parameter_name]['valid_types'] is False:
					return http_400({
						"error": {
							"error_code": 10,
							"message": 'Invalid Type for Required Parameter!',
							"fields": parameter_name
						}
					})
				else:
					required_parameters[parameter_name]['value'] = parameter_value
		else:
			return http_400({
				"error": {
					"error_code": 2,
					"message": 'Required JSON Object Not Sent',
					"fields": 'body'
				}
			})

	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	# Generic End #

	matches = required_parameters['matches']['value']  # type: List[Dict]
	server_password = required_parameters['serverPassword']['value']  # type: str

	try:
		db_functions.upload_matches(matches, server_password)
		response = {
			"data": {
				"success": True
			}
		}
		response_object = home_cor(jsonify(**response))
		response_object.status_code = 200
		return response_object
	except exceptions.GenericException as e:
		response = {
			"error": {
				"code": e.error_code,
				"message": e.error_message,
				"fields": e.fields
			}
		}
		response_object = home_cor(jsonify(**response))
		response_object.status_code = 400
		return response_object


@app.route('/download/app', methods=['OPTIONS', 'GET'])
def api_download():
	if request.method == 'OPTIONS':
		return home_cor(jsonify(**{}))
	if request.method == 'GET':
		server_password = request.args.get('serverPassword', None)
		if server_password != os.environ['serverPassword']:
			return http_400({
				"error": {
					"code": 3,
					"message": "Not Authorized!",
					"fields": "serverPassword"
				}
			})
		response = {
			'matches': db_functions.matches_array()
		}
		return home_cor(jsonify(**response))


@app.route('/events/<event_code>/matches/all', methods=['OPTIONS', 'GET'])
def events_event_code_matches_all(event_code):
	if request.method == 'OPTIONS':
		return home_cor(jsonify(**{}))
	if request.method == 'GET':
		server_password = request.args.get('serverPassword', None)
		if server_password != os.environ['serverPassword']:
			return http_400({
				"error": {
					"code": 3,
					"message": "Not Authorized!",
					"fields": "serverPassword"
				}
			})
		response = {
			'matches': db_functions.matches_array({event_code})
		}
		return home_cor(jsonify(**response))


@app.route('/events', methods=['OPTIONS', 'GET'])
def api_events():
	response = {
		'events': db_functions.events_recorded()
	}
	return home_cor(jsonify(**response))


@app.route('/download/csv', methods=['OPTIONS', 'GET'])
def api_download_data():
	if request.method == 'OPTIONS':
		return home_cor(jsonify(**{}))
	if request.method == 'GET':
		dataset = request.args.get('dataset', None)
		server_password = request.args.get('serverPassword', None)
		if server_password != os.environ['serverPassword']:
			return http_400({
				"error": {
					"code": 3,
					"message": "Not Authorized!",
					"fields": "serverPassword"
				}
			})
		data = db_functions.matrix_data_for_event(dataset)
		return excel.make_response_from_array(data, 'csv', file_name=f'{dataset}-{datetime.datetime.utcnow()}.csv')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8000, threaded=True)
