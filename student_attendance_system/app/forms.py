from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from app.models import Student_User

class RegistrationForm(FlaskForm):
    id=IntegerField('ID',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    batchid = StringField('Batch ID',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_id(self, id):
        idn = Student_User.query.filter_by(id=id.data).first()
        if idn:
            raise ValidationError('That id is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = Student_User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')