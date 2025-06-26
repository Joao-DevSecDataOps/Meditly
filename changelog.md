# Changelog - Diário TCC

Este documento registra todas as principais etapas e marcos no desenvolvimento da aplicação Diário TCC.

## Versão 1.0.0 (26-06-2025)

### ✨ Features (Funcionalidades)

- **Conteinerização e Preparação para Deploy:**
    - Adicionado `Dockerfile` para conteinerizar a aplicação.
    - Adicionado `gunicorn` como servidor de produção WSGI.
    - Adicionado arquivo `.dockerignore` para otimizar a imagem.
    - Instruções de Git e GitHub adicionadas ao `README.md`.

- **Inteligência Artificial (Machine Learning):**
    - Criado `model.py` para treinar um modelo de classificação de texto com `scikit-learn`.
    - Modelo prevê distorções cognitivas com base no texto do pensamento.
    - Adicionada rota de API (`/rdp/prever_distorcoes`) para inferência em tempo real.
    - Integrado botão "Sugerir (IA) ✨" no formulário de Novo RDP com JavaScript para interação.
    - Modelo e binarizador salvos em `cbt_distortion_model.joblib`.

- **Análise e Visualização de Dados:**
    - Criado `analysis.py` para centralizar a lógica de análise.
    - Adicionada página de "Análise" com:
        - Gráfico de barras de frequência de distorções.
        - Nuvem de palavras para pensamentos e situações.
        - Gráfico de linha de evolução da intensidade emocional.
        - Geração de "insights preditivos simples" baseados em padrões.
    - Adicionadas dependências `pandas`, `matplotlib`, `wordcloud`.

- **Segurança Robusta (Defesa em Profundidade):**
    - **Criptografia de Dados:**
        - Abandonada a abordagem de criptografia de arquivo (`sqlcipher3-binary`) devido a problemas de compatibilidade.
        - Implementada criptografia em nível de aplicação com a biblioteca `cryptography`.
        - Todos os dados sensíveis (pensamentos, situações, etc.) são criptografados antes de serem salvos no banco.
        - Chave de criptografia gerenciada via variável de ambiente `DATA_ENCRYPTION_KEY`.
    - **Autenticação de Usuário:**
        - Adicionada tela de login.
        - Integrado `Flask-Login` para gerenciamento de sessão.
        - Senhas de usuário são hasheadas com `werkzeug.security`.
    - **Proteção Web:**
        - Integrado `Flask-WTF` para todos os formulários, garantindo proteção contra ataques CSRF.
        - Gerenciamento de segredos (`SECRET_KEY`) via arquivo `.env`.

- **Estrutura Fundamental da Aplicação:**
    - Estruturado o projeto com `app.py`, `database.py` e `schema.sql`.
    - Implementadas as funcionalidades CRUD para:
        - Registro de Pensamentos Disfuncionais (RDP).
        - Crenças Centrais e Pressupostos Adjacentes.
        - Diário de Gratidão.
        - Questionamento Socrático detalhado por RDP.
    - Criados templates HTML com Jinja2 e estilizados com Tailwind CSS.

### 🐛 Bug Fixes & Refatoração

- **Resolução de Erros de Importação:**
    - Corrigido `ImportError` para `RangeField`, substituindo-o por `IntegerField` com `render_kw={"type": "range"}` para garantir compatibilidade.
    - Corrigido `AttributeError` para `get_all_crencas` ao completar o arquivo `database.py` com todas as funções necessárias.
- **Resolução de Erros de Ambiente:**
    - Solucionado erro `TemplateNotFound: login.html` ajustando a estrutura de pastas para incluir todos os templates dentro da pasta `/templates`.
    - Guias fornecidos para corrigir o erro `"'git' não é reconhecido..."` através da instalação correta do Git no Windows.
    - Resolvido problema de compatibilidade do `sqlcipher3-binary` ao pivotar para a biblioteca `cryptography`.
- **Refatoração de Formulários:**
    - Todos os formulários HTML foram migrados para classes `FlaskForm` no arquivo `forms.py` para centralizar a lógica e aumentar a segurança.

### 📄 Documentação

- Criado `README.md` com instruções detalhadas de instalação e execução.
- Criado `ARQUITETURA.md` descrevendo a engenharia atual do projeto.
- Criado este `CHANGELOG.md` para rastrear o histórico de desenvolvimento.