import os
import sys
from datetime import datetime
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from src.models.base import db
from src.models.clinica import Paciente, Consulta, bcrypt
from src.forms import MarcacaoForm, RegistroForm, LoginForm

app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(__file__), 'static'),
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT' 

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
bcrypt.init_app(app) 

# Flask-Login Configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'info' 

@login_manager.user_loader
def load_user(user_id):
    return Paciente.query.get(int(user_id))

with app.app_context():
    db.create_all()

# Context processor for current year and user
@app.context_processor
def inject_context():
    return {'current_year': datetime.utcnow().year, 'current_user': current_user}

# --- Main Page Routes --- 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

# --- Marcacao (Booking) Route --- 
@app.route('/marcacao', methods=['GET', 'POST'])
@login_required 
def marcacao():
    form = MarcacaoForm()
    if request.method == 'GET':
        form.nome.data = current_user.nome
        form.email.data = current_user.email
        form.telefone.data = current_user.telefone
        
    if form.validate_on_submit():
        paciente_id = current_user.id
        nova_consulta = Consulta(
            paciente_id=paciente_id, 
            data_hora=form.data_hora.data,
            servico=form.servico.data,
            observacoes=form.observacoes.data
        )
        db.session.add(nova_consulta)
        try:
            db.session.commit()
            flash('Solicitação de marcação enviada com sucesso! Entraremos em contato para confirmar.', 'success')
            return redirect(url_for('marcacao_sucesso')) 
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao guardar a marcação: {e}', 'danger')

    return render_template('marcacao.html', form=form)

@app.route('/marcacao-sucesso')
@login_required
def marcacao_sucesso():
    return render_template('marcacao_sucesso.html')

# --- Auth Routes --- 

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistroForm()
    if form.validate_on_submit():
        existing_user = Paciente.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Este email já está registado. Por favor, faça login.', 'warning')
            return redirect(url_for('login'))
            
        novo_paciente = Paciente(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            password=form.password.data
        )
        db.session.add(novo_paciente)
        try:
            db.session.commit()
            flash('Conta criada com sucesso! Por favor, faça login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar a conta: {e}', 'danger')
            
    return render_template('registro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        paciente = Paciente.query.filter_by(email=form.email.data).first()
        if paciente and paciente.check_password(form.password.data):
            login_user(paciente)
            flash('Login efetuado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login falhou. Verifique o email e a senha.', 'danger')
            
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout efetuado com sucesso.', 'info')
    return redirect(url_for('index'))

# --- Patient History Route --- 

@app.route('/meu-historico')
@login_required
def meu_historico():
    # Fetch consultations for the currently logged-in user (patient)
    consultas = Consulta.query.filter_by(paciente_id=current_user.id).order_by(Consulta.data_hora.desc()).all()
    return render_template('historico.html', consultas=consultas)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 

