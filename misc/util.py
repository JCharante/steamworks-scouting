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


def tie_breaker_steam_works(red_foul_points: int, blue_foul_points: int,
							red_auto_points: int, blue_auto_points: int,
							red_total_rotor_points: int, blue_total_rotor_points: int,
							red_touchpad_points: int, blue_touchpad_points: int,
							red_total_pressure: int, blue_total_pressure: int) -> str:
	"""
	Taken from the Game Manual
	Table 10-2: Quarterfinal, Semifinal, and Overtime Tiebreaker Criteria
	Order Sort Criteria
	1st Fewer FOUL points
	2nd Cumulative sum of AUTO points
	3rd Cumulative ROTOR engagement score (AUTO and TELEOP)
	4th Cumulative TOUCHPAD score
	5th Total accumulated pressure
	6th MATCH is replayed
	"""

	if red_foul_points > blue_foul_points:
		return 'red'
	elif blue_foul_points > red_foul_points:
		return 'blue'

	if red_auto_points > blue_auto_points:
		return 'red'
	elif blue_auto_points > red_auto_points:
		return 'blue'

	if red_total_rotor_points > blue_total_rotor_points:
		return 'red'
	elif blue_total_rotor_points > red_total_rotor_points:
		return 'blue'

	if red_touchpad_points > blue_touchpad_points:
		return 'red'
	elif blue_touchpad_points > red_touchpad_points:
		return 'blue'

	if red_total_pressure > blue_total_pressure:
		return 'red'
	elif blue_total_pressure > red_total_pressure:
		return 'blue'

	return 'replay'
