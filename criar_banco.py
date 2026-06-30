import sqlite3, os

if os.path.exists("gestao_beneficiarios.db"):
    os.remove("gestao_beneficiarios.db")

conn = sqlite3.connect("gestao_beneficiarios.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE familias (
    id_familia INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_familia TEXT NOT NULL,
    responsavel TEXT,
    telefone TEXT,
    endereco TEXT,
    situacao TEXT CHECK(situacao IN ('Ativa','Inativa')),
    data_criacao DATE DEFAULT CURRENT_DATE,
    num_membros INTEGER DEFAULT 0,
    num_projetos INTEGER DEFAULT 0
);

CREATE TABLE membros_familia (
    id_membro INTEGER PRIMARY KEY AUTOINCREMENT,
    id_familia INTEGER,
    nome TEXT NOT NULL,
    idade INTEGER,
    projetos TEXT,
    FOREIGN KEY (id_familia) REFERENCES familias(id_familia)
);

CREATE TABLE beneficiarios (
    id_beneficiario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo TEXT NOT NULL,
    data_nascimento DATE,
    idade INTEGER,
    familia_id INTEGER,
    projeto TEXT,
    data_entrada DATE DEFAULT CURRENT_DATE,
    situacao TEXT CHECK(situacao IN ('Ativo','Inativo')),
    FOREIGN KEY (familia_id) REFERENCES familias(id_familia)
);

CREATE TABLE projetos (
    id_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_projeto TEXT NOT NULL,
    coordenador TEXT,
    num_inscritos INTEGER DEFAULT 0
);
""")

conn.commit()
conn.close()

print("Banco criado com sucesso!")

conn = sqlite3.connect("gestao_beneficiarios.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tabelas criadas:", cursor.fetchall())

conn.close()

