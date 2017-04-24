import curio
import curio_http
import json
import requests
from typing import List, Dict
from settings import Settings


class EventCodeFetcher:

	def __init__(self):
		self.settings = Settings()

	def list_of_all_event_codes(self):
		url = 'https://www.thebluealliance.com/api/v2/events/2017'
		headers = {
			'X-TBA-App-Id': self.settings.app_id
		}
		events = requests.get(url, headers=headers).json()
		return [event['key'] for event in events]


class EventDataFetcher:

	def __init__(self):
		self.settings = Settings()

	async def fetch_one(self, url):
		headers = {
			'X-TBA-App-Id': self.settings.app_id
		}
		async with curio_http.ClientSession() as session:
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


def print_all_event_data():

	def print_event_data(response, content):
		print('GET %s' % response.url)
		print(content)
		print()

	event_code_fetcher = EventCodeFetcher()
	event_data_fetcher = EventDataFetcher()

	event_data_fetcher.get_event_data(event_code_fetcher.list_of_all_event_codes(), print_event_data)


def list_of_all_event_data():
	response_list = []

	def add_to_list(response, content):
		response_list.append(content)

	event_code_fetcher = EventCodeFetcher()
	event_data_fetcher = EventDataFetcher()

	event_data_fetcher.get_event_data(event_code_fetcher.list_of_all_event_codes(), add_to_list)

	return response_list

a = list_of_all_event_data()
print(len(a))  # 179
print(json.dumps(a, indent=4, sort_keys=True))
