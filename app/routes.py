from flask import render_template, flash, redirect, url_for, request, send_from_directory



from app.rating import *
from app.form_utils import *


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

                # Get base recaps, pre-fill recaps form with it
                status_code, team_recaps = get_base_recaps(recaps_form.idteam.data)
                if status_code != 200:
                    flash('Rating request for base recaps failed with status code {}'.format(status_code))
                    break

                # Set n_players based on response, create new recaps form
                session['n_players'] = len(team_recaps['players'])
                print(session['n_players'])
                # recaps_form = RecapsForm(session['n_players'])

                # Populate our new form with team data from rating.chgk.info
                populate_team_form(recaps_form, team_info)

                # Clean form if it's filled with something
                for i in range(len(recaps_form.player_forms.entries)):
                    recaps_form.player_forms.pop_entry()

                # Populate form with player data
                for i, idplayer in enumerate(team_recaps['players']):
                    status_code, player_info = get_player_info(idplayer)
                    if status_code != 200:
                        flash('Rating request for player {} info failed with status code {}'.format(idplayer, status_code))
                        break
                    else:
                        # add_players_to_form(recaps_form)
                        # populate_player_form(recaps_form, player_info, i)
                        recaps_form.player_forms.append_entry()
                        populate_player_form(recaps_form.player_forms.entries[-1].form, player_info)
            # If we create a new team with id 0
            else:
                app.logger.info('Create a new team with ID 0')
                flash('Create a new team with ID 0')

                session['n_players'] = 6
                # recaps_form = RecapsForm(session['n_players'])
                for i in range(session['n_players']):
                    # add_players_to_form(recaps_form)
                    recaps_form.player_forms.append_entry()
                recaps_form.idteam.data = '0'

        # Handle find player by id
        if request.method == 'POST' and 'btn-find-player' in request.form:
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
                    del recaps_form.player_forms.entries[i]
                    break
            # session['n_players'] -= 1
            # delete_player_form(recaps_form, form_id)

        # Handle add player
        if request.method == 'POST' and 'btn-add-player' in request.form:
            app.logger.info('Add new player')

            # session['n_players'] += 1
            # recaps_form = RecapsForm(session['n_players'])
            recaps_form.player_forms.append_entry()
            # populate_recaps_form(recaps_form, request.form)

        # Handle clean form
        if request.method == 'POST' and 'btn-reset-team' in request.form:
            app.logger.info('Reset fields')
            for e in recaps_form.player_forms.entries:
                reset_player_form(e.form)
            session.clear()

        # Handle save or send recaps
        if request.method == 'POST' and ('btn-save-recaps' in request.form or 'btn-send-recaps' in request.form):
            # print(get_csv(player_forms, team_form))
            # render_template('index.html', title='Home', team_form=team_form, player_forms=player_forms, send_form=send_form)
            # save_csv(player_forms, team_form)
            save_csv_recaps(recaps_form)
            flash('Form saved!')
            return redirect(url_for('safe_csv_sender', filename='recaps_{}.csv'.format(recaps_form.idteam.data)))

        # dump_forms_session(team_form, player_forms)

        break

    return render_template('index.html', title='Home', recaps_form=recaps_form)

    # Create forms
    # team_form, player_forms = restore_forms_session()
    # send_form = FlaskForm()
    #
    # # Search for team by id or create a new team
    # app.logger.debug('Request form keys {}'.format([k for k in request.form.keys()]))
    # # if team_form.validate_on_submit():
    # if request.method == 'POST' and 'btn-find-team' in request.form:
    #     app.logger.info('Validate on submit ID')
    #
    #     # If find existing team
    #     if request.form['idteam'] and request.form['idteam'] != "0":
    #         # Get general team info
    #         status_code, team_info = get_team_info(request.form['idteam'])
    #         if status_code != 200:
    #             flash('Rating request for team info failed with status code {}'.format(status_code))
    #         else:
    #             flash('Requested ID {} for team {}'.format(request.form['idteam'], team_info["name"]))
    #             populate_team_form(team_form, team_info)
    #             # session['team_form'] = team_form.data
    #
    #             # Get base recaps, pre-fill recaps form with it
    #             status_code, team_recaps = get_base_recaps(team_form.idteam.data)
    #             if status_code != 200:
    #                 flash('Rating request for base recaps failed with status code {}'.format(status_code))
    #             else:
    #                 player_forms = []
    #                 for idplayer in team_recaps['players']:
    #                     status_code, player_info = get_player_info(idplayer)
    #                     if status_code != 200:
    #                         flash('Rating request for player {} info failed with status code {}'.format(idplayer, status_code))
    #                     else:
    #                         player_form = PlayerForm()
    #                         populate_player_form(player_form, player_info)
    #                         player_forms.append(player_form)
    #
    #         # session['player_forms'] = [f.data for f in player_forms]
    #     # If create a new team with id 0
    #     else:
    #         team_form = TeamForm()
    #         team_form.idteam.data = '0'
    #         app.logger.info('Create a new team with ID 0')
    #         flash('Create a new team with ID 0')
    #         player_forms = []
    #         # Create six player forms by default
    #         for i in range(6):
    #             player_form = PlayerForm()
    #             player_forms.append(player_form)
    #
    #     # return redirect(url_for('index'))
    #
    # # Handle find player by id
    # if request.method == 'POST' and 'btn-find-player' in request.form:
    #     if request.form['idplayer'] != 0:
    #         status_code, player_info = get_player_info(request.form['idplayer'])
    #         if status_code != 200:
    #             flash('Rating request for player {} info failed with status code {}'.format(idplayer, status_code))
    #         else:
    #             form_id = int(request.form['btn-find-player'])
    #             populate_player_form(player_forms[form_id], player_info)
    #
    # # Handle remove player
    # if request.method == 'POST' and 'btn-remove-player' in request.form:
    #     form_id = int(request.form['btn-remove-player'])
    #     app.logger.info('Remove player {}'.format(form_id))
    #     del player_forms[form_id]
    #
    # # Handle add player
    # if request.method == 'POST' and 'btn-add-player' in request.form:
    #     app.logger.info('Add new player')
    #     player_form = PlayerForm()
    #     player_forms.append(player_form)
    #
    # # Handle clean form
    # if request.method == 'POST' and 'btn-reset-team' in request.form:
    #     app.logger.info('Reset fields')
    #     if 'player_forms' in session:
    #         for player_form in player_forms:
    #             reset_player_form(player_form)
    #     session.clear()
    #
    # # Handle save or send recaps
    # if request.method == 'POST' and ('btn-save-recaps' in request.form or 'btn-send-recaps' in request.form):
    #     # print(get_csv(player_forms, team_form))
    #     # render_template('index.html', title='Home', team_form=team_form, player_forms=player_forms, send_form=send_form)
    #     save_csv(player_forms, team_form)
    #     flash('Form saved!')
    #     return redirect(url_for('safe_csv_sender', filename='recaps_{}.csv'.format(team_form.idteam.data)))
    #
    # dump_forms_session(team_form, player_forms)
    # return render_template('index.html', title='Home', team_form=team_form, player_forms=player_forms, send_form=send_form)


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
    return send_from_directory('../collected_recaps',
                               filename,
                               mimetype='text/csv',
                               as_attachment=True,
                               attachment_filename=filename
                               )

