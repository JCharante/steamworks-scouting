import requests
import util
import db_functions
import exceptions
from settings import Settings


class RankFetcher:

	def __init__(self, event_code: str):
		self.settings = Settings()
		self.event_code = event_code
		self.url = f'https://www.thebluealliance.com/api/v2/event/{event_code}'
		self.headers = {
			'X-TBA-App-Id': self.settings.app_id
		}
		self.ranking_data = []
		self.winning_teams = []

		self.fetch_data()

	def fetch_data(self):
		print(f'Fetching Ranking Data for {self.event_code}..')
		data = requests.get(self.url + '/rankings', headers=self.headers).json()
		self.ranking_data = data[1:]
		print(f'Fetching Event Winner Data for {self.event_code}..')
		data = requests.get(self.url + '/awards', headers=self.headers).json()
		winner_award_names = ['District Event Winner', 'Regional Winners', 'Championship Subdivision Winner']
		if len(data) > 0:  # Some Events have 0 Data
			found_winning_award = False
			for award in data:
				award_name = award.get('name', '')
				if award_name in winner_award_names:
					found_winning_award = True
					recipient_list = award.get('recipient_list', [])
					for recipient in recipient_list:
						team = str(recipient.get('team_number'))
						self.winning_teams.append(team)
			if found_winning_award and len(self.winning_teams) > 0:
				self.save_data()
			else:
				print(f'Could not find any Winning Awards or Winning Teams for {self.event_code}')

	def save_data(self):
		print(f'Saving Data for {self.event_code}')
		for rank in self.ranking_data:
			try:
				ranking = int(rank[0])
				team = str(rank[1])
				won = team in self.winning_teams
				try:
					db_functions.add_ranking(self.event_code, team, ranking, won)
				except exceptions.TeamAtEventAlreadyRecorded:
					break
			except Exception as e:
				print(repr(e))
		print(f'Done Saving Data for {self.event_code}')


def get_2016_event_codes():
	url = 'https://www.thebluealliance.com/api/v2/events/2016'
	settings = Settings()
	headers = {
		'X-TBA-App-Id': settings.app_id
	}
	event_codes = set()
	data = requests.get(url, headers=headers).json()
	for event in data:
		event_code = event.get('key', None)
		if event_code is not None:
			event_codes.add(event_code)
	return event_codes


def get_2016_data():
	for event_code in get_2016_event_codes():
		RankFetcher(event_code)

get_2016_data()

data = [['Rank', 'WinPct']] + [[ranking, float(value.get('wins', 0) / value.get('instances'))] for ranking, value in db_functions.get_rankings().items()]
util.save_as_csv(data, name='2016-chances-of-winning-at-a-ranking')

