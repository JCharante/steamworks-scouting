

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
		return 'red victory'
	elif blue_foul_points > red_foul_points:
		return 'blue victory'

	if red_auto_points > blue_auto_points:
		return 'red victory'
	elif blue_auto_points > red_auto_points:
		return 'blue victory'

	if red_total_rotor_points > blue_total_rotor_points:
		return 'red victory'
	elif blue_total_rotor_points > red_total_rotor_points:
		return 'blue victory'

	if red_touchpad_points > blue_touchpad_points:
		return 'red victory'
	elif blue_touchpad_points > red_touchpad_points:
		return 'blue victory'

	if red_total_pressure > blue_total_pressure:
		return 'red victory'
	elif blue_total_pressure > red_total_pressure:
		return 'blue victory'

	return 'replay'
