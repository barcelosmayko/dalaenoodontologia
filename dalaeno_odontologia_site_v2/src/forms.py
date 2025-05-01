from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SelectField, DateTimeLocalField, TextAreaField, SubmitField, PasswordField # Added PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo # Added EqualTo

class MarcacaoForm(FlaskForm):
    nome = StringField("Nome Completo", validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    telefone = TelField("Telefone (Opcional)")
    servico = SelectField("Serviço Desejado", choices=[
        ("", "-- Selecione o Serviço --"), 
        ("Clínico Geral", "Clínico Geral"), 
        ("Harmonização Orofacial", "Harmonização Orofacial"),
        ("Avaliação", "Avaliação / Consulta Inicial")
    ], validators=[DataRequired()])
    data_hora = DateTimeLocalField("Data e Hora Preferencial", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    observacoes = TextAreaField("Observações (Opcional)")
    submit = SubmitField("Solicitar Marcação")

class RegistroForm(FlaskForm):
    nome = StringField("Nome Completo", validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    telefone = TelField("Telefone (Opcional)")
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("password", message="As senhas devem ser iguais.")])
    submit = SubmitField("Registar")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    # remember = BooleanField("Lembrar-me") # Optional: Add remember me functionality later
    submit = SubmitField("Login")

