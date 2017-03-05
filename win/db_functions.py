from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, RankingV1
import util
import uuid
from settings import Settings
from typing import Tuple, List, Dict
import exceptions


settings = Settings()
# Connects to the database
engine = create_engine(settings.database_address)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def add_ranking(event_code: str, team: str, ranking: int, won: bool):
	session = DBSession()
	if type(event_code) is not str or type(team) is not str or type(ranking) is not int or type(won) is not bool:
		raise ValueError()
	if session.query(RankingV1).filter(RankingV1.event_code == event_code).filter(RankingV1.team == team).first() is not None:
		session.close()
		raise exceptions.TeamAtEventAlreadyRecorded()
	if session.query(RankingV1).filter(RankingV1.event_code == event_code).filter(RankingV1.ranking == ranking).first() is not None:
		session.close()
		raise exceptions.RankAtEventAlreadyRecorded()
	session.add(RankingV1(
		event_code=event_code,
		team=team,
		ranking=ranking,
		won=won
	))
	session.commit()
	session.close()


def get_rankings() -> Dict[int, Dict[str, int]]:
	session = DBSession()
	rankings = {}
	for ranking in session.query(RankingV1).all():  # type: RankingV1
		rank = rankings.get(ranking.ranking, {})
		rank['instances'] = rank.get('instances', 0) + 1
		win_delta = 1 if ranking.won else 0
		rank['wins'] = rank.get('wins', 0) + win_delta
		rankings[ranking.ranking] = rank
	return rankings
