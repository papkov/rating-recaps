from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired


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


class TeamForm(FlaskForm):
    idteam = StringField('ID', validators=[InputRequired()])
    team_name = StringField('Название', validators=[InputRequired()])
    town = StringField('Город')
    institute = StringField('Вуз')


# Dynamically changing form that encapsulates all the fields
class RecapsForm(FlaskForm):

    idteam = StringField('ID', validators=[InputRequired()])
    team_name = StringField('Название', validators=[InputRequired()])
    town = StringField('Город')
    institute = StringField('Вуз')

    def __new__(cls, n_players, **kwargs):
        SelectField()
        fields = dict(
            idplayer=[StringField, {'label': 'ID', 'validators': [InputRequired()]}],
            status=[SelectField, {'label': 'Статус', 'choices': [('Б', 'Б'), ('К', 'К'), ('Л', 'Л')],
                                  'validators': [InputRequired()]}],
            surname=[StringField, {'label': 'Фамилия', 'validators': [InputRequired()]}],
            name=[StringField, {'label': 'Имя', 'validators': [InputRequired()]}],
            patronymic=[StringField, {'label': 'Отчество', 'validators': [InputRequired()]}],
            birthdate=[DateField, {'label': 'Дата рождения', 'validators': [InputRequired()]}]
        )

        for i in range(n_players):
            for name in fields:
                field_name = "{}_{}".format(name, i)
                field = fields[name][0](**fields[name][1])
                setattr(cls, field_name, field)

        return super(RecapsForm, cls).__new__(cls, **kwargs)

