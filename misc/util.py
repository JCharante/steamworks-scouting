import os
import json
from typing import List
from subprocess import run
import csv
from datetime import datetime


def path_to_this_files_directory():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	return dir_path + '/'


def loads(x: str):
	try:
		return json.loads(x)
	except:
		return {}


def dumps(x: dict):
	try:
		return json.dumps(x)
	except:
		return "{}"


def get_team_number(teamid):
	return teamid.replace('frc', '')


def save_as_csv(data: List[List], name='unnamed', append_timestamp=False):
	run(['mkdir', '-p', 'exports'])
	filename = f'exports/{name}{f"-{datetime.utcnow()}" if append_timestamp else ""}.csv'
	run(['touch', filename])
	with open(filename, "w") as f:
		writer = csv.writer(f)
		writer.writerows(data)
