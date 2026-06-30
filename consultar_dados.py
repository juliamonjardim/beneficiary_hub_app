import sqlite3

conn = sqlite3.connect("gestao_beneficiarios.db")
cursor = conn.cursor()

print("\n=== Famílias ===")
for row in cursor.execute("SELECT * FROM familias;"):
    print(f"ID: {row[0]} | Nome: {row[1]} | Responsável: {row[2]} | Telefone: {row[3]} | Endereço: {row[4]} | Situação: {row[5]}")

print("\n=== Membros da Família ===")
for row in cursor.execute("SELECT * FROM membros_familia;"):
    print(f"ID: {row[0]} | Família ID: {row[1]} | Nome: {row[2]} | Idade: {row[3]} | Projetos: {row[4]}")

print("\n=== Beneficiários ===")
for row in cursor.execute("SELECT * FROM beneficiarios;"):
    print(f"ID: {row[0]} | Nome: {row[1]} | Nascimento: {row[2]} | Idade: {row[3]} | Família ID: {row[4]} | Projeto: {row[5]} | Situação: {row[7]}")

print("\n=== Projetos ===")
for row in cursor.execute("SELECT * FROM projetos;"):
    print(f"ID: {row[0]} | Nome: {row[1]} | Coordenador: {row[2]} | Inscritos: {row[3]}")

conn.close()
