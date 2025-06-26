# forms.py

from flask_wtf import FlaskForm
# Linha 1: Ajuste as importações. Removemos RangeField e adicionamos IntegerField e o validador.
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SelectMultipleField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
    # ... (sem alterações aqui)
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')


class RDPForm(FlaskForm):
    # ... (sem alterações aqui)
    situacao = TextAreaField('Situação', validators=[DataRequired()], render_kw={"rows": 3, "class": "w-full mt-1 p-3 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500"})
    pensamentos_automaticos = TextAreaField('Pensamentos Automáticos', validators=[DataRequired()], render_kw={"rows": 4, "id": "pensamentos_automaticos", "class": "w-full mt-1 p-3 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500"})
    emocoes = StringField('Emoções', validators=[DataRequired()], render_kw={"placeholder": "Ex: Ansiedade 90%, Tristeza 60%", "class": "w-full mt-1 p-3 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500"})
    comportamento = TextAreaField('Comportamento', render_kw={"rows": 3, "class": "w-full mt-1 p-3 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500"})
    id_crenca_associada = SelectField('Crença Associada', coerce=int, render_kw={"class": "w-full mt-1 p-3 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500"})
    distorcoes = SelectMultipleField('Distorções Cognitivas', coerce=int)
    submit = SubmitField('Salvar Registro', render_kw={"class": "bg-teal-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-teal-700 transition duration-300 shadow-md"})

class QuestionamentoForm(FlaskForm):
    # ... (sem alterações nos outros campos)
    pergunta = SelectField('Pergunta Orientadora', choices=[
        'Quais as evidências que apoiam esse pensamento? E quais não apoiam?',
        'Existe uma forma alternativa de ver esta situação?',
        'Qual o pior, o melhor e o mais realista resultado possível?',
        'Qual o efeito de acreditar nesse pensamento? E qual seria o efeito de mudá-lo?',
        'O que eu diria a um amigo que estivesse passando pela mesma situação?'
    ], render_kw={"class": "mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm rounded-md"})
    resposta = TextAreaField('Sua Resposta / Análise', validators=[DataRequired()], render_kw={"rows": 4, "class": "w-full mt-1 p-3 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500"})
    pensamento_alternativo = TextAreaField('Pensamento Alternativo', render_kw={"rows": 3, "class": "w-full mt-1 p-3 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500"})
    # Linha 2: Altere RangeField para IntegerField e adicione o validador e o render_kw
    nivel_dissonia_cognitiva = IntegerField(
        'Nível de convicção no pensamento original agora (0-100%)', 
        validators=[NumberRange(min=0, max=100)],
        default=70, 
        render_kw={"type": "range", "class": "w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"}
    )
    submit = SubmitField('Salvar Análise', render_kw={"class": "bg-teal-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-teal-700 transition duration-300"})


class CrencaForm(FlaskForm):
    # ... (sem alterações nos outros campos)
    descricao = TextAreaField('Descrição da Crença', validators=[DataRequired()], render_kw={"rows": 3, "class": "w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm"})
    tipo = SelectField('Tipo', choices=[('Central', 'Crença Central'), ('Pressuposto Adjacente', 'Pressuposto Adjacente')], render_kw={"class": "w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm"})
    categoria_triade = SelectField('Tríade Cognitiva', choices=[('EU', 'Eu'), ('PESSOAS', 'Pessoas/Outros'), ('MUNDO/FUTURO', 'Mundo/Futuro')], render_kw={"class": "w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm"})
    # Linha 3: Altere RangeField para IntegerField aqui também
    nivel_conviccao = IntegerField(
        'Nível de Convicção (0-100%)', 
        validators=[NumberRange(min=0, max=100)],
        default=70, 
        render_kw={"type": "range", "class": "w-full mt-1"}
    )
    submit = SubmitField('Adicionar', render_kw={"class": "bg-teal-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-teal-700"})

class GratidaoForm(FlaskForm):
    # ... (sem alterações aqui)
    entrada = TextAreaField('Pelo que você é grato(a) hoje?', validators=[DataRequired()], render_kw={"rows": 4, "placeholder": "Liste 3 a 5 coisas...", "class": "w-full mt-1 p-3 border border-gray-300 rounded-md shadow-sm"})
    submit = SubmitField('Salvar Entrada', render_kw={"class": "bg-teal-600 text-white font-bold py-2 px-5 rounded-lg hover:bg-teal-700"})