import requests
from app import app

api_root = 'https://rating.chgk.info/api'
search_player_template = api_root+'/players.json/search?name={name}&surname={surname}&patronymic={patronymic}'


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


def find_player(name='', surname='', patronymic=''):
    app.logger.info('Find player {} {} {}'.format(name, surname, patronymic))
    url = search_player_template.format(name=name, surname=surname, patronymic=patronymic)
    response = requests.get(url)
    return response.status_code, response.json() if response.status_code == 200 else None
