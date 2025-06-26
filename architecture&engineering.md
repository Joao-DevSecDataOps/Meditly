# Documento de Arquitetura e Engenharia: Diário TCC

**Versão:** 1.0 (Local e Segura)

## 1. Visão Geral

Este documento detalha a arquitetura da aplicação "Diário TCC" em seu estado atual. O projeto foi concebido como uma aplicação web local, segura e de usuário único, com foco em robustez, confidencialidade e extensibilidade.

## 2. Arquitetura da Aplicação (Monólito Modular)

A aplicação segue um padrão de arquitetura **Monólito Modular**, onde todos os componentes rodam em um único processo, mas o código é organizado em módulos com responsabilidades distintas.

- **Frontend:** A interface do usuário é renderizada no lado do servidor (`Server-Side Rendering`) utilizando o motor de templates **Jinja2**, integrado ao Flask. O estilo é gerenciado pela framework de CSS utilitária **Tailwind CSS**, consumida via CDN para simplicidade.
- **Backend:** O núcleo da aplicação é construído com **Flask**, um micro-framework Python. Ele gerencia as rotas, a lógica de negócios e a interação com o banco de dados.
- **Servidor WSGI:** Para execução em produção (via Docker), o servidor de desenvolvimento do Flask é substituído pelo **Gunicorn**, um servidor WSGI robusto e eficiente.

### Estrutura de Módulos
- `app.py`: Ponto de entrada da aplicação. Controla as rotas, autenticação e renderização de templates.
- `database.py`: Módulo de acesso a dados. Centraliza toda a comunicação com o banco de dados, abstraindo as queries SQL do resto da aplicação.
- `forms.py`: Define todos os formulários da aplicação usando `Flask-WTF`, centralizando a validação e a proteção contra CSRF.
- `analysis.py`: Módulo de análise de dados. Usa `pandas` e `matplotlib` para gerar gráficos e insights.
- `model.py`: Módulo de Machine Learning. Contém a lógica para treinar e salvar o modelo de classificação de texto com `scikit-learn`.

## 3. Arquitetura de Dados

- **Banco de Dados:** **SQLite**, um banco de dados relacional leve e baseado em arquivo, ideal para uma aplicação local.
- **Persistência:** O banco de dados é persistido no arquivo `terapia.db`.
- **Schema:** O schema (`schema.sql`) é relacional, conectando RDPs a crenças, distorções e outras entidades, permitindo consultas complexas e a integridade dos dados.

## 4. Arquitetura de Segurança (Defesa em Profundidade)

A segurança é o pilar central da arquitetura, implementada em múltiplas camadas:

1.  **Controle de Acesso (Autenticação):**
    - Acesso à aplicação é protegido por uma tela de login.
    - Utiliza a biblioteca **Flask-Login** para gerenciar sessões de usuário.
    - As senhas não são armazenadas em texto plano; apenas seus hashes seguros (gerados com `Werkzeug.security`) são persistidos no banco.

2.  **Criptografia de Dados em Repouso (Application-Level Encryption):**
    - Para evitar problemas de compatibilidade com criptografia de banco de dados em nível de arquivo, foi adotada a criptografia em nível de aplicação.
    - Todos os dados textuais sensíveis (pensamentos, situações, descrições, etc.) são criptografados com o algoritmo **AES** através da biblioteca `cryptography` (Fernet).
    - A criptografia e descriptografia são realizadas de forma transparente dentro do módulo `database.py`.
    - A chave de criptografia (`DATA_ENCRYPTION_KEY`) é gerenciada como um segredo no arquivo `.env` e nunca é versionada no Git.

3.  **Segurança da Aplicação Web:**
    - **Proteção CSRF (Cross-Site Request Forgery):** Implementada em todos os formulários através da integração com `Flask-WTF`, que gera e valida tokens CSRF automaticamente.
    - **Gerenciamento de Segredos:** Todas as chaves e senhas são carregadas a partir de um arquivo `.env` usando `python-dotenv`, mantendo os segredos fora do código-fonte.

## 5. Arquitetura de Machine Learning (ML)

- **Tipo de Modelo:** Classificação de Texto Multirrótulo.
- **Objetivo:** Prever as distorções cognitivas associadas a um "pensamento automático".
- **Pipeline de ML:**
    1.  **Vetorização:** O texto é transformado em vetores numéricos usando `TfidfVectorizer`.
    2.  **Classificador:** Um modelo de Regressão Logística é treinado para cada rótulo (distorção) usando a estratégia `OneVsRestClassifier`.
    - **Persistência do Modelo:** O pipeline treinado e o binarizador de rótulos são salvos em um único arquivo (`cbt_distortion_model.joblib`) usando `joblib`.
- **Ciclo de Vida (Manual):** O modelo é treinado manualmente pelo usuário através do script `model.py`. O `app.py` carrega o modelo salvo durante a inicialização para realizar inferências em tempo real.

## 6. Conteinerização

- **Tecnologia:** **Docker**.
- **Dockerfile:** Define uma imagem de produção baseada em `python:3.11-slim`, instala as dependências e configura o Gunicorn como servidor.
- **`.dockerignore`:** Garante que segredos, ambiente virtual e outros artefatos desnecessários não sejam incluídos na imagem, mantendo-a leve e segura.