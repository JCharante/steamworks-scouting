from flask import Flask, request, make_response, Response, jsonify
import json

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
	return home_cor(jsonify(**{
		'message': 'This server doesn\'t have a cow.'
	}))

app.run(debug=True, host='0.0.0.0', port=9876)
