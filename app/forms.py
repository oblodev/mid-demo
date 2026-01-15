from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, IntegerField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Optional, NumberRange, Length, Email, EqualTo


class ClientForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message='Name ist erforderlich'),
        Length(max=100, message='Name darf maximal 100 Zeichen haben')
    ])
    birth_date = DateField('Geburtsdatum', validators=[Optional()])
    address = StringField('Adresse', validators=[
        Optional(),
        Length(max=255, message='Adresse darf maximal 255 Zeichen haben')
    ])
    care_level = SelectField('Pflegegrad', choices=[
        ('', '-- Kein Pflegegrad --'),
        ('1', 'Pflegegrad 1'),
        ('2', 'Pflegegrad 2'),
        ('3', 'Pflegegrad 3'),
        ('4', 'Pflegegrad 4'),
        ('5', 'Pflegegrad 5'),
    ], validators=[Optional()])
    notes = TextAreaField('Notizen', validators=[Optional()])


class CareEntryForm(FlaskForm):
    category = SelectField('Kategorie', choices=[
        ('grundpflege', 'Grundpflege'),
        ('medikamente', 'Medikamente'),
        ('vitalzeichen', 'Vitalzeichen'),
        ('ernaehrung', 'Ernährung'),
        ('mobilisation', 'Mobilisation'),
        ('besonderheiten', 'Besonderheiten'),
    ], validators=[DataRequired(message='Kategorie ist erforderlich')])
    description = TextAreaField('Beschreibung', validators=[
        DataRequired(message='Beschreibung ist erforderlich'),
        Length(min=10, message='Beschreibung muss mindestens 10 Zeichen haben')
    ])
    recorded_by = StringField('Erfasst von', validators=[
        DataRequired(message='Mitarbeiter ist erforderlich'),
        Length(max=100)
    ])


class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[
        DataRequired(message='E-Mail ist erforderlich'),
        Email(message='Bitte geben Sie eine gültige E-Mail-Adresse ein')
    ])
    password = PasswordField('Passwort', validators=[
        DataRequired(message='Passwort ist erforderlich')
    ])
    remember = BooleanField('Angemeldet bleiben')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message='Name ist erforderlich'),
        Length(min=2, max=100, message='Name muss zwischen 2 und 100 Zeichen haben')
    ])
    email = StringField('E-Mail', validators=[
        DataRequired(message='E-Mail ist erforderlich'),
        Email(message='Bitte geben Sie eine gültige E-Mail-Adresse ein')
    ])
    password = PasswordField('Passwort', validators=[
        DataRequired(message='Passwort ist erforderlich'),
        Length(min=6, message='Passwort muss mindestens 6 Zeichen haben')
    ])
    password_confirm = PasswordField('Passwort bestätigen', validators=[
        DataRequired(message='Bitte bestätigen Sie Ihr Passwort'),
        EqualTo('password', message='Passwörter stimmen nicht überein')
    ])
