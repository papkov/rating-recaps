from app import app
from flask import session
from app.forms import *
import io
import os


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
    return


def reset_player_form(player_form):
    player_form.idplayer.data = ''
    player_form.status.data = ''  # When populating, all players are from the base recaps
    player_form.name.data = ''
    player_form.surname.data = ''
    player_form.patronymic.data = ''
    player_form.birthdate.data = ''
    return


def populate_team_form(team_form, team_info):
    team_form.idteam.data = team_info['idteam']
    if 'name' in team_info:
        team_form.team_name.data = team_info['name']
    elif 'team_name' in team_info:
        team_form.team_name.data = team_info['team_name']
    team_form.town.data = team_info['town']
    # Fill non-rating fields
    if 'institute' in team_info:
        team_form.institute.data = team_info['institute']


def form_to_str(player_form, team_form, include_birthdate=False, include_institute=False):
    rating_str = ';'.join([team_form.idteam.data,
                           team_form.team_name.data,
                           team_form.town.data,
                           player_form.status.data,
                           player_form.idplayer.data,
                           player_form.surname.data,
                           player_form.name.data,
                           player_form.patronymic.data])
    if include_birthdate:
        rating_str = ';'.join([rating_str, player_form.birthdate.data])
    if include_institute:
        rating_str = ';'.join([rating_str, team_form.institute.data])

    return rating_str


def get_csv(player_forms, team_form):
    rating_strs = [form_to_str(player_form, team_form) for player_form in player_forms if player_form is not None]
    return '\n'.join(rating_strs)


def save_csv(player_forms, team_form, folder_name='collected_recaps'):
    txt = get_csv(player_forms, team_form)

    if folder_name not in os.listdir('.'):
        os.mkdir(os.path.join('.', folder_name))

    fn = os.path.join('.', folder_name, 'recaps_{}.csv'.format(team_form.idteam.data))
    with io.open(fn, 'w+', encoding="utf-8") as f:
        f.write(txt)


def dump_forms_session(team_form, player_forms):
    session['team_form'] = team_form.data
    session['player_forms'] = [pf.data for pf in player_forms]
    return


def restore_forms_session():
    app.logger.debug('Session keys: {}'.format([k for k in session.keys()]))
    team_form = TeamForm()
    player_forms = []
    if 'team_form' in session:
        # team_form.data = session['team_form']
        populate_team_form(team_form, session['team_form'])
    if 'player_forms' in session:
        for spf in session['player_forms']:
            pf = PlayerForm()
            populate_player_form(pf, spf)
            # pf.data = spf.data
            player_forms.append(pf)

    return team_form, player_forms
