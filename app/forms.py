from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FieldList, FormField, RadioField
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
    other = StringField('Другое')

    find = SubmitField()
    remove = SubmitField()


class InvitationForm(FlaskForm):
    position = StringField('ректору (должность в дательном падеже)')
    first_name = StringField('Иван')
    second_name = StringField('Иванович')
    surname = StringField('Иванову (фамилия в дательном падеже)')
    university = StringField('Вуз в дательном падеже')
    email = StringField('ivanov@uni.ru')
    # university/institute, team_name and recaps come from RecapsForm


# Dynamically changing form that encapsulates all the fields
class RecapsForm(FlaskForm):
    idteam = StringField('ID', validators=[InputRequired()])
    team_name = StringField('Название', validators=[InputRequired()])
    town = StringField('Город', validators=[InputRequired()])
    institute = StringField('Вуз', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired()])

    player_forms = FieldList(FormField(PlayerForm), min_entries=0)
    invitation_form = FormField(InvitationForm)


