from flask import render_template, flash, redirect, url_for, request, send_from_directory
import pandas as pd
from datetime import datetime

from app.rating import *
from app.form_utils import *
recaps_folder = 'collected_recaps'


# Main page for recaps collection
@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        session.clear()

    if 'n_players' not in session:
        session['n_players'] = 0
    app.logger.debug('Request method {}\nRequest form keys {}'.format(request.method, [k for k in request.form.keys()]))
    app.logger.debug('N players {}'.format(session['n_players']))
    recaps_form = RecapsForm()
    # print(recaps_form.__dict__)

    # Handle status exceptions using while-breaks
    status_code = 200
    # TODO: Is there a more clever way to handle exceptions than while-break?
    while status_code == 200:

        # Handle find team request
        if request.method == 'POST' and 'btn-find-team' in request.form:
            app.logger.info('Look for team id {}'.format(request.form['idteam']))

            # If find existing team (id presented and not 0)
            if request.form['idteam'] and request.form['idteam'] != "0":

                # Get team info
                status_code, team_info = get_team_info(request.form['idteam'])
                if status_code != 200:
                    flash('Rating request for team info failed with status code {}'.format(status_code))
                    break
                flash('Requested ID {} for team {}'.format(request.form['idteam'], team_info["name"]))

                # Populate our new form with team data from rating.chgk.info
                populate_team_form(recaps_form, team_info)

                # Clean form if it's filled with something
                for i in range(len(recaps_form.player_forms.entries)):
                    recaps_form.player_forms.pop_entry()

                # Get base recaps, pre-fill recaps form with it
                status_code, team_recaps = get_base_recaps(recaps_form.idteam.data)
                if status_code != 200:
                    flash('Rating request for base recaps failed with status code {}'.format(status_code))
                    break
                if not team_recaps:
                    flash('Error! There are no base recaps for team {}'.format(request.form['idteam']))
                    for i in range(6):
                        recaps_form.player_forms.append_entry()
                    break

                # Populate form with player data
                for i, idplayer in enumerate(team_recaps['players']):
                    status_code, player_info = get_player_info(idplayer)
                    if status_code != 200:
                        flash('Rating request for player {} info failed with status code {}'.format(idplayer, status_code))
                        break
                    else:
                        recaps_form.player_forms.append_entry()
                        populate_player_form(recaps_form.player_forms.entries[-1].form, player_info)

            # If we create a new team with id 0
            else:
                app.logger.info('Create a new team with ID 0')
                flash('Create a new team with ID 0')

                # Clean form if it's filled with something
                for i in range(len(recaps_form.player_forms.entries)):
                    recaps_form.player_forms.pop_entry()

                for i in range(6):
                    recaps_form.player_forms.append_entry()

                recaps_form.idteam.data = '0'
                recaps_form.team_name.data = ''
                recaps_form.institute.data = ''
                recaps_form.town.data = ''

        # Handle find player by id
        if request.method == 'POST' and 'btn-find-player' in request.form:
            # Set field names
            btn_name = request.form['btn-find-player']
            form_id = int(btn_name.split('-')[1])
            field_name = 'player_forms-{}-idplayer'.format(form_id)

            if request.form[field_name] != 0:
                app.logger.info('Look for player id {}'.format(request.form[field_name]))
                status_code, player_info = get_player_info(request.form[field_name])
                if status_code != 200:
                    flash('Rating request for player {} info failed with status code {}'.format(request.form[field_name], status_code))
                    break

                for e in recaps_form.player_forms.entries:
                    if e.form.find.name == btn_name:
                        populate_player_form(e.form, player_info)
                app.logger.info('Populated form {} with data from id {}'.format(form_id, request.form[field_name]))

        # Handle remove player
        if request.method == 'POST' and 'btn-remove-player' in request.form:
            btn_name = request.form['btn-remove-player']
            print(btn_name)
            form_id = int(btn_name.split('-')[1])
            app.logger.info('Remove player {}'.format(form_id))

            for i, e in enumerate(recaps_form.player_forms.entries):
                if e.form.remove.name == btn_name:
                    # TODO: del is not safe here
                    del recaps_form.player_forms.entries[i]
                    break

        # Handle add player
        if request.method == 'POST' and 'btn-add-player' in request.form:
            app.logger.info('Add new player')
            recaps_form.player_forms.append_entry()

        # Handle clean form
        if request.method == 'POST' and 'btn-reset-team' in request.form:
            app.logger.info('Reset fields')
            for e in recaps_form.player_forms.entries:
                reset_player_form(e.form)
            session.clear()

        # Handle save or send recaps
        if request.method == 'POST' and ('btn-save-recaps' in request.form or 'btn-send-recaps' in request.form):
            if not recaps_form.validate():
                flash('Error! Validation failed')
                break

            save_csv_recaps(recaps_form)
            fn = 'recaps_{}.csv'.format(recaps_form.idteam.data)
            if 'btn-save-recaps' in request.form:
                flash('Form saved!')
                return redirect(url_for('safe_csv_sender', filename=fn))
            else:
                flash('Form saved!')

        break

    return render_template('index.html', title='Home', recaps_form=recaps_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))

    return render_template("login.html", title="Sign in", form=form)


@app.route('/<filename>')
def safe_csv_sender(filename):
    app.logger.info('Download file {}'.format(filename))
    return send_from_directory(recaps_folder,
                               filename,
                               mimetype='text/csv',
                               as_attachment=True,
                               attachment_filename=filename
                               )


@app.route('/accepted')
def accepted():
    if recaps_folder not in os.listdir('.'):
        os.mkdir(os.path.join(recaps_folder))

    accepted_fn = 'accepted.csv'
    columns = ['ID', 'Название', 'Город', 'Вуз']
    accepted_csv = None
    if accepted_fn in os.listdir(recaps_folder):
        accepted_csv = pd.read_csv(os.path.join(recaps_folder, accepted_fn), header=0, index_col=0)

    collected_ids = [int(fn.split('_')[1].split('.')[0]) for fn in os.listdir(recaps_folder) if fn.startswith('recaps_')]

    if accepted_csv is None:
        accepted_csv = pd.DataFrame(columns=columns + ['Время'])

    for team_id in collected_ids:
        if team_id not in accepted_csv['ID'].tolist():

            # Could be rewritten to fetch data from rating.chgk.info
            recaps_path = os.path.join(recaps_folder, 'recaps_{}.csv'.format(team_id))
            team_recaps = pd.read_csv(recaps_path, index_col=None,
                                      header=None, sep=';')
            modification_time = os.path.getmtime(recaps_path)
            modification_time = datetime.utcfromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')

            # Get team id, name, town and institute
            team_info = team_recaps.iloc[:1, [0, 1, 2, -1]]
            team_info.columns = columns
            team_info['Время'] = modification_time

            accepted_csv = pd.concat([accepted_csv, team_info], axis=0).reset_index(drop=True).sort_values('Время')

    accepted_csv.to_csv(os.path.join(recaps_folder, accepted_fn))
    return render_template("accepted.html", title="Accepted",
                           table=accepted_csv.to_html(classes=["table", "table-striped", "table-hover"],
                                                      col_space=50, index=False))
