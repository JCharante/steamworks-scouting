from asynchronous_fetcher import DataFetcher, EventCodeFetcher
import pytest


class TestDataFetcher:

	def test_one(self):

		def set_of_team_names_at_events(event_codes):
			response_list = set()

			def add_to_set(response, content):
				for team in content:
					response_list.add(team['nickname'])

			data_fetcher = DataFetcher()

			data_fetcher.get_event_teams_data(event_codes, add_to_set)

			return response_list

		assert len(set_of_team_names_at_events(['2017week0', '2017nhgrs', '2017mabos', '2017melew', '2017necmp'])) == 128

	def test_two(self):
		event_code_fetcher = EventCodeFetcher()
		data_fetcher = DataFetcher()

		all_event_codes = event_code_fetcher.list_of_all_event_codes()

		responses = []

		def add_to_list(response, content):
			responses.append(content)

		data_fetcher.get_match_data_for_events(all_event_codes, add_to_list)

		assert len(responses) == len(all_event_codes)
