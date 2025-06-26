CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS problemas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    resolvido BOOLEAN DEFAULT 0
);
CREATE TABLE IF NOT EXISTS distorcoes_cognitivas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL,
    descricao TEXT
);
CREATE TABLE IF NOT EXISTS crencas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    tipo TEXT CHECK(tipo IN ('Central', 'Pressuposto Adjacente')) NOT NULL,
    categoria_triade TEXT CHECK(categoria_triade IN ('EU', 'PESSOAS', 'MUNDO/FUTURO')),
    nivel_conviccao INTEGER DEFAULT 70
);
CREATE TABLE IF NOT EXISTS rdp (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    situacao TEXT NOT NULL,
    pensamentos_automaticos TEXT NOT NULL,
    emocoes TEXT NOT NULL,
    comportamento TEXT NOT NULL,
    id_crenca_associada INTEGER,
    FOREIGN KEY (id_crenca_associada) REFERENCES crencas(id)
);
CREATE TABLE IF NOT EXISTS rdp_distorcoes (
    id_rdp INTEGER,
    id_distorcao INTEGER,
    PRIMARY KEY (id_rdp, id_distorcao),
    FOREIGN KEY (id_rdp) REFERENCES rdp(id),
    FOREIGN KEY (id_distorcao) REFERENCES distorcoes_cognitivas(id)
);
CREATE TABLE IF NOT EXISTS questionamento_socratico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_rdp INTEGER NOT NULL,
    pergunta TEXT NOT NULL,
    resposta TEXT,
    pensamento_alternativo TEXT,
    nivel_dissonia_cognitiva INTEGER,
    FOREIGN KEY (id_rdp) REFERENCES rdp(id)
);
CREATE TABLE IF NOT EXISTS diario_gratidao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    entrada TEXT NOT NULL
);
INSERT OR IGNORE INTO distorcoes_cognitivas (nome, descricao) VALUES
    ('Pensamento Tudo-ou-Nada', 'Ver as coisas em categorias absolutas, preto e branco.'),
    ('Supergeneralização', 'Ver um único evento negativo como um padrão de derrota sem fim.'),
    ('Filtro Mental', 'Focar exclusivamente nos detalhes negativos e ignorar os positivos.'),
    ('Desqualificar o Positivo', 'Insistir que as realizações positivas "não contam".'),
    ('Leitura Mental', 'Concluir que alguém está reagindo negativamente a você sem evidências.'),
    ('Erro do Adivinho', 'Prever que as coisas darão errado.'),
    ('Maximização e Minimização', 'Exagerar a importância de seus problemas e minimizar suas qualidades.'),
    ('Raciocínio Emocional', 'Assumir que suas emoções negativas refletem a realidade.'),
    ('Declarações "Deveria"', 'Criticar a si mesmo ou aos outros com "Eu deveria...", "Eu não deveria...".'),
    ('Rotulação', 'Identificar-se com seus erros em vez de vê-los como eventos.'),
    ('Personalização', 'Assumir a responsabilidade por um evento negativo quando não há base para isso.');