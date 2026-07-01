import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# Conexão com banco de dados
conn = sqlite3.connect("gestao_beneficiarios.db")
cursor = conn.cursor()

# Criação das tabelas se não existirem
cursor.execute("""
CREATE TABLE IF NOT EXISTS beneficiarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    data_nascimento TEXT,
    idade INTEGER,
    familia TEXT,
    projeto TEXT,
    situacao TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS familias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    telefone TEXT,
    endereco TEXT,
    situacao TEXT,
    data_cadastro TEXT
)
""")
conn.commit()

# Barra lateral de navegação
st.sidebar.title("Beneficiary Hub")
pagina = st.sidebar.radio("Navegar", ["Dashboard", "Beneficiários", "Famílias"])

# ---------------- Dashboard ----------------
if pagina == "Dashboard":
    st.title("📊 Visão Geral")

    total_familias = cursor.execute("SELECT COUNT(*) FROM familias").fetchone()[0]
    total_beneficiarios = cursor.execute("SELECT COUNT(*) FROM beneficiarios").fetchone()[0]
    projetos = ["Educação", "Esporte", "Cultura", "Música", "Assistência Social", "Informática", "Artesanato"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Famílias cadastradas", total_familias)
    col2.metric("Beneficiários", total_beneficiarios)
    col3.metric("Projetos ativos", len(projetos))
    col4.metric("Coordenadores", 12)

    # Beneficiários por projeto (exemplo fixo)
    df_proj = pd.DataFrame({
        "Projeto": projetos,
        "Beneficiários": [278, 215, 198, 122, 157, 98, 75]
    })
    st.bar_chart(df_proj.set_index("Projeto"))

    # Distribuição por idade (exemplo fixo)
    df_idade = pd.DataFrame({
        "Faixa Etária": ["0-6", "7-12", "13-17", "18-59", "60+"],
        "Percentual": [18, 28, 19, 25, 10]
    })
    st.write("### Distribuição por Idade")
    st.dataframe(df_idade)

# ---------------- Beneficiários ----------------
elif pagina == "Beneficiários":
    st.title("🧾 Cadastro de Beneficiários")

    with st.form("form_beneficiario"):
        nome = st.text_input("Nome completo")
        data_nasc = st.date_input("Data de nascimento", date.today())
        idade = date.today().year - data_nasc.year
        familia = st.text_input("Família")
        projeto = st.selectbox("Projeto", ["Educação", "Esporte", "Cultura", "Música", "Assistência Social", "Informática", "Artesanato"])
        situacao = st.selectbox("Situação", ["Ativo", "Inativo"])
        salvar = st.form_submit_button("Salvar")

        if salvar:
            cursor.execute("""
                INSERT INTO beneficiarios (nome, data_nascimento, idade, familia, projeto, situacao)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nome, str(data_nasc), idade, familia, projeto, situacao))
            conn.commit()
            st.success("✅ Beneficiário cadastrado com sucesso!")

    st.write("### Lista de Beneficiários")
    df_ben = pd.read_sql_query("SELECT nome, idade, projeto, situacao FROM beneficiarios", conn)
    st.dataframe(df_ben)

# ---------------- Famílias ----------------
elif pagina == "Famílias":
    st.title("🏠 Gestão de Famílias")

    with st.form("form_familia"):
        nome_fam = st.text_input("Nome da família")
        telefone = st.text_input("Telefone")
        endereco = st.text_input("Endereço")
        situacao = st.selectbox("Situação", ["Ativa", "Inativa"])
        data_cad = date.today().strftime("%d/%m/%Y")
        salvar = st.form_submit_button("Cadastrar Família")

        if salvar:
            cursor.execute("""
                INSERT INTO familias (nome, telefone, endereco, situacao, data_cadastro)
                VALUES (?, ?, ?, ?, ?)
            """, (nome_fam, telefone, endereco, situacao, data_cad))
            conn.commit()
            st.success("✅ Família cadastrada com sucesso!")

    st.write("### Famílias Registradas")
    df_fam = pd.read_sql_query("SELECT nome, telefone, endereco, situacao, data_cadastro FROM familias", conn)
    st.dataframe(df_fam)
