from werkzeug.security import generate_password_hash
import sqlite3
import getpass
import os

DATABASE_NAME = "terapia.db"

if not os.path.exists(DATABASE_NAME):
    print(f"Banco de dados '{DATABASE_NAME}' não encontrado.")
    print("Por favor, rode o comando para inicializar o banco de dados primeiro:")
    print("python -c \"import database; database.init_db()\"")
    exit()

print("--- Criação de Usuário ---")
username = input("Digite o nome de usuário: ")
password = getpass.getpass("Digite a senha: ")
password_confirm = getpass.getpass("Confirme a senha: ")

if password != password_confirm:
    print("As senhas não coincidem. Abortando.")
    exit()

password_hash = generate_password_hash(password)

try:
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute('INSERT INTO usuarios (username, password_hash) VALUES (?, ?)', (username, password_hash))
    conn.commit()
    conn.close()
    print(f"\nUsuário '{username}' criado com sucesso!")
    print("Agora você pode criptografar o banco de dados.")
except Exception as e:
    print(f"Erro ao criar usuário: {e}")