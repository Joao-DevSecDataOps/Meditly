# Meu Diário TCC - Versão Segura e Inteligente

Esta é uma aplicação web local, desenvolvida em Python com Flask, para auxiliar estudantes e praticantes de Terapia Cognitivo-Comportamental (TCC) a aplicar e registrar seus aprendizados.

### Funcionalidades Principais
- **Segurança Robusta:** Autenticação de usuário, criptografia em nível de aplicação para todos os dados sensíveis e proteção contra ataques CSRF.
- **Registro TCC Completo:** Funcionalidades para Registro de Pensamentos Disfuncionais (RDP), Crenças Centrais, Distorções Cognitivas, Questionamento Socrático e Diário de Gratidão.
- **Análise Visual de Dados:** Gráficos e nuvens de palavras para explorar padrões e insights em seus registros.
- **Inteligência Artificial:** Sistema de Machine Learning que sugere distorções cognitivas automaticamente com base no texto dos pensamentos.
- **Pronto para Deploy:** A aplicação está conteinerizada com Docker para portabilidade e um deploy simplificado.

---

## Guia de Instalação e Execução

Siga estes passos **exatamente** na ordem apresentada.

### Pré-requisitos
- Python 3.8+
- Git
- Docker Desktop

### 1. Configuração do Ambiente Local
```bash
# Clone o repositório (se estiver no GitHub) ou extraia os arquivos.
# Navegue até a pasta raiz do projeto:
cd cbt-jounal

# Crie e ative um ambiente virtual:
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# Instale todas as dependências:
pip install -r requirements.txt