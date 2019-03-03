from app import app
from flask import session
from app.forms import *
import io
import os
player_fields = ['idplayer', 'status', 'name', 'surname', 'patronymic', 'birthdate']


def populate_player_form(player_form, player_info):
    app.logger.info('Populate form for player ID {}'.format(player_info['idplayer']))

    player_form.idplayer.data = player_info['idplayer']
    player_form.status.data = 'Б'  # When populating, all players are from the base recaps
    player_form.name.data = player_info['name']
    player_form.surname.data = player_info['surname']
    player_form.patronymic.data = player_info['patronymic']
    # Fill non-rating fields
    if 'birthdate' in player_info:
        player_form.birthdate.data = player_info['birthdate']
    if 'status' in player_info:
        player_form.status.data = player_info['status']

    # for pf in player_fields:
    #     field_name = 'player_forms-{}-{}'.format(player_form_id, pf)
    #     if pf in player_info and hasattr(player_form, field_name):
    #         setattr(getattr(player_form, field_name), 'data', player_info[pf])
    return


def reset_player_form(player_form):
    # for i in range(len(player_form)):
    #     for pf in player_fields:
    #         setattr(getattr(player_form, '{}_{}'.format(pf, i)), 'data', '')
    player_form.idplayer.data = ''
    player_form.status.data = ''  # When populating, all players are from the base recaps
    player_form.name.data = ''
    player_form.surname.data = ''
    player_form.patronymic.data = ''
    player_form.birthdate.data = ''
    return


def populate_team_form(team_form, team_info):

    # for field in team_info:
    #     if hasattr(team_form, field):
    #         setattr(getattr(team_form, field), 'data', team_form[field])

    team_form.idteam.data = team_info['idteam']
    if 'name' in team_info:
        team_form.team_name.data = team_info['name']
    elif 'team_name' in team_info:
        team_form.team_name.data = team_info['team_name']
    team_form.town.data = team_info['town']
    # Fill non-rating fields
    # if 'institute' in team_info:
    #     team_form.institute.data = team_info['institute']

    return


def populate_recaps_form(recaps_form, request_form):
    for field in request_form:
        if hasattr(recaps_form, field):
            setattr(getattr(recaps_form, field), 'data', request_form[field])


def save_csv_recaps(recaps_form, include_birthdate=True, include_institute=True, folder_name='collected_recaps'):
    rating_strs = []
    for e in recaps_form.player_forms.entries:
        rating_str = ';'.join([recaps_form.idteam.data,
                               recaps_form.team_name.data,
                               recaps_form.town.data,
                               e.form.status.data,
                               e.form.idplayer.data,
                               e.form.surname.data,
                               e.form.name.data,
                               e.form.patronymic.data])

        if include_birthdate:
            rating_str = ';'.join([rating_str, str(e.form.birthdate.data) if e.form.birthdate.data is not None else ''])
        if include_institute:
            rating_str = ';'.join([rating_str, recaps_form.institute.data if recaps_form.institute.data is not None else ''])
            rating_strs.append(rating_str)

    txt = '\n'.join(rating_strs)

    if folder_name not in os.listdir('.'):
        os.mkdir(os.path.join('.', folder_name))

    fn = os.path.join('.', folder_name, 'recaps_{}.csv'.format(recaps_form.idteam.data))
    with io.open(fn, 'w+', encoding="utf-8") as f:
        f.write(txt)
