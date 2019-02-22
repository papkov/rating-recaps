import requests
import json
from app import app

api_root = 'http://rating.chgk.info/api'


def get_team_info(idteam):
    app.logger.info('loading info about team ID {}'.format(idteam))
    url = '/'.join([api_root, 'teams', idteam])
    response = requests.get(url)
    return response.status_code, response.json()[0] if response.status_code == 200 else None


def get_base_recaps(idteam):
    app.logger.info('loading recaps team ID {}'.format(idteam))
    url = '/'.join([api_root, 'teams', idteam, 'recaps', 'last'])
    response = requests.get(url)
    return response.status_code, response.json() if response.status_code == 200 else None


def get_player_info(idplayer):
    app.logger.info('loading info for player ID {}'.format(idplayer))
    url = '/'.join([api_root, 'players', idplayer])
    response = requests.get(url)
    return response.status_code, response.json()[0] if response.status_code == 200 else None
