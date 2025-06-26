import pandas as pd
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64
import re
import database

def get_data_as_dataframe(query):
    conn = database.get_db_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def _plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.close(fig)
    return data

def gerar_grafico_distorcoes():
    query = "SELECT dc.nome FROM rdp_distorcoes rd JOIN distorcoes_cognitivas dc ON rd.id_distorcao = dc.id"
    df = get_data_as_dataframe(query)
    if df.empty: return None
    distorcao_counts = df['nome'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    distorcao_counts.sort_values().plot(kind='barh', ax=ax, color='teal')
    ax.set_title('Frequência de Distorções Cognitivas', fontsize=16)
    ax.set_xlabel('Número de Ocorrências')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return _plot_to_base64(fig)

def gerar_nuvem_palavras(campo):
    query = f"SELECT {campo} FROM rdp"
    df = get_data_as_dataframe(query)
    if df.empty or df[campo].isnull().all(): return None
    text = ' '.join(df[campo].dropna().values)
    stopwords_pt = set(['de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos', 'já', 'está', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'era', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'estão', 'você', 'tinha', 'foram', 'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha', 'numa', 'pelos', 'elas', 'havia', 'seja', 'qual', 'será', 'nós', 'tenho', 'lhe', 'deles', 'essas', 'esses', 'pelas', 'este', 'fosse', 'dele', 'tu', 'te', 'vocês', 'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas', 'dela', 'delas', 'esta', 'estes', 'estas', 'aquele', 'aquela', 'aqueles', 'aquelas', 'isto', 'aquilo', 'estou', 'está', 'estamos', 'estão', 'estive', 'esteve', 'estivemos', 'estiveram', 'estava', 'estávamos', 'estavam', 'estivera', 'estivéramos', 'esteja', 'estejamos', 'estejam', 'estivesse', 'estivéssemos', 'estivessem', 'estiver', 'estivermos', 'estiverem', 'hei', 'há', 'havemos', 'hão', 'houve', 'houvemos', 'houveram', 'houvera', 'houvéramos', 'haja', 'hajamos', 'hajam', 'houvesse', 'houvéssemos', 'houvessem', 'houver', 'houvermos', 'houverem', 'houverei', 'houverá', 'houveremos', 'houverão', 'houveria', 'houveríamos', 'houveriam', 'sou', 'somos', 'são', 'era', 'éramos', 'eram', 'fui', 'foi', 'fomos', 'foram', 'fora', 'fôramos', 'seja', 'sejamos', 'sejam', 'fosse', 'fôssemos', 'fossem', 'for', 'formos', 'forem', 'serei', 'será', 'seremos', 'serão', 'seria', 'seríamos', 'seriam'])
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords_pt, colormap='viridis').generate(text)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return _plot_to_base64(fig)

def parse_emocoes(df_column):
    parsed_data = []
    for item in df_column.dropna():
        match = re.search(r'([a-zA-Zá-úÁ-Ú]+)\s*(\d+)', item)
        if match:
            parsed_data.append({'emocao_principal': match.group(1).capitalize(), 'intensidade': int(match.group(2))})
    return pd.DataFrame(parsed_data)

def gerar_grafico_emocoes_tempo():
    query = "SELECT data_registro, emocoes FROM rdp ORDER BY data_registro"
    df = get_data_as_dataframe(query)
    if df.empty: return None
    df['data_registro'] = pd.to_datetime(df['data_registro'])
    df_emocoes = parse_emocoes(df['emocoes'])
    if df_emocoes.empty: return None
    df_merged = pd.concat([df, df_emocoes], axis=1).dropna(subset=['data_registro', 'emocao_principal', 'intensidade'])
    fig, ax = plt.subplots(figsize=(12, 7))
    for emocao, group in df_merged.groupby('emocao_principal'):
        if len(group) > 1:
            ax.plot(group['data_registro'], group['intensidade'], marker='o', linestyle='-', label=emocao)
    ax.set_title('Intensidade das Emoções ao Longo do Tempo', fontsize=16)
    ax.set_ylabel('Intensidade (0-100)')
    ax.set_xlabel('Data')
    ax.legend(title='Emoções')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    return _plot_to_base64(fig)

def identificar_insights_preditivos():
    insights = []
    rdp_query = "SELECT situacao, emocoes FROM rdp"
    df_rdp = get_data_as_dataframe(rdp_query)
    if not df_rdp.empty:
        df_emocoes = parse_emocoes(df_rdp['emocoes'])
        if not df_emocoes.empty:
            df_merged = pd.concat([df_rdp, df_emocoes], axis=1).dropna()
            if not df_merged.empty and 'intensidade' in df_merged.columns and len(df_merged) > 0:
                primeiro_gatilho = df_merged.sort_values(by='intensidade', ascending=False).iloc[0]
                insights.append({'tipo': 'alerta', 'texto': f"Gatilho de Alta Intensidade: A situação \"{str(primeiro_gatilho['situacao'])[:50]}...\" está associada à emoção '{primeiro_gatilho['emocao_principal']}' com intensidade {primeiro_gatilho['intensidade']}."})
    padrao_query = "SELECT dc.nome as distorcao, c.descricao as crenca FROM rdp r JOIN rdp_distorcoes rd ON r.id = rd.id_rdp JOIN distorcoes_cognitivas dc ON rd.id_distorcao = dc.id JOIN crencas c ON r.id_crenca_associada = c.id"
    df_padrao = get_data_as_dataframe(padrao_query)
    if not df_padrao.empty:
        padrao_comum = df_padrao.groupby(['distorcao', 'crenca']).size().reset_index(name='contagem').sort_values(by='contagem', ascending=False)
        if not padrao_comum.empty:
            primeiro_padrao = padrao_comum.iloc[0]
            insights.append({'tipo': 'padrao', 'texto': f"Padrão Cognitivo Recorrente: A distorção '{primeiro_padrao['distorcao']}' aparece frequentemente conectada à crença \"{primeiro_padrao['crenca']}\"."})
    return insights