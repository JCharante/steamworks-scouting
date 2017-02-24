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
	1 - Invalid Credentials
	2 - json body in post request missing
	3 - Missing Required Field
	4 - Username not Unique
	5 - Insecure Password (Probably blank)
	6 - Invalid AID
	7 - Invalid Group ID
	8 - Can't leave existing group
	9 - Can't join a group that you're a member of
	"""
	response_object = home_cor(Response(json.dumps({
		'code': code,
		'message': message,
		'fields': fields
	}), 400))
	response_object.headers['Content-Type'] = 'application/json'
	return response_object


@app.route('/groups/create', methods=['OPTIONS', 'POST', 'GET'])
def groups_create():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	aid = None
	group_name = None

	if request.method == 'GET':
		aid = request.args.get('aid', None)
		group_name = request.args.get('group_name', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			data = data  # type: Dict
			aid = data.get('aid', None)
			group_name = data.get('group_name', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if aid is None:
		return http_400(3, 'Required Parameter is Missing', 'aid')
	if group_name is None:
		return http_400(3, 'Required Parameter is Missing', 'group_name')

	try:
		aid = aid  # str
		group_name = group_name  # str
		group_id = db_functions.create_group(aid, group_name)
	except exceptions.InvalidAid:
		return http_400(6, 'Invalid AID', 'aid')

	response['group_id'] = group_id
	return home_cor(jsonify(**response))


@app.route('/groups/join', methods=['OPTIONS', 'GET', 'POST'])
def groups_join():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	aid = None
	invite_code = None

	if request.method == 'GET':
		aid = request.args.get('aid', None)
		invite_code = request.args.get('invite_code', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			aid = data.get('aid', None)
			invite_code = data.get('invite_code', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if aid is None:
		return http_400(3, 'Required Parameter is Missing', 'aid')
	if invite_code is None:
		return http_400(3, 'Required Parameter is Missing', 'invite_code')

	try:
		db_functions.join_group_invite_code(aid, invite_code)
	except exceptions.InvalidAid:
		return http_400(6, 'Invalid AID', 'aid')
	except exceptions.InvalidGroupInviteCode:
		return http_400(7, 'Invalid Group Invite Code', 'invite_code')
	except exceptions.AlreadyAGroupMember:
		return http_400(9, 'Already In Group', 'aid')

	response['success'] = True
	return home_cor(jsonify(**response))


@app.route('/groups/leave', methods=['OPTIONS', 'GET', 'POST'])
def groups_leave():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	aid = None
	group_id = None

	if request.method == 'GET':
		aid = request.args.get('aid', None)
		group_id = request.args.get('group_id', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			aid = data.get('aid', None)
			group_id = data.get('group_id', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if aid is None:
		return http_400(3, 'Required Parameter is Missing', 'aid')
	if group_id is None:
		return http_400(3, 'Required Parameter is Missing', 'group_id')

	try:
		db_functions.leave_group(aid, group_id)
	except exceptions.InvalidAid:
		return http_400(6, 'Invalid AID', 'aid')
	except exceptions.InvalidGroupId:
		return http_400(7, 'Invalid Group ID', 'group_id')
	except exceptions.AlreadyNotAGroupMember:
		return http_400(8, 'Can\'t leave a group you\'re not in', 'group_id')

	response['success'] = True
	return home_cor(jsonify(**response))


@app.route('/groups/invite_code', methods=['OPTIONS', 'GET', 'POST'])
def groups_invite_code():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	group_id = None

	if request.method == 'GET':
		group_id = request.args.get('group_id', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			group_id = data.get('group_id', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if group_id is None:
		return http_400(3, 'Required Parameter is Missing', 'group_id')

	try:
		invite_code = db_functions.get_invite_code(group_id)
	except exceptions.InvalidGroupId:
		return http_400(7, 'Invalid Group ID', 'group_id')

	response['invite_code'] = invite_code
	return home_cor(jsonify(**response))


@app.route('/users/join', methods=['POST', 'OPTIONS', 'GET'])
def users_join():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	username = None
	password = None

	if request.method == 'GET':
		username = request.args.get('username', None)
		password = request.args.get('password', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			username = data.get('username', None)
			password = data.get('password', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if username is None:
		return http_400(3, 'Required Parameter is Missing', 'username')
	if password is None:
		return http_400(3, 'Required Parameter is Missing', 'password')

	try:
		aid = db_functions.create_user(username, password)
	except exceptions.UsernameNotUniqueException:
		return http_400(4, 'Username Taken', 'username')
	except exceptions.InsecurePasswordException:
		return http_400(5, 'Password Is Too Weak', 'password')

	response['aid'] = aid
	return home_cor(jsonify(**response))


@app.route('/users/login', methods=['POST', 'OPTIONS', 'GET'])
def users_login():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	username = None
	password = None

	if request.method == 'GET':
		username = request.args.get('username', None)
		password = request.args.get('password', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			username = data.get('username', None)
			password = data.get('password', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if username is None:
		return http_400(3, 'Required Parameter is Missing', 'username')
	if password is None:
		return http_400(3, 'Required Parameter is Missing', 'password')

	try:
		aid = db_functions.login(username, password)
	except exceptions.InvalidCredentials:
		return http_400(1, 'Invalid Credentials', 'Username/Password')

	response['aid'] = aid
	return home_cor(jsonify(**response))


@app.route('/users/wipe')
def users_wipe():
	if settings.dev_mode:
		db_functions.wipe_users()
		return home_cor(jsonify(**{
			'success': True
		}))
	else:
		return home_cor(jsonify(**{
			'success': False,
			'error': 'not running in dev mode'
		}))


@app.route('/users/metrics')
def users_quantity():
	return home_cor(jsonify(**{
		'RegisteredUsers': db_functions.number_of_users()
	}))


@app.route('/users/username', methods=['OPTIONS', 'GET', 'POST'])
def users_username():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	aid = None

	if request.method == 'GET':
		aid = request.args.get('aid', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			aid = data.get('aid', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if aid is None:
		return http_400(3, 'Required Parameter is Missing', 'aid')

	aid = aid  # type: str
	try:
		username = db_functions.get_username(aid)
	except exceptions.InvalidAid:
		return http_400(6, 'Invalid AID', 'aid')

	response['username'] = username
	return home_cor(jsonify(**response))


@app.route('/users/leave', methods=['OPTIONS', 'GET', 'POST'])
def users_leave():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	aid = None

	if request.method == 'GET':
		aid = request.args.get('aid', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			aid = data.get('aid', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if aid is None:
		return http_400(3, 'Required Parameter is Missing', 'aid')

	aid = aid  # type: str
	try:
		db_functions.delete_user(aid)
	except exceptions.InvalidAid:
		return http_400(6, 'Invalid AID', 'aid')

	response['success'] = True
	return home_cor(jsonify(**response))


@app.route('/users/last_login', methods=['OPTIONS', 'GET', 'POST'])
def users_last_login():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	aid = None

	if request.method == 'GET':
		aid = request.args.get('aid', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			aid = data.get('aid', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if aid is None:
		return http_400(3, 'Required Parameter is Missing', 'aid')

	aid = aid  # type: str
	try:
		last_login = db_functions.get_last_login(aid)
	except exceptions.InvalidAid:
		return http_400(6, 'Invalid AID', 'aid')

	response['last_login'] = last_login
	return home_cor(jsonify(**response))


@app.route('/users/groups', methods=['OPTIONS', 'POST', 'GET'])
def users_groups():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	aid = None

	if request.method == 'GET':
		aid = request.args.get('aid', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			aid = data.get('aid', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if aid is None:
		return http_400(3, 'Required Parameter is Missing', 'aid')

	try:
		groups = db_functions.groups_user_is_in(aid)
	except exceptions.InvalidAid:
		return http_400(6, 'Invalid AID', 'aid')

	response['groups'] = groups
	return home_cor(jsonify(**response))


@app.route('/groups/details', methods=['OPTIONS', 'POST', 'GET'])
def groups_details():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	aid = None
	group_id = None

	if request.method == 'GET':
		aid = request.args.get('aid', None)
		group_id = request.args.get('group_id', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			aid = data.get('aid', None)
			group_id = data.get('group_id', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if aid is None:
		return http_400(3, 'Required Parameter is Missing', 'aid')
	if group_id is None:
		return http_400(3, 'Required Parameter is Missing', 'group_id')

	try:
		details = db_functions.get_group_details(aid, group_id)
	except exceptions.InvalidAid:
		return http_400(6, 'Invalid AID', 'aid')
	except exceptions.InvalidGroupId:
		return http_400(7, 'Invalid Group ID', 'group_id')
	except exceptions.NotAGroupMember:
		return http_400(8, 'You need to be in this group to perform this action', 'group_id')

	response['group'] = details
	return home_cor(jsonify(**response))

print(f'Using Database: {settings.database_address}')

app.run(debug=True, host='0.0.0.0', port=8881)
