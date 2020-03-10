from app import app
from flask import session
from app.forms import *
import io
import pandas as pd
import os
from app.invitation import *
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


def save_csv_recaps(recaps_form, folder_name='collected_recaps'):
    rating_strs = []
    for e in recaps_form.player_forms.entries:
        rating_str = ','.join([recaps_form.idteam.data.strip(),
                               f'"{recaps_form.team_name.data.strip()}"',
                               recaps_form.town.data.strip(),
                               e.form.status.data.strip(),
                               e.form.idplayer.data.strip(),
                               e.form.surname.data.strip(),
                               e.form.name.data.strip(),
                               e.form.patronymic.data.strip(),
                               str(e.form.birthdate.data) if e.form.birthdate.data is not None else '',
                               f'"{e.form.other.data}"' if e.form.other.data is not None else '',
                               recaps_form.institute.data if recaps_form.institute.data is not None else '',
                               ])

        rating_strs.append(rating_str)

    txt = '\n'.join(rating_strs)

    if folder_name not in os.listdir('.'):
        os.mkdir(os.path.join('.', folder_name))

    fn = os.path.join('.', folder_name, 'recaps_{}.csv'.format(recaps_form.idteam.data.strip()))
    with io.open(fn, 'w+', encoding="utf-8") as f:
        f.write(txt)


def validate_invitation(recaps_form):
    return recaps_form.invitation_form.position.data and  \
           recaps_form.invitation_form.first_name.data and \
           recaps_form.invitation_form.second_name.data and \
           recaps_form.invitation_form.surname.data and \
           recaps_form.invitation_form.email.data and \
           recaps_form.invitation_form.university.data


def save_team_info_csv(recaps_form, fn='teams.csv'):
    basic = ','.join([
        recaps_form.idteam.data,
        recaps_form.team_name.data,
        recaps_form.town.data,
        recaps_form.email.data,
    ])

    if validate_invitation(recaps_form):
        invitation = ','.join([
            recaps_form.invitation_form.position.data,
            recaps_form.invitation_form.first_name.data,
            recaps_form.invitation_form.second_name.data,
            recaps_form.invitation_form.surname.data,
            recaps_form.invitation_form.email.data
        ])
        basic = ','.join([basic, invitation])

    path = os.path.join('./data/', fn)
    with open(path, 'a+') as f:
        f.write(basic + '\n')


def save_invitation_docx(recaps_form):
    try:
        invitation_id = len(os.listdir('./invitations/')) + 15
        get_invitation(team_id=recaps_form.idteam.data,
                       invitation_id=invitation_id,
                       position=recaps_form.invitation_form.position.data,
                       university=recaps_form.invitation_form.university.data,
                       first_name=recaps_form.invitation_form.first_name.data,
                       second_name=recaps_form.invitation_form.second_name.data,
                       surname=recaps_form.invitation_form.surname.data,
                       team_name=recaps_form.team_name.data,
                       recaps=[' '.join([e.form.surname.data, e.form.name.data, e.form.patronymic.data]) +
                               (f', {e.form.other.data}' if e.form.other.data else '')
                               for e in recaps_form.player_forms.entries])
    except FileNotFoundError as e:
        print('File not found', e)
