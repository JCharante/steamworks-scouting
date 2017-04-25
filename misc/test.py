from asynchronous_fetcher import DataFetcher
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
