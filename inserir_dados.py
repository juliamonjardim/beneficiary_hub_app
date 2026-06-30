import sqlite3

# Conecta ao banco existente
conn = sqlite3.connect("gestao_beneficiarios.db")
cursor = conn.cursor()

# Limpa as tabelas antes de inserir (apenas para testes!)
cursor.execute("DELETE FROM familias;")
cursor.execute("DELETE FROM membros_familia;")
cursor.execute("DELETE FROM beneficiarios;")
cursor.execute("DELETE FROM projetos;")

# Inserir famílias
cursor.execute("""
INSERT INTO familias (nome_familia, responsavel, telefone, endereco, situacao)
VALUES ('Familia Silva Santos', 'Paula Silva Santos', '(27) 99999-1234', 'Rua das Flores, 123 - Vitória', 'Ativa');
""")

cursor.execute("""
INSERT INTO familias (nome_familia, responsavel, telefone, endereco, situacao)
VALUES ('Familia Oliveira Lima', 'Carlos Oliveira', '(27) 98888-5678', 'Av. Central, 456 - Vitória', 'Ativa');
""")

# Inserir membros
cursor.execute("""
INSERT INTO membros_familia (id_familia, nome, idade, projetos)
VALUES (1, 'Ana Beatriz Santos', 12, 'Educação, Música');
""")

cursor.execute("""
INSERT INTO membros_familia (id_familia, nome, idade, projetos)
VALUES (1, 'Pedro Henrique Santos', 9, 'Esporte');
""")

# Inserir beneficiários
cursor.execute("""
INSERT INTO beneficiarios (nome_completo, data_nascimento, idade, familia_id, projeto, data_entrada, situacao)
VALUES ('Ana Clara Silva', '2014-05-10', 10, 1, 'Educação', '2023-03-15', 'Ativo');
""")

cursor.execute("""
INSERT INTO beneficiarios (nome_completo, data_nascimento, idade, familia_id, projeto, data_entrada, situacao)
VALUES ('João Pedro Souza', '2016-07-20', 8, 2, 'Esporte', '2023-03-20', 'Ativo');
""")

# Inserir projetos
cursor.execute("""
INSERT INTO projetos (nome_projeto, coordenador, num_inscritos)
VALUES ('Educação', 'Mariana Alves', 278);
""")

cursor.execute("""
INSERT INTO projetos (nome_projeto, coordenador, num_inscritos)
VALUES ('Esporte', 'Carlos Lima', 215);
""")

conn.commit()
conn.close()

print("Dados inseridos com sucesso (sem duplicatas)!")
