import util
from util import tie_breaker_steam_works
from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Tuple, List, Dict
from settings import Settings
from db_setup import Base, TrueSkillMatchV1, TrueSkillTeamV1
from asynchronous_demo import DataFetcher, EventCodeFetcher
import requests
import re
from trueskill import Rating, quality, rate


settings = Settings()
engine = create_engine(settings.database_address)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


ratings = {}


def retrieve_rating(team_number):
	global ratings
	if team_number in ratings:
		return ratings[team_number]
	else:
		return Rating()


def retrieve_rating_from_db(team_number):
	session = DBSession()
	row = session.query(TrueSkillTeamV1).filter(TrueSkillTeamV1.team_number == team_number).first()
	session.close()
	if row is None:
		return Rating()
	else:
		return Rating(mu=row.mu, sigma=row.sigma)


def save_rating(team_number, rating_obj):
	global ratings
	ratings[team_number] = rating_obj


def save_rating_to_db(team_number: int, mu: float, sigma: float):
	session = DBSession()
	row = session.query(TrueSkillTeamV1).filter(TrueSkillTeamV1.team_number == team_number).first()
	if row is None:
		session.add(TrueSkillTeamV1(
			team_number=team_number,
			mu=mu,
			sigma=sigma
		))
	else:
		row.mu = mu
		row.sigma = sigma
	session.commit()
	session.close()


def save_ratings_to_db(rankings: List[List]):
	session = DBSession()
	for ranking in rankings:
		row = session.query(TrueSkillTeamV1).filter(TrueSkillTeamV1.team_number == ranking[0]).first()
		if row is None:
			session.add(TrueSkillTeamV1(
				team_number=ranking[0],
				mu=ranking[1],
				sigma=ranking[2]
			))
		else:
			row.mu = ranking[1]
			row.sigma = ranking[2]
	session.commit()
	session.close()


def save_ratings(rankings: List[List]):
	global ratings
	for ranking in rankings:
		ratings[ranking[0]] = ranking[1]


def get_event_codes_for_district(district_code):
	url = f'https://www.thebluealliance.com/api/v2/district/{district_code}/2017/events'
	headers = {
		'X-TBA-App-Id': settings.app_id
	}
	events = requests.get(url, headers=headers).json()
	return [event['key'] for event in events]


def get_all_event_codes():
	url = 'https://www.thebluealliance.com/api/v2/events/2017'
	headers = {
		'X-TBA-App-Id': settings.app_id
	}
	events = requests.get(url, headers=headers).json()
	return [event['key'] for event in events]


def calculate_ratings():
	session = DBSession()
	print('Deleting Stored Ratings')
	session.query(TrueSkillTeamV1).delete()
	session.commit()

	print('Calculating Ratings...')
	for match in session.query(TrueSkillMatchV1).all():
		old_blue_1_rating = retrieve_rating(match.blue_1)
		old_blue_2_rating = retrieve_rating(match.blue_2)
		old_blue_3_rating = retrieve_rating(match.blue_3)
		old_red_1_rating = retrieve_rating(match.red_1)
		old_red_2_rating = retrieve_rating(match.red_2)
		old_red_3_rating = retrieve_rating(match.red_3)
		blue_alliance = [old_blue_1_rating, old_blue_2_rating, old_blue_3_rating]
		red_alliance = [old_red_1_rating, old_red_2_rating, old_red_3_rating]

		ranks = [0, 0]
		if match.winning_alliance == 'red':
			ranks = [1, 0]
		elif match.winning_alliance == 'blue':
			ranks = [0, 1]

		(new_blue_1_rating, new_blue_2_rating, new_blue_3_rating), (new_red_1_rating, new_red_2_rating, new_red_3_rating) = rate([blue_alliance, red_alliance], ranks=ranks)

		save_ratings([
			[match.blue_1, new_blue_1_rating],
			[match.blue_2, new_blue_2_rating],
			[match.blue_3, new_blue_3_rating],
			[match.red_1, new_red_1_rating],
			[match.red_2, new_red_2_rating],
			[match.red_3, new_red_3_rating]
		])

	session.close()
	print('Finished Calculating Ratings')


def save_ratings_to_csv(name='untitled-rankings', append_timestamp=False):
	session = DBSession()
	two_d_list = [['Team Number', 'Mu', 'Sigma']]
	for team in session.query(TrueSkillTeamV1).all():  # type: TrueSkillTeamV1
		two_d_list.append([team.team_number, team.mu, team.sigma])
	util.save_as_csv(two_d_list, name=name, append_timestamp=append_timestamp)

# NE District Rankings
# This takes into account datasets outside of NE events, which is why it is commented out.
# TODO: Calculate Ratings for teams in matches in a specified set of events
"""
for event_code in get_event_codes_for_district('ne'):
	MatchDataFetcher(event_code)

calculate_ratings()
save_ratings_to_db([[team_number, rating.mu, rating.sigma] for team_number, rating in ratings.items()])
save_ratings_to_csv(name='ne-district-rankings')
"""

# World Rankings


def save_match_data():
	def fetch_and_save_data(response, content):
		session = DBSession()
		event_code = response.url.split('/')[4]  # www.thebluealliance.com/api/v2/event/{event_code}/matches
		print(f'Fetched Ranking Data for {event_code}..')
		matches = content
		recorded_matches = session.query(TrueSkillMatchV1).filter(TrueSkillMatchV1.event_key == event_code).count()
		if recorded_matches == len(matches):
			print(f'All matches for {event_code} already recorded')
			session.close()
			return
		elif recorded_matches > 0:
			session.query(TrueSkillMatchV1).filter(TrueSkillMatchV1.event_key == event_code).delete()
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
			# Checking if Match wasn't recorded (look at 2017week0 to know what I mean because I can't articulate well enough)
			if match.get('score_breakdown', None) is None:
				continue

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
				print('Error Processing Match. Invalid Data Type. Raw data:', match)
				session.close()
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
					elif tie_breaker_winner == 'replay':
						winner = 'draw'
					else:
						print('Error Determining Tie Breaker. Match Key:', match_key)
						session.close()
						return

			session.add(TrueSkillMatchV1(
				winning_alliance=winner,
				blue_1=int(re.sub("\D", "", blue_1)),
				blue_2=int(re.sub("\D", "", blue_2)),
				blue_3=int(re.sub("\D", "", blue_3)),
				red_1=int(re.sub("\D", "", red_1)),
				red_2=int(re.sub("\D", "", red_2)),
				red_3=int(re.sub("\D", "", red_3)),
				event_key=event_code,
				match_key=match_key
			))
		print(f'Saving Data for {event_code}')
		session.commit()
		print(f'Saved Data for {event_code}')
		session.close()

	data_fetcher = DataFetcher()
	event_code_fetcher = EventCodeFetcher()
	data_fetcher.get_match_data_for_events(event_code_fetcher.list_of_all_event_codes(), fetch_and_save_data)

save_match_data()

calculate_ratings()
save_ratings_to_db([[team_number, rating.mu, rating.sigma] for team_number, rating in ratings.items()])
save_ratings_to_csv(name='world-trueskill-rankings', append_timestamp=True)
