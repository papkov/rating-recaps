from flask import render_template, flash, redirect, url_for, request, send_from_directory

from app.rating import *
from app.form_utils import *


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():

    # Create forms
    team_form, player_forms = restore_forms_session()
    send_form = FlaskForm()

    # Search for team by id or create a new team
    app.logger.debug('Request form keys {}'.format([k for k in request.form.keys()]))
    # if team_form.validate_on_submit():
    if request.method == 'POST' and 'btn-find-team' in request.form:
        app.logger.info('Validate on submit ID')

        # If find existing team
        if request.form['idteam'] and request.form['idteam'] != "0":
            # Get general team info
            team_info = get_team_info(request.form['idteam'])
            flash('Requested ID {} for team {}'.format(request.form['idteam'], team_info["name"]))
            populate_team_form(team_form, team_info)
            # session['team_form'] = team_form.data

            # Get base recaps, pre-fill recaps form with it
            team_recaps = get_base_recaps(team_form.idteam.data)
            player_forms = []
            for idplayer in team_recaps['players']:
                player_info = get_player_info(idplayer)
                player_form = PlayerForm()
                populate_player_form(player_form, player_info)
                player_forms.append(player_form)

            # session['player_forms'] = [f.data for f in player_forms]
        # If create a new team with id 0
        else:
            team_form = TeamForm()
            team_form.idteam.data = '0'
            app.logger.info('Create a new team with ID 0')
            flash('Create a new team with ID 0')
            player_forms = []
            # Create six player forms by default
            for i in range(6):
                player_form = PlayerForm()
                player_forms.append(player_form)

        # return redirect(url_for('index'))

    # Handle find player by id
    if request.method == 'POST' and 'btn-find-player' in request.form:
        if request.form['idplayer'] != 0:
            player_info = get_player_info(request.form['idplayer'])
            form_id = int(request.form['btn-find-player'])
            populate_player_form(player_forms[form_id], player_info)

    # Handle remove player
    if request.method == 'POST' and 'btn-remove-player' in request.form:
        form_id = int(request.form['btn-remove-player'])
        app.logger.info('Remove player {}'.format(form_id))
        del player_forms[form_id]

    # Handle add player
    if request.method == 'POST' and 'btn-add-player' in request.form:
        app.logger.info('Add new player')
        player_form = PlayerForm()
        player_forms.append(player_form)

    # Handle clean form
    if request.method == 'POST' and 'btn-reset-team' in request.form:
        app.logger.info('Reset fields')
        if 'player_forms' in session:
            for player_form in player_forms:
                reset_player_form(player_form)
        session.clear()

    # Handle save or send recaps
    if request.method == 'POST' and ('btn-save-recaps' in request.form or 'btn-send-recaps' in request.form):
        # print(get_csv(player_forms, team_form))
        save_csv(player_forms, team_form)
        return redirect(url_for('safe_csv_sender', filename='recaps_{}.csv'.format(team_form.idteam.data)))

    dump_forms_session(team_form, player_forms)
    return render_template('index.html', title='Home', team_form=team_form,
                           player_forms=player_forms, send_form=send_form)


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
    return send_from_directory('recaps',
                               filename,
                               mimetype='text/csv',
                               as_attachment=True,
                               attachment_filename=filename
                               )

