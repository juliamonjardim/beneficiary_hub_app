import streamlit as st
import sqlite3
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Gestão de Beneficiários",
    page_icon=None,
    layout="wide"
)

# CSS para esconder menu, rodapé e logo
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Título principal
st.title("Gestão de Beneficiários")

# Conexão com o banco
conn = sqlite3.connect("gestao_beneficiarios.db")

# Carregar tabelas
df_familias = pd.read_sql_query("SELECT * FROM familias;", conn)
df_membros = pd.read_sql_query("SELECT * FROM membros_familia;", conn)
df_beneficiarios = pd.read_sql_query("SELECT * FROM beneficiarios;", conn)
df_projetos = pd.read_sql_query("SELECT * FROM projetos;", conn)

conn.close()

# KPIs (contadores)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Famílias cadastradas", len(df_familias))
col2.metric("Membros cadastrados", len(df_membros))
col3.metric("Beneficiários ativos", len(df_beneficiarios[df_beneficiarios['situacao']=='Ativo']))
col4.metric("Projetos", len(df_projetos))

# Exibir tabelas
st.subheader("📋 Famílias")
st.dataframe(df_familias)

st.subheader("👨‍👩‍👧 Membros da Família")
st.dataframe(df_membros)

st.subheader("👤 Beneficiários")
st.dataframe(df_beneficiarios)

st.subheader("🎯 Projetos")
st.dataframe(df_projetos)

# Gráficos simples
st.subheader("📊 Distribuição de Beneficiários por Projeto")
st.bar_chart(df_beneficiarios['projeto'].value_counts())

st.subheader("📊 Situação dos Beneficiários")
st.bar_chart(df_beneficiarios['situacao'].value_counts())
