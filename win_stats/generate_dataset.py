import util
from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Tuple, List, Dict
from settings import Settings
import requests
import re
import json

Base = declarative_base()


class TrueSkillMatchV1(Base):
	__tablename__ = 'TrueSkillMatchV1'
	pk = Column(Integer, primary_key=True)
	winning_alliance = Column(String(4))
	blue_1 = Column(Integer)
	blue_2 = Column(Integer)
	blue_3 = Column(Integer)
	red_1 = Column(Integer)
	red_2 = Column(Integer)
	red_3 = Column(Integer)
	event_key = Column(String(10))
	match_key = Column(String(20))


class TrueSkillTeamV1(Base):
	__tablename__ = 'TrueSkillTeamV1'
	pk = Column(Integer, primary_key=True)
	team_number = Column(Integer)
	mu = Column(Float)
	sigma = Column(Float)


class GraphTeamInfoV4(Base):
	__tablename__ = 'GraphTeamInfoV4'
	pk = Column(Integer, primary_key=True)
	team_number = Column(Integer)
	region = Column(Text(collation='utf8_general_ci'))
	nickname = Column(Text(collation='utf8_general_ci'))


settings = Settings()
engine = create_engine(settings.database_address)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def get_team_info(team_number: int) -> Dict:
	session = DBSession()
	row = session.query(GraphTeamInfoV4).filter(GraphTeamInfoV4.team_number == team_number).first()
	if row is None:
		print(f'Querying TBA for Team Info: {team_number}')
		url = f'https://www.thebluealliance.com/api/v2/team/frc{team_number}'
		headers = {
			'X-TBA-App-Id': settings.app_id
		}
		response = requests.get(url, headers=headers).json()
		session.add(GraphTeamInfoV4(
			team_number=team_number,
			region=response['region'],
			nickname=response['nickname']
		))
		session.commit()
		session.close()
		return {
			'region': response['region'],
			'nickname': response['nickname']
		}
	else:
		session.close()
		return {
			'region': row.region,
			'nickname': row.nickname
		}


def generate_nodes_and_edges_filtered(filter_team: int, instance_thickness=False):
	session = DBSession()
	nodes = {}
	connections = {}
	for match in session.query(TrueSkillMatchV1).filter(TrueSkillMatchV1.blue_1 == filter_team or TrueSkillMatchV1.blue_2 == filter_team or TrueSkillMatchV1.blue_3 == filter_team or TrueSkillMatchV1.red_1 == filter_team or TrueSkillMatchV1.red_2 == filter_team or TrueSkillMatchV1.red_3 == filter_team).all():  # type: TrueSkillMatchV1
		for team in {match.blue_1, match.blue_2, match.blue_3, match.red_1, match.red_2, match.red_3}:  # type: int
			if (team in nodes) is False:
				team_trueskill_info = session.query(TrueSkillTeamV1).filter(TrueSkillTeamV1.team_number == team).first()  # TrueSkillTeamV1
				team_info = get_team_info(team)
				nodes[team] = {
					'id': team,
					'label': str(team),
					'title': f'{team_info["nickname"]}<br>Region: {team_info["region"]}',
					'value': team_trueskill_info.mu,
					'group': team_info['region']
				}
			for team_2nd_loop in {match.blue_1, match.blue_2, match.blue_3, match.red_1, match.red_2, match.red_3}:
				if team != team_2nd_loop:
					connections[team] = connections.get(team, {})
					connections[team][team_2nd_loop] = connections[team].get(team_2nd_loop, 0) + 1
	edges = []
	for team_number, value in connections.items():
		for other_team, instances in value.items():
			edges.append({
				'from': team_number,
				'to': other_team,
				'width': instances if instance_thickness else 1
			})
	session.close()
	return [node for team, node in nodes.items()], edges


def generate_nodes_and_edges(instance_thickness=False):
	session = DBSession()
	nodes = {}
	connections = {}
	for match in session.query(TrueSkillMatchV1).all():  # type: TrueSkillMatchV1
		for team in {match.blue_1, match.blue_2, match.blue_3, match.red_1, match.red_2, match.red_3}:  # type: int
			if (team in nodes) is False:
				team_trueskill_info = session.query(TrueSkillTeamV1).filter(TrueSkillTeamV1.team_number == team).first()  # TrueSkillTeamV1
				team_info = get_team_info(team)
				nodes[team] = {
					'id': team,
					'label': str(team),
					'title': f'{team_info["nickname"]}<br>Region: {team_info["region"]}',
					'value': team_trueskill_info.mu,
					'group': team_info['region']
				}
			for team_2nd_loop in {match.blue_1, match.blue_2, match.blue_3, match.red_1, match.red_2, match.red_3}:
				if team != team_2nd_loop:
					connections[team] = connections.get(team, {})
					connections[team][team_2nd_loop] = connections[team].get(team_2nd_loop, 0) + 1
	edges = []
	for team_number, value in connections.items():
		for other_team, instances in value.items():
			edges.append({
				'from': team_number,
				'to': other_team,
				'width': instances if instance_thickness else 1
			})
	session.close()
	return [node for team, node in nodes.items()], edges

nodes_, edges_ = generate_nodes_and_edges()
data = {
	'nodes': nodes_,
	'edges': edges_
}

with open('connections/data.json', 'w') as fp:
	json.dump(data, fp)
