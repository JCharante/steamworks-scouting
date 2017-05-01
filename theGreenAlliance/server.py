import json
from twisted.web.static import File
from klein import Klein
import db_functions
from db_setup import MatchV1
from db_functions import DBSession

app = Klein()


@app.route('/')
def pg_index(request):
	return 'The Green Alliance'


@app.route('/static', branch=True)
def pg_static(request):
	return File('./static/')


@app.route('/event/<event_code>/matches/all')
def pg_matches_all(request, event_code):
	request.responseHeaders.addRawHeader(b'content-type', b'application/json')
	session = DBSession()
	json_response = {
		'data': {
			'matches': []
		}
	}
	for match in session.query(MatchV1).filter(MatchV1.event_code == event_code).all():  # type: MatchV1
		json_response['data']['matches'].append({
			'has_played': match.has_played,
			'taking_bets': match.taking_bets,
			'event_code': match.event_code,
			'match_key': match.match_key,
			'blue_1': match.blue_1,
			'blue_2': match.blue_2,
			'blue_3': match.blue_3,
			'red_1': match.red_1,
			'red_2': match.red_2,
			'red_3': match.red_3
		})
	return json.dumps(json_response)


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
