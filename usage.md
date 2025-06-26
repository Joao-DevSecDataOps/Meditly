# Guia de Execução e Manutenção: Diário TCC

Este arquivo centraliza os comandos essenciais para configurar, executar e manter a aplicação.

---

## 1. Configuração Inicial (Executar Apenas Uma Vez)

### a. Configuração de Segredos (`.env`)

1.  **Copie o arquivo de exemplo** para criar seu arquivo de ambiente local.
    ```bash
    # No Windows (Command Prompt):
    copy .env.example .env
    # No macOS/Linux:
    cp .env.example .env
    ```

2.  **Gere uma chave de criptografia** executando o seguinte comando no terminal:
    ```bash
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    ```

3.  **Edite o arquivo `.env`:**
    * Abra o `.env` em um editor de texto.
    * Cole a chave gerada no passo anterior como o valor de `DATA_ENCRYPTION_KEY`.
    * Altere o valor de `SECRET_KEY` para outra sequência longa e aleatória de sua escolha.

### b. Configuração do Banco de Dados e Usuário

1.  **Crie a estrutura do banco de dados:**
    ```bash
    python -c "import database; database.init_db()"
    ```

2.  **Crie sua conta de usuário principal:**
    ```bash
    python create_user.py
    ```
    * Siga as instruções no terminal para definir seu nome de usuário e senha.

---

## 2. Executando a Aplicação (Uso Diário)

Escolha uma das opções abaixo para iniciar o servidor.

### Opção A: Localmente (para Desenvolvimento)

Este método é ideal para testar mudanças rápidas no código.

```bash
# Certifique-se de que seu ambiente virtual esteja ativo
# .\venv\Scripts\activate (Windows) ou source venv/bin/activate (macOS/Linux)

flask run
```
A aplicação estará disponível em `http://127.0.0.1:5000`.

### Opção B: Via Docker (Recomendado para Simular Produção)

Este método executa a aplicação dentro de um contêiner isolado, como seria em um servidor de produção.

1.  **Construa a imagem Docker (se ainda não o fez ou se mudou o código):**
    ```bash
    docker build -t diario-tcc-app .
    ```

2.  **Rode o contêiner:**
    ```bash
    docker run -p 5000:5000 --env-file .env diario-tcc-app
    ```
A aplicação estará disponível em `http://127.0.0.1:5000`.

---

## 3. Manutenção e Treinamento de IA (Uso Periódico)

O modelo de Inteligência Artificial aprende com seus registros. Para que ele melhore e aprenda com os novos dados que você insere, você precisa treiná-lo novamente de tempos em tempos.

**Quando treinar?**
-   Recomendado após adicionar 15-20 novos RDPs com distorções associadas.

**Como treinar:**
1.  **Pare a aplicação** (pressione `Ctrl+C` no terminal onde ela está rodando).
2.  **Execute o script de treinamento:**
    ```bash
    python model.py
    ```
3.  **Reinicie a aplicação** usando a Opção A ou B acima para que ela carregue o novo modelo treinado.