import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import joblib

import database as db
import analysis
from forms import LoginForm, RDPForm, QuestionamentoForm, CrencaForm, GratidaoForm

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.login_message_category = "error"

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = db.get_db_connection()
    user_data = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user_data:
        return User(id=user_data['id'], username=user_data['username'])
    return None

MODEL_PATH = "cbt_distortion_model.joblib"
model_bundle = None
if os.path.exists(MODEL_PATH):
    try:
        model_bundle = joblib.load(MODEL_PATH)
        print(f"Modelo de ML '{MODEL_PATH}' carregado.")
    except Exception as e:
        print(f"Erro ao carregar o modelo de ML: {e}")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        conn = db.get_db_connection()
        user_data = conn.execute('SELECT * FROM usuarios WHERE username = ?', (form.username.data,)).fetchone()
        conn.close()
        if user_data and check_password_hash(user_data['password_hash'], form.password.data):
            user = User(id=user_data['id'], username=user_data['username'])
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Usuário ou senha inválidos.', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    rdps = db.get_all_rdps()
    crencas = db.get_all_crencas()
    return render_template('index.html', rdps=rdps, crencas=crencas)

@app.route('/rdp/novo', methods=['GET', 'POST'])
@login_required
def novo_rdp():
    form = RDPForm()
    form.id_crenca_associada.choices = [(c['id'], f"[{c['tipo']}] {c['descricao']}") for c in db.get_all_crencas()]
    form.id_crenca_associada.choices.insert(0, (0, 'Nenhuma crença associada'))
    distorcoes_db = db.get_all_distorcoes()
    if form.validate_on_submit():
        db.add_rdp(form.situacao.data, form.pensamentos_automaticos.data, form.emocoes.data, form.comportamento.data, form.id_crenca_associada.data, form.distorcoes.data)
        flash('Novo RDP salvo com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('novo_rdp.html', form=form, distorcoes_db=distorcoes_db)

@app.route('/rdp/<int:rdp_id>', methods=['GET', 'POST'])
@login_required
def detalhe_rdp(rdp_id):
    rdp = db.get_rdp_by_id(rdp_id)
    if rdp is None:
        flash('RDP não encontrado.', 'error')
        return redirect(url_for('index'))
    form = QuestionamentoForm()
    if form.validate_on_submit():
        db.add_questionamento(rdp_id, form.pergunta.data, form.resposta.data, form.pensamento_alternativo.data, form.nivel_dissonia_cognitiva.data)
        flash('Análise salva com sucesso!', 'success')
        return redirect(url_for('detalhe_rdp', rdp_id=rdp_id))
    return render_template('detalhe_rdp.html', rdp=rdp, form=form)

@app.route('/crencas', methods=['GET', 'POST'])
@login_required
def gerenciar_crencas():
    form = CrencaForm()
    if form.validate_on_submit():
        db.add_crenca(form.descricao.data, form.tipo.data, form.categoria_triade.data, form.nivel_conviccao.data)
        flash('Nova crença adicionada com sucesso!', 'success')
        return redirect(url_for('gerenciar_crencas'))
    crencas = db.get_all_crencas()
    return render_template('crencas.html', crencas=crencas, form=form)

@app.route('/gratidao', methods=['GET', 'POST'])
@login_required
def diario_gratidao():
    form = GratidaoForm()
    if form.validate_on_submit():
        db.add_gratidao_entry(form.entrada.data)
        flash('Entrada de gratidão salva!', 'success')
        return redirect(url_for('diario_gratidao'))
    entradas = db.get_all_gratidao_entries()
    return render_template('gratidao.html', entradas=entradas, form=form)

@app.route('/analise')
@login_required
def pagina_analise():
    insights = analysis.identificar_insights_preditivos()
    grafico_distorcoes = analysis.gerar_grafico_distorcoes()
    nuvem_pensamentos = analysis.gerar_nuvem_palavras('pensamentos_automaticos')
    nuvem_situacoes = analysis.gerar_nuvem_palavras('situacao')
    grafico_emocoes = analysis.gerar_grafico_emocoes_tempo()
    return render_template('analise.html', insights=insights, grafico_distorcoes=grafico_distorcoes, nuvem_pensamentos=nuvem_pensamentos, nuvem_situacoes=nuvem_situacoes, grafico_emocoes=grafico_emocoes)

@app.route('/rdp/prever_distorcoes', methods=['POST'])
@login_required
def prever_distorcoes_api():
    if not model_bundle: return jsonify({'erro': 'Modelo não carregado'}), 500
    data = request.get_json()
    texto_pensamento = data.get('texto')
    if not texto_pensamento: return jsonify({'sugestoes': []})
    predicoes = model_bundle['pipeline'].predict([texto_pensamento])
    sugestoes = model_bundle['binarizer'].inverse_transform(predicoes)
    return jsonify({'sugestoes': list(sugestoes[0]) if sugestoes else []})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)