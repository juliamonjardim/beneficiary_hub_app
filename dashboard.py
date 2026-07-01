import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# Database setup
conn = sqlite3.connect("gestao_beneficiarios.db")
cursor = conn.cursor()

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

# Sidebar navigation
st.sidebar.title("Beneficiary Hub")
page = st.sidebar.radio("Navigate", ["Dashboard", "Beneficiaries", "Families"])

# Dashboard
if page == "Dashboard":
    st.title("📊 Dashboard Overview")

    # Example metrics
    total_familias = cursor.execute("SELECT COUNT(*) FROM familias").fetchone()[0]
    total_beneficiarios = cursor.execute("SELECT COUNT(*) FROM beneficiarios").fetchone()[0]
    projetos = ["Education", "Sports", "Culture", "Music", "Social Assistance", "IT", "Crafts"]
    st.metric("Families Registered", total_familias)
    st.metric("Total Beneficiaries", total_beneficiarios)
    st.metric("Active Projects", len(projetos))
    st.metric("Coordinators", 12)

    # Beneficiaries per project
    df_proj = pd.DataFrame({
        "Project": projetos,
        "Beneficiaries": [278, 215, 198, 122, 157, 98, 75]
    })
    st.bar_chart(df_proj.set_index("Project"))

    # Age distribution
    df_age = pd.DataFrame({
        "Age Range": ["0-6", "7-12", "13-17", "18-59", "60+"],
        "Percentage": [18, 28, 19, 25, 10]
    })
    st.write("### Age Distribution of Beneficiaries")
    st.dataframe(df_age)

# Beneficiary registration
elif page == "Beneficiaries":
    st.title("🧾 Beneficiary Registration")

    with st.form("beneficiary_form"):
        nome = st.text_input("Full Name")
        data_nasc = st.date_input("Birth Date", date.today())
        idade = date.today().year - data_nasc.year
        familia = st.text_input("Family Name")
        projeto = st.selectbox("Project", ["Education", "Sports", "Culture", "Music", "Social Assistance", "IT", "Crafts"])
        situacao = st.selectbox("Status", ["Active", "Inactive"])
        submitted = st.form_submit_button("Save")

        if submitted:
            cursor.execute("INSERT INTO beneficiarios (nome, data_nascimento, idade, familia, projeto, situacao) VALUES (?, ?, ?, ?, ?, ?)",
                           (nome, str(data_nasc), idade, familia, projeto, situacao))
            conn.commit()
            st.success("Beneficiary saved successfully!")

    st.write("### Beneficiary List")
    df_ben = pd.read_sql_query("SELECT nome, idade, projeto, situacao FROM beneficiarios", conn)
    st.dataframe(df_ben)

# Family management
elif page == "Families":
    st.title("🏠 Family Management")

    with st.form("family_form"):
        nome_fam = st.text_input("Family Name")
        telefone = st.text_input("Phone")
        endereco = st.text_input("Address")
        situacao = st.selectbox("Status", ["Active", "Inactive"])
        data_cad = date.today().strftime("%d/%m/%Y")
        submitted = st.form_submit_button("Register Family")

        if submitted:
            cursor.execute("INSERT INTO familias (nome, telefone, endereco, situacao, data_cadastro) VALUES (?, ?, ?, ?, ?)",
                           (nome_fam, telefone, endereco, situacao, data_cad))
            conn.commit()
            st.success("Family registered successfully!")

    st.write("### Registered Families")
    df_fam = pd.read_sql_query("SELECT nome, telefone, endereco, situacao, data_cadastro FROM familias", conn)
    st.dataframe(df_fam)
