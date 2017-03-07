import json
import util


class Settings:
	def __init__(self):
		self.settings = {}
		self.read_settings()

		self.dev_mode = self.settings.get('dev_mode', False)
		self.public_address = self.settings.get('public_address', '')
		self.database_address = self.settings.get('database_address', '')

	def read_settings(self):
		with open(util.path_to_this_files_directory() + 'settings.json') as json_data:
			self.settings = json.load(json_data)
