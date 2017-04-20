import util
from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Tuple, List, Dict
from settings import Settings
import requests
import re

Base = declarative_base()


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


class TrueSkillMatchV1(Base):
	__tablename__ = 'TrueSkillMatchV1'
	pk = Column(Integer, primary_key=True)
	winning_alliance = Column(String(4))
	blue_1 = Column(Integer)
	blue_2 = Column(Integer)
	blue_3 = Column(Integer)
	red_1 = Column(Integer)
	red_2 = Column(Integer)
	red_3 = Column(Integer)
	event_key = Column(String(10))
	match_key = Column(String(20))


settings = Settings()
engine = create_engine(settings.database_address)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


class MatchDataFetcher:

	def __init__(self, event_code: str):
		self.settings = Settings()
		self.event_code = event_code
		self.url = f'https://www.thebluealliance.com/api/v2/event/{event_code}'
		self.headers = {
			'X-TBA-App-Id': self.settings.app_id
		}

		self.fetch_and_save_data()

	def fetch_and_save_data(self):
		session = DBSession()
		print(f'Fetching Ranking Data for {self.event_code}..')
		matches = requests.get(self.url + '/matches', headers=self.headers).json()
		recorded_matches = session.query(TrueSkillMatchV1).filter(TrueSkillMatchV1.event_key == self.event_code).count()
		if recorded_matches == len(matches):
			print(f'All matches for {self.event_code} already recorded')
			return
		elif recorded_matches > 0:
			session.query(TrueSkillMatchV1).query(TrueSkillMatchV1.event_key == self.event_code).delete()
			session.commit()
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
				print('Error Processing Match. Raw data:', match)
				return
			winner = ''

			# Determining Winner for Qualification Match
			if comp_level == 'qm':
				if blue_score > red_score:
					winner = 'draw'
				elif red_score > blue_score:
					winner = 'red'
				elif red_score == blue_score:
					winner = 'blue'
			# Determining Winner for Quarter Final or Semi Final Match or Final Match
			elif comp_level == 'qf' or comp_level == 'sf' or comp_level == 'f':
				if blue_score > red_score:
					winner = 'blue'
				elif red_score > blue_score:
					winner = 'red'
				elif blue_score == red_score:
					blue_score_breakdown = match['score_breakdown']['blue']
					red_score_breakdown = match['score_breakdown']['red']

					red_foul_points = red_score_breakdown['foulPoints']
					blue_foul_points = blue_score_breakdown['foulPoints']
					red_auto_points = red_score_breakdown['autoPoints']
					blue_auto_points = blue_score_breakdown['autoPoints']
					red_total_rotor_points = red_score_breakdown['autoRotorPoints'] + red_score_breakdown['teleopRotorPoints']
					blue_total_rotor_points = blue_score_breakdown['autoRotorPoints'] + blue_score_breakdown['teleopRotorPoints']
					red_touchpad_points = sum([50 if red_score_breakdown['touchpadNear'] == 'ReadyForTakeoff' else 0, 50 if red_score_breakdown['touchpadMiddle'] == 'ReadyForTakeoff' else 0, 50 if red_score_breakdown['touchpadFar'] == 'ReadyForTakeoff' else 0])
					blue_touchpad_points = sum([50 if blue_score_breakdown['touchpadNear'] == 'ReadyForTakeoff' else 0, 50 if blue_score_breakdown['touchpadMiddle'] == 'ReadyForTakeoff' else 0, 50 if blue_score_breakdown['touchpadFar'] == 'ReadyForTakeoff' else 0])
					red_total_pressure = red_score_breakdown['autoFuelPoints'] + red_score_breakdown['teleopFuelPoints']
					blue_total_pressure = blue_score_breakdown['autoFuelPoints'] + blue_score_breakdown['teleopFuelPoints']

					tie_breaker_winner = tie_breaker_steam_works(red_foul_points, blue_foul_points,
											red_auto_points, blue_auto_points,
											red_total_rotor_points, blue_total_rotor_points,
											red_touchpad_points, blue_touchpad_points,
											red_total_pressure, blue_total_pressure)

					if tie_breaker_winner == 'red' or tie_breaker_winner == 'blue':
						winner = tie_breaker_winner
					else:
						print('Error Processing Match. Raw data:', match)
						return

			session.add(TrueSkillMatchV1(
				winning_alliance=winner,
				blue_1=re.sub("\D", "", blue_1),
				blue_2=re.sub("\D", "", blue_2),
				blue_3=re.sub("\D", "", blue_3),
				red_1=re.sub("\D", "", red_1),
				red_2=re.sub("\D", "", red_2),
				red_3=re.sub("\D", "", red_3),
				event_key=self.event_code,
				match_key=match_key
			))
		print(f'Saving Data for {self.event_code}')
		session.commit()
		print(f'Saved Data for {self.event_code}')
		session.close()

a = MatchDataFetcher('2017necmp')
