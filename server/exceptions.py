class NotYetImplemented(Exception):
	pass


class MatchDataOutdated(Exception):
	pass


class GenericException(Exception):
	def __init__(self, error_code: int, error_message: str, fields: str):
		self.error_code = error_code
		self.error_message = error_message
		self.fields = fields
