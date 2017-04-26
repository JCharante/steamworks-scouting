import curio
import curio_http
import json
import requests
import os
from typing import List, Dict

MAX_CONNECTIONS_PER_HOST = 6
sema = curio.BoundedSemaphore(MAX_CONNECTIONS_PER_HOST)


class EventCodeFetcher:

	def __init__(self):
		pass

	def list_of_all_event_codes(self):
		url = 'https://www.thebluealliance.com/api/v2/events/2017'
		headers = {
			'X-TBA-App-Id': os.environ['tba']
		}
		events = requests.get(url, headers=headers).json()
		return [event['key'] for event in events]


class DataFetcher:

	def __init__(self):
		pass

	async def fetch_one(self, url):
		headers = {
			'X-TBA-App-Id': os.environ['tba']
		}

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
