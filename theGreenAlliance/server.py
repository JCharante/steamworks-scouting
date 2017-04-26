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


app.run('0.0.0.0', 8080)
