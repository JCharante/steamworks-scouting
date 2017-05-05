from klein import Klein
import pyexcel
from io import StringIO
from pyexcel_io import save_data
from twisted.web.static import File
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


app = Klein()
templates_folder = dir_path = os.path.dirname(os.path.realpath(__file__)) + '/templates'


def get_arg(request, key, default_value):
	list = request.args.get(str.encode(key), default_value)
	if list == default_value:
		return default_value
	else:
		return list[0].decode('utf-8')


def return_json(request, response):
	request.responseHeaders.addRawHeader(b'content-type', b'application/json')
	request.responseHeaders.addRawHeader(b'Access-Control-Allow-Origin', b'*')
	request.responseHeaders.addRawHeader(b'Access-Control-Allow-Headers', b'Content-Type, Access-Control-Allow-Origin')
	return json.dumps(response)


def home_cor(obj):
	return_response = make_response(obj)
	return_response.headers['Access-Control-Allow-Origin'] = "*"
	return_response.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS,PUT,DELETE'
	return_response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Origin, Accept"
	return return_response


def http_400(request, response):
	request.setResponseCode(400)
	return return_json(request, response)


@app.route('/')
def api_root(request):
	return open(f'{templates_folder}/index.html').read()


@app.route('/match/upload', methods=['OPTIONS', 'POST'])
def api_match_upload(request):
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
	if request.method == b'POST':
		data = json.loads(request.content.read().decode('utf-8'))
		if data is not None:
			data = data  # type: Dict
			for parameter_name in required_parameters:
				parameter_value = data.get(parameter_name, None)
				if parameter_value is None:
					return http_400(request, {
						"error": {
							"error_code": 3,
							"message": 'Required Parameter is Missing',
							"fields": parameter_name
						}
					})
				if type(parameter_value) in required_parameters[parameter_name]['valid_types'] is False:
					return http_400(request, {
						"error": {
							"error_code": 10,
							"message": 'Invalid Type for Required Parameter!',
							"fields": parameter_name
						}
					})
				else:
					required_parameters[parameter_name]['value'] = parameter_value
		else:
			return http_400(request, {
				"error": {
					"error_code": 2,
					"message": 'Required JSON Object Not Sent',
					"fields": 'body'
				}
			})

	response = dict()

	if request.method == b'OPTIONS':
		return return_json(request, response)
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
		return return_json(request, response)
	except exceptions.GenericException as e:
		response = {
			"error": {
				"code": e.error_code,
				"message": e.error_message,
				"fields": e.fields
			}
		}
		return http_400(request, response)


@app.route('/download/app', methods=['OPTIONS', 'GET'])
def api_download(request):
	if request.method == b'OPTIONS':
		return return_json(request, {})
	if request.method == b'GET':
		server_password = get_arg(request, 'serverPassword', None)
		if server_password != os.environ['serverPassword']:
			return http_400(request, {
				"error": {
					"code": 3,
					"message": "Not Authorized!",
					"fields": "serverPassword"
				}
			})
		response = {
			'matches': db_functions.matches_array()
		}
		return return_json(request, response)


@app.route('/events/<event_code>/matches/all', methods=['OPTIONS', 'GET'])
def events_event_code_matches_all(request, event_code):
	if request.method == b'GET':
		server_password = get_arg(request, 'serverPassword', None)
		if server_password != os.environ['serverPassword']:
			return http_400(request, {
				"error": {
					"code": 3,
					"message": "Not Authorized!",
					"fields": "serverPassword"
				}
			})
		response = {
			'matches': db_functions.matches_array({event_code})
		}
		return return_json(request, response)
	elif request.method == b'OPTIONS':
		return return_json(request, {})


@app.route('/events', methods=['OPTIONS', 'GET'])
def api_events(request):
	response = {
		'events': db_functions.events_recorded()
	}
	return return_json(request, response)


@app.route('/download/csv', methods=['OPTIONS', 'GET'])
def api_download_data(request):
	if request.method == b'OPTIONS':
		return return_json(request, {})
	if request.method == b'GET':
		dataset = get_arg(request, 'dataset', None)
		server_password = get_arg(request, 'serverPassword', None)
		if server_password != os.environ['serverPassword']:
			return http_400(request, {
				"error": {
					"code": 3,
					"message": "Not Authorized!",
					"fields": "serverPassword"
				}
			})
		if dataset is None:
			return http_400(request, {
				"error": {
					"code": 4,
					"message": "Dataset not specified",
					"fields": "dataset"
				}
			})
		data = db_functions.matrix_data_for_event(dataset)
		io = StringIO()
		save_data(io, data)
		request.responseHeaders.addRawHeader(b'Content-Disposition', str.encode(f'attachment; filename="{dataset}-{datetime.datetime.utcnow()}.csv"'))
		return io.getvalue()

if __name__ == '__main__':
	app.run('0.0.0.0', 80)
