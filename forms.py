from dataclasses import Field
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    usuario = StringField('usuario', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('submit')

class PostForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    endereco = StringField('endereco', validators=[DataRequired()])
    cidade = StringField('cidade', validators=[DataRequired()])
    valor = DecimalField('valor', validators=[DataRequired()])
    submit = SubmitField('submit')
    