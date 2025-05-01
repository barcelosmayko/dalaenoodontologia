from .base import db
from datetime import datetime
from flask_login import UserMixin # Import UserMixin
from flask_bcrypt import Bcrypt # Import Bcrypt

bcrypt = Bcrypt()

class Paciente(db.Model, UserMixin): # Inherit from UserMixin
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False) # Add password hash field
    # Adicionar outros campos relevantes, como data de nascimento, etc.
    consultas = db.relationship("Consulta", backref="paciente", lazy=True)

    def __init__(self, nome, email, password, telefone=None):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # Flask-Login required methods are inherited from UserMixin (like is_authenticated, is_active, is_anonymous)
    # get_id is also inherited and returns self.id by default, which is correct here.

    def __repr__(self):
        return f"<Paciente {self.nome}>"

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    servico = db.Column(db.String(100), nullable=False) # Ex: "Clínico Geral", "Harmonização"
    dentista = db.Column(db.String(100), nullable=True) # Ex: "Dra. Gabriela Bueno"
    observacoes = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Consulta {self.id} - {self.paciente.nome} em {self.data_hora}>"

