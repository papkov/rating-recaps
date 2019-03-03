from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FieldList, FormField
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
    patronymic = StringField('Отчество')
    birthdate = DateField('Дата рождения', validators=[InputRequired()])

    find = SubmitField()
    remove = SubmitField()


# Dynamically changing form that encapsulates all the fields
class RecapsForm(FlaskForm):

    idteam = StringField('ID', validators=[InputRequired()])
    team_name = StringField('Название', validators=[InputRequired()])
    town = StringField('Город')
    institute = StringField('Вуз')
    player_forms = FieldList(FormField(PlayerForm), min_entries=0)

