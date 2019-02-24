from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FieldList, FormField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired
from markupsafe import Markup


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sigh in")


class PlayerForm(FlaskForm):
    idplayer = StringField('ID', validators=[InputRequired()])
    status = SelectField('Статус', choices=[('Б', 'Б'), ('К', 'К'), ('Л', 'Л')], validators=[InputRequired()])
    surname = StringField('Фамилия', validators=[InputRequired()])
    name = StringField('Имя', validators=[InputRequired()])
    patronymic = StringField('Отчество', validators=[InputRequired()])
    birthdate = DateField('Дата рождения', validators=[InputRequired()])

    find = SubmitField()
    remove = SubmitField()


class TeamForm(FlaskForm):
    idteam = StringField('ID', validators=[InputRequired()])
    team_name = StringField('Название', validators=[InputRequired()])
    town = StringField('Город', validators=[InputRequired()])
    institute = StringField('Вуз', validators=[InputRequired()])


# Dynamically changing form that encapsulates all the fields
class RecapsForm(FlaskForm):

    idteam = StringField('ID', validators=[InputRequired()])
    team_name = StringField('Название', validators=[InputRequired()])
    town = StringField('Город')
    institute = StringField('Вуз')
    player_forms = FieldList(FormField(PlayerForm), min_entries=0)

    #
    # def __new__(cls, n_players, **kwargs):
    #
    #     setattr(cls, 'idteam', StringField('ID', validators=[InputRequired()]))
    #     setattr(cls, 'team_name', StringField('Название', validators=[InputRequired()]))
    #     setattr(cls, 'town', StringField('Город'))
    #     setattr(cls, 'institute', StringField('Вуз'))
    #
    #     fields = dict(
    #         idplayer={'label': 'ID'},
    #         status={'label': 'Статус', 'choices': [('Б', 'Б'), ('К', 'К'), ('Л', 'Л')]},
    #         surname={'label': 'Фамилия'},
    #         name={'label': 'Имя'},
    #         patronymic={'label': 'Отчество'},
    #         birthdate={'label': 'Дата рождения'}
    #     )
    #
    #     for i in range(n_players):
    #         for name in fields.keys():
    #             field_name = "{}_{}".format(name, i)
    #             if name == 'status':
    #                 field = SelectField(**fields[name], validators=[InputRequired()])
    #             elif name == 'birthdate':
    #                 field = DateField(**fields[name], validators=[InputRequired()])
    #             else:
    #                 field = StringField(**fields[name], validators=[InputRequired()])
    #             setattr(cls, field_name, field)
    #
    #     return super(RecapsForm, cls).__new__(cls, **kwargs)

