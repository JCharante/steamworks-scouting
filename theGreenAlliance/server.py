import json
from twisted.web.static import File
from klein import Klein
import db_functions

app = Klein()


@app.route('/')
def pg_index(request):
	return 'The Green Alliance'


@app.route('/static', branch=True)
def pg_static(request):
	return File('./static/')


@app.route('/list_of_numbers')
def pg_list_of_random_numbers(request):
	request.responseHeaders.addRawHeader(b'content-type', b'application/json')
	json_data = {
		'data': {
			'numbers': [i for i in range(100)]
		}
	}
	return json.dumps(json_data)

app.run('0.0.0.0', 8080)
