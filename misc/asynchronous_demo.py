import curio
import curio_http
import json
import requests
from typing import List, Dict
from settings import Settings


MAX_CONNECTIONS_PER_HOST = 6
sema = curio.BoundedSemaphore(MAX_CONNECTIONS_PER_HOST)


class EventCodeFetcher:
c
	def __init__(self):
		self.settings = Settings()

	def list_of_all_event_codes(self):
		url = 'https://www.thebluealliance.com/api/v2/events/2017'
		headers = {
			'X-TBA-App-Id': self.settings.app_id
		}
		events = requests.get(url, headers=headers).json()
		return [event['key'] for event in events]


class DataFetcher:

	def __init__(self):
		self.settings = Settings()

	async def fetch_one(self, url):
		headers = {
			'X-TBA-App-Id': self.settings.app_id
		}
		#async with curio_http.ClientSession() as session:
		async with sema, curio_http.ClientSession() as session:
			response = await session.get(url, headers=headers)
			content = await response.json()
			return response, content

	async def main(self, url_list, callback):
		tasks = []

		for url in url_list:
			task = await curio.spawn(self.fetch_one(url))
			tasks.append(task)

		for task in tasks:
			response, content = await task.join()
			callback(response, content)

	def get_event_data(self, event_codes: List[str], callback: any) -> None:
		url_list = [f'https://www.thebluealliance.com/api/v2/event/{event_code}' for event_code in event_codes]
		curio.run(self.main(url_list, callback))

	def get_team_data(self, team_numbers: List[int], callback: any) -> None:
		url_list = [f'https://www.thebluealliance.com/api/v2/team/frc{team_number}' for team_number in team_numbers]
		curio.run(self.main(url_list, callback))

	def get_event_teams_data(self, event_codes: List[str], callback: any) -> None:
		url_list = [f'https://www.thebluealliance.com/api/v2/event/{event_code}/teams' for event_code in event_codes]
		curio.run(self.main(url_list, callback))

	def get_match_data_for_events(self, event_codes: List[str], callback: any) -> None:
		url_list = [f'https://www.thebluealliance.com/api/v2/event/{event_code}/matches' for event_code in event_codes]
		curio.run(self.main(url_list, callback))


def list_of_all_event_data():
	response_list = []

	def add_to_list(response, content):
		response_list.append(content)

	event_code_fetcher = EventCodeFetcher()
	data_fetcher = DataFetcher()

	data_fetcher.get_event_data(event_code_fetcher.list_of_all_event_codes(), add_to_list)

	return response_list


def set_of_team_names_at_events(event_codes):
	response_list = set()

	def add_to_set(response, content):
		for team in content:
			response_list.add(team['nickname'])

	data_fetcher = DataFetcher()

	data_fetcher.get_event_teams_data(event_codes, add_to_set)

	return response_list

if __name__ == '__main__':
	#  Example A: Printing the list of team names that have been to events that we've gone to
	[print(team_name) for team_name in set_of_team_names_at_events(['2017week0', '2017nhgrs', '2017mabos', '2017melew', '2017necmp'])]

	# Example B: Getting a list of responses for /event/{event_code} from every event in 2017.
	a = list_of_all_event_data()
	print(len(a))  # 179
	print(json.dumps(a, indent=4, sort_keys=True))
