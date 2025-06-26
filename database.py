# database.py (Versão Completa e Corrigida)

import sqlite3
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Carrega as variáveis de ambiente
load_dotenv()

DATABASE_NAME = "terapia.db"

# Carrega a chave de criptografia do .env
ENCRYPTION_KEY = os.getenv("DATA_ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("A chave de criptografia DATA_ENCRYPTION_KEY não foi definida no arquivo .env!")
fernet = Fernet(ENCRYPTION_KEY.encode())

# --- Funções de Criptografia ---
def encrypt(data):
    """Criptografa um dado (string)."""
    if data is None:
        return None
    return fernet.encrypt(str(data).encode()).decode()

def decrypt(encrypted_data):
    """Descriptografa um dado."""
    if encrypted_data is None:
        return None
    try:
        return fernet.decrypt(encrypted_data.encode()).decode()
    except Exception:
        return encrypted_data

# --- Conexão e Funções do Banco ---

def get_db_connection():
    """Cria e retorna uma conexão com um banco de dados SQLite PADRÃO."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso.")

# --- Funções CRUD Completas ---

def add_rdp(situacao, pensamentos, emocoes, comportamento, crenca_id, distorcoes_ids):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO rdp (situacao, pensamentos_automaticos, emocoes, comportamento, id_crenca_associada) VALUES (?, ?, ?, ?, ?)',
        (encrypt(situacao), encrypt(pensamentos), encrypt(emocoes), encrypt(comportamento), crenca_id if crenca_id and crenca_id != 0 else None)
    )
    rdp_id = cursor.lastrowid
    if distorcoes_ids:
        for distorcao_id in distorcoes_ids:
            cursor.execute('INSERT INTO rdp_distorcoes (id_rdp, id_distorcao) VALUES (?, ?)', (rdp_id, distorcao_id))
    conn.commit()
    conn.close()

def get_all_rdps():
    conn = get_db_connection()
    rdps_encrypted = conn.execute('SELECT * FROM rdp ORDER BY data_registro DESC').fetchall()
    conn.close()
    rdps_decrypted = []
    for rdp in rdps_encrypted:
        rdp_dict = dict(rdp)
        rdp_dict['situacao'] = decrypt(rdp_dict['situacao'])
        rdp_dict['pensamentos_automaticos'] = decrypt(rdp_dict['pensamentos_automaticos'])
        rdps_decrypted.append(rdp_dict)
    return rdps_decrypted

def get_rdp_by_id(rdp_id):
    conn = get_db_connection()
    rdp_encrypted = conn.execute('SELECT rdp.*, c.descricao as crenca_descricao FROM rdp LEFT JOIN crencas c ON rdp.id_crenca_associada = c.id WHERE rdp.id = ?', (rdp_id,)).fetchone()
    if not rdp_encrypted:
        conn.close()
        return None
    distorcoes = conn.execute('SELECT dc.nome FROM rdp_distorcoes rd JOIN distorcoes_cognitivas dc ON rd.id_distorcao = dc.id WHERE rd.id_rdp = ?', (rdp_id,)).fetchall()
    questionamentos_encrypted = conn.execute('SELECT * FROM questionamento_socratico WHERE id_rdp = ? ORDER BY id', (rdp_id,)).fetchall()
    conn.close()
    rdp_dict = dict(rdp_encrypted)
    rdp_dict['situacao'] = decrypt(rdp_dict['situacao'])
    rdp_dict['pensamentos_automaticos'] = decrypt(rdp_dict['pensamentos_automaticos'])
    rdp_dict['emocoes'] = decrypt(rdp_dict['emocoes'])
    rdp_dict['comportamento'] = decrypt(rdp_dict['comportamento'])
    rdp_dict['crenca_descricao'] = decrypt(rdp_dict['crenca_descricao'])
    rdp_dict['distorcoes'] = [d['nome'] for d in distorcoes]
    rdp_dict['questionamentos'] = [
        {**q, 'resposta': decrypt(q['resposta']), 'pensamento_alternativo': decrypt(q['pensamento_alternativo'])}
        for q in questionamentos_encrypted
    ]
    return rdp_dict

def get_all_distorcoes():
    conn = get_db_connection()
    distorcoes = conn.execute('SELECT * FROM distorcoes_cognitivas ORDER BY nome').fetchall()
    conn.close()
    return distorcoes

def get_all_crencas(): # <--- A FUNÇÃO QUE ESTAVA FALTANDO
    conn = get_db_connection()
    crencas_encrypted = conn.execute('SELECT * FROM crencas ORDER BY tipo, descricao').fetchall()
    conn.close()
    crencas_decrypted = []
    for crenca in crencas_encrypted:
        crenca_dict = dict(crenca)
        crenca_dict['descricao'] = decrypt(crenca_dict['descricao'])
        crencas_decrypted.append(crenca_dict)
    return crencas_decrypted

def add_crenca(descricao, tipo, categoria_triade, nivel_conviccao):
    conn = get_db_connection()
    conn.execute('INSERT INTO crencas (descricao, tipo, categoria_triade, nivel_conviccao) VALUES (?, ?, ?, ?)',
                 (encrypt(descricao), tipo, categoria_triade, nivel_conviccao))
    conn.commit()
    conn.close()

def get_all_gratidao_entries():
    conn = get_db_connection()
    entries_encrypted = conn.execute('SELECT * FROM diario_gratidao ORDER BY data_registro DESC').fetchall()
    conn.close()
    entries_decrypted = [ {**entry, 'entrada': decrypt(entry['entrada'])} for entry in entries_encrypted]
    return entries_decrypted

def add_gratidao_entry(entrada):
    conn = get_db_connection()
    conn.execute('INSERT INTO diario_gratidao (entrada) VALUES (?)', (encrypt(entrada),))
    conn.commit()
    conn.close()

def add_questionamento(rdp_id, pergunta, resposta, pensamento_alternativo, dissonancia):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO questionamento_socratico (id_rdp, pergunta, resposta, pensamento_alternativo, nivel_dissonia_cognitiva) VALUES (?, ?, ?, ?, ?)',
        (rdp_id, pergunta, encrypt(resposta), encrypt(pensamento_alternativo), dissonancia)
    )
    conn.commit()
    conn.close()

def get_data_for_ml_training():
    conn = get_db_connection()
    query = "SELECT r.id, r.pensamentos_automaticos, GROUP_CONCAT(dc.nome, '|') as distorcoes FROM rdp r JOIN rdp_distorcoes rd ON r.id = rd.id_rdp JOIN distorcoes_cognitivas dc ON rd.id_distorcao = dc.id GROUP BY r.id, r.pensamentos_automaticos HAVING distorcoes IS NOT NULL;"
    rows = conn.execute(query).fetchall()
    conn.close()
    training_data = [(decrypt(row['pensamentos_automaticos']), row['distorcoes'].split('|')) for row in rows]
    return training_data