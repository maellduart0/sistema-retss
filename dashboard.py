
import streamlit as st
import pandas as pd
from fila_prioridade import processar_fila
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Sistema RETTS",
    page_icon="🏥",
    layout="wide"
)

# Carregar os dados
@st.cache_data
def carregar_dados():
    caminho = Path(__file__).parent / "pacientes_triagem.csv"
    dados = pd.read_csv(caminho, encoding="utf-8-sig")
    dados["Prioridade_RETTS"] = pd.to_numeric(
        dados["Prioridade_RETTS"]
    )
    return dados

df = processar_fila(carregar_dados())
st.write("Classes encontradas:", df["Classe_RETTS"].unique())

# Organizar pacientes por prioridade e horário

# Título
st.title("🏥 Sistema de Triagem e Visualização Hospitalar")
st.subheader("Painel de acompanhamento de pacientes - RETTS")

st.divider()

# Indicadores
col1, col2, col3 = st.columns(3)

col1.metric("Total de pacientes", len(df))
col2.metric("Prioridade máxima (1)", len(df[df["Prioridade_RETTS"] == 1]))
col3.metric("Prioridade mínima (5)", len(df[df["Prioridade_RETTS"] == 5]))

st.divider()

# Filtro de prioridade
st.subheader("🔎 Filtrar pacientes")

prioridades = sorted(df["Prioridade_RETTS"].unique())

filtro = st.multiselect(
    "Selecione as prioridades:",
    prioridades,
    default=prioridades
)

dados_filtrados = df[
    df["Prioridade_RETTS"].isin(filtro)
]

# Cores de cada classe RETTS
cores = {
    "vermelho": "#ff4b4b",
    "laranja": "#ff9f43",
    "amarelo": "#ffe066",
    "verde": "#51cf66",
    "azul": "#339af0"
}

def colorir_linha(linha):
    classe = str(linha["Classe_RETTS"]).strip().lower()
    cor = cores.get(classe, "#ffffff")
    return [f"background-color: {cor}; color: black"] * len(linha)

# Tabela de pacientes
st.subheader("📋 Fila de atendimento")

tabela = dados_filtrados.style.apply(
    colorir_linha,
    axis=1
)

st.dataframe(
    tabela,
    width="stretch",
    hide_index=True
)

st.divider()

# Gráfico de distribuição
st.subheader("📊 Distribuição de pacientes por prioridade")

distribuicao = (
    df.groupby("Classe_RETTS")
    .size()
    .reindex(["Vermelho", "Laranja", "Amarelo", "Verde", "Azul"])
    .dropna()
)

import altair as alt

dados_grafico = distribuicao.rename_axis(
    "Classe_RETTS"
).reset_index(name="Quantidade")

grafico = alt.Chart(dados_grafico).mark_bar().encode(
    x=alt.X(
        "Classe_RETTS:N",
        sort=["Vermelho", "Laranja", "Amarelo", "Verde", "Azul"],
        title="Classificação RETTS"
    ),
    y=alt.Y("Quantidade:Q", title="Número de pacientes"),
    color=alt.Color(
        "Classe_RETTS:N",
        scale=alt.Scale(
            domain=["Vermelho", "Laranja", "Amarelo", "Verde", "Azul"],
            range=["#ff4b4b", "#ff9f43", "#ffe066", "#51cf66", "#339af0"]
        ),
        legend=None
    )
)

st.altair_chart(grafico, width="stretch")

st.caption(
    "O sistema organiza os pacientes considerando a prioridade RETTS "
    "e o horário de chegada."
)
