import json
from db_setup import MatchV7
from db_functions import DBSession

included = ('2017cars', 'nec', 'pine-tree')

session = DBSession()
scouts = {}

for match in session.query(MatchV7).filter(MatchV7.event_name.in_(included)).all():  # type: MatchV7
	scouts[match.scout_name] = scouts.get(match.scout_name, 0) + 1

session.close()

print(json.dumps(scouts, indent=4))
