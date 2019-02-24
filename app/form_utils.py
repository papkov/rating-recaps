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


def add_players_to_form(recaps_form, n_players=1):

    next_player_id = 0
    if not hasattr(recaps_form, 'next_player_id'):
        setattr(recaps_form, 'next_player_id', next_player_id)
    else:
        next_player_id = getattr(recaps_form, 'next_player_id')

    fields = dict(
        idplayer={'label': 'ID'},
        status={'label': 'Статус', 'choices': [('Б', 'Б'), ('К', 'К'), ('Л', 'Л')]},
        surname={'label': 'Фамилия'},
        name={'label': 'Имя'},
        patronymic={'label': 'Отчество'},
        birthdate={'label': 'Дата рождения'}
    )

    for i in range(n_players):
        for name in fields.keys():
            field_name = "{}_{}".format(name, next_player_id)
            if name == 'status':
                field = SelectField(**fields[name], validators=[InputRequired()])
            elif name == 'birthdate':
                field = DateField(**fields[name], validators=[InputRequired()])
            else:
                field = StringField(**fields[name], validators=[InputRequired()])
            setattr(recaps_form, field_name, field)
        next_player_id += 1

    setattr(recaps_form, 'next_player_id', next_player_id)



def delete_player_form(player_form, player_form_id):
    for pf in player_fields:
        delattr(player_form, '{}_{}'.format(pf, player_form_id))
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


def form_to_str(player_form, team_form, include_birthdate=True, include_institute=True):
    rating_str = ';'.join([team_form.idteam.data,
                           team_form.team_name.data,
                           team_form.town.data,
                           player_form.status.data,
                           player_form.idplayer.data,
                           player_form.surname.data,
                           player_form.name.data,
                           player_form.patronymic.data])
    print(team_form.institute)
    print(player_form.birthdate)
    print(player_form.idplayer)
    if include_birthdate and player_form.birthdate.data is not None:
        rating_str = ';'.join([rating_str, str(player_form.birthdate.data)])
    if include_institute and team_form.institute.data is not None:
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
