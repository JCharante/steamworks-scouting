import re
from typing import List
from db_setup import MatchV1
from db_functions import DBSession
from util import tie_breaker_steam_works
from dataFetcher import EventCodeFetcher, DataFetcher


def download_event_matches(event_codes: List[str]):
	def save_event_matches(response, content):
		session = DBSession()
		event_code = response.url.split('/')[4]  # www.thebluealliance.com/api/v2/event/{event_code}/matches
		print(f'Fetched Ranking Data for {event_code}..')
		matches = content
		for match in matches:
			"""
			match = {
						"comp_level": "f",
						"match_number": 3,
						"key": "2017necmp_f1m1",
						"score_breakdown": {
							"blue": {
								"teleopPoints": 370,
								"robot3Auto": "Mobility",
								"rotor1Auto": true,
								"autoPoints": 75,
								"rotor1Engaged": true,
								"foulCount": 0,
								"touchpadFar": "ReadyForTakeoff",
								"foulPoints": 25,
								"techFoulCount": 0,
								"totalPoints": 470,
								"tba_rpEarned": null,
								"autoRotorPoints": 60,
								"adjustPoints": 0,
								"robot1Auto": "Mobility",
								"rotor2Auto": false,
								"rotor4Engaged": true,
								"teleopRotorPoints": 120,
								"autoFuelHigh": 0,
								"teleopFuelHigh": 0,
								"teleopTakeoffPoints": 150,
								"robot2Auto": "Mobility",
								"kPaRankingPointAchieved": false,
								"autoFuelLow": 0,
								"teleopFuelLow": 0,
								"rotorBonusPoints": 100,
								"autoMobilityPoints": 15,
								"rotor3Engaged": true,
								"autoFuelPoints": 0,
								"teleopFuelPoints": 0,
								"touchpadMiddle": "ReadyForTakeoff",
								"touchpadNear": "ReadyForTakeoff",
								"rotorRankingPointAchieved": false,
								"kPaBonusPoints": 0,
								"rotor2Engaged": true
							},
							"red": {
								"teleopPoints": 398,
								"robot3Auto": "Mobility",
								"rotor1Auto": true,
								"autoPoints": 117,
								"rotor1Engaged": true,
								"foulCount": 0,
								"touchpadFar": "ReadyForTakeoff",
								"foulPoints": 0,
								"techFoulCount": 1,
								"totalPoints": 515,
								"tba_rpEarned": null,
								"autoRotorPoints": 60,
								"adjustPoints": 0,
								"robot1Auto": "Mobility",
								"rotor2Auto": false,
								"rotor4Engaged": true,
								"teleopRotorPoints": 120,
								"autoFuelHigh": 42,
								"teleopFuelHigh": 26,
								"teleopTakeoffPoints": 150,
								"robot2Auto": "Mobility",
								"kPaRankingPointAchieved": false,
								"autoFuelLow": 0,
								"teleopFuelLow": 0,
								"rotorBonusPoints": 100,
								"autoMobilityPoints": 15,
								"rotor3Engaged": true,
								"autoFuelPoints": 42,
								"teleopFuelPoints": 8,
								"touchpadMiddle": "ReadyForTakeoff",
								"touchpadNear": "ReadyForTakeoff",
								"rotorRankingPointAchieved": false,
								"kPaBonusPoints": 20,
								"rotor2Engaged": true
							}
						},
						"alliances": {
							"blue": {
								"surrogates": [],
								"score": 364,
								"teams": [
									"frc1519",
									"frc3719",
									"frc5813"
								]
							},
							"red": {
								"surrogates": [],
								"score": 511,
								"teams": [
									"frc1073",
									"frc2168",
									"frc195"
								]
							}
						}
					}
			"""

			has_played = match.get('score_breakdown', None) is not None

			# Basic Information
			match_key = match.get('key', None)
			comp_level = match.get('comp_level', None)
			blue_1 = match.get('alliances', {}).get('blue', {}).get('teams', [None, None, None])[0]
			blue_2 = match.get('alliances', {}).get('blue', {}).get('teams', [None, None, None])[1]
			blue_3 = match.get('alliances', {}).get('blue', {}).get('teams', [None, None, None])[2]
			red_1 = match.get('alliances', {}).get('red', {}).get('teams', [None, None, None])[0]
			red_2 = match.get('alliances', {}).get('red', {}).get('teams', [None, None, None])[1]
			red_3 = match.get('alliances', {}).get('red', {}).get('teams', [None, None, None])[2]
			red_score = match.get('alliances', {}).get('red', {}).get('score', None)
			blue_score = match.get('alliances', {}).get('blue', {}).get('score', None)

			if match_key is None or comp_level is None or blue_1 is None or blue_2 is None or blue_3 is None or red_1 is None or red_2 is None or red_3 is None or red_score is None or blue_score is None:
				continue

			result = 'unknown'

			if has_played:

				# Determining Winner for Qualification Match
				if comp_level == 'qm':
					if blue_score > red_score:
						result = 'draw'
					elif red_score > blue_score:
						result = 'red victory'
					elif red_score == blue_score:
						result = 'blue victory'
				# Determining Winner for Quarter Final or Semi Final Match or Final Match
				elif comp_level == 'qf' or comp_level == 'sf' or comp_level == 'f':
					if blue_score > red_score:
						result = 'blue'
					elif red_score > blue_score:
						result = 'red'
					elif blue_score == red_score:
						blue_score_breakdown = match['score_breakdown']['blue']
						red_score_breakdown = match['score_breakdown']['red']

						red_foul_points = red_score_breakdown['foulPoints']
						blue_foul_points = blue_score_breakdown['foulPoints']
						red_auto_points = red_score_breakdown['autoPoints']
						blue_auto_points = blue_score_breakdown['autoPoints']
						red_total_rotor_points = red_score_breakdown['autoRotorPoints'] + red_score_breakdown['teleopRotorPoints']
						blue_total_rotor_points = blue_score_breakdown['autoRotorPoints'] + blue_score_breakdown['teleopRotorPoints']
						red_touchpad_points = sum([
							50 if red_score_breakdown['touchpadNear'] == 'ReadyForTakeoff' else 0,
							50 if red_score_breakdown['touchpadMiddle'] == 'ReadyForTakeoff' else 0,
							50 if red_score_breakdown['touchpadFar'] == 'ReadyForTakeoff' else 0
						])
						blue_touchpad_points = sum([
							50 if blue_score_breakdown['touchpadNear'] == 'ReadyForTakeoff' else 0,
							50 if blue_score_breakdown['touchpadMiddle'] == 'ReadyForTakeoff' else 0,
							50 if blue_score_breakdown['touchpadFar'] == 'ReadyForTakeoff' else 0
						])
						red_total_pressure = red_score_breakdown['autoFuelPoints'] + red_score_breakdown['teleopFuelPoints']
						blue_total_pressure = blue_score_breakdown['autoFuelPoints'] + blue_score_breakdown['teleopFuelPoints']

						tie_breaker_winner = tie_breaker_steam_works(red_foul_points, blue_foul_points,
																	 red_auto_points, blue_auto_points,
																	 red_total_rotor_points, blue_total_rotor_points,
																	 red_touchpad_points, blue_touchpad_points,
																	 red_total_pressure, blue_total_pressure)

						if tie_breaker_winner == 'red victory' or tie_breaker_winner == 'blue victory':
							result = tie_breaker_winner
						else:
							continue

			session.add(MatchV1(
				winning_alliance=result,
				blue_1=int(re.sub("\D", "", blue_1)),
				blue_2=int(re.sub("\D", "", blue_2)),
				blue_3=int(re.sub("\D", "", blue_3)),
				red_1=int(re.sub("\D", "", red_1)),
				red_2=int(re.sub("\D", "", red_2)),
				red_3=int(re.sub("\D", "", red_3)),
				event_code=event_code,
				match_key=match_key
			))
		print(f'Saving Data for {event_code}')
		session.commit()
		print(f'Saved Data for {event_code}')
		session.close()
