import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração visual da página
st.set_page_config(page_title="Saúde Mental - Universitários", layout="wide")

st.title("🧠 Dashboard: Saúde Mental e Hábitos de Universitários")
st.markdown("Análise dos fatores associados à depressão, estresse e rotina acadêmica.")

# Função que carrega o arquivo que vocês trataram no Colab
@st.cache_data
def carregar_dados():
    return pd.read_csv("base_tratada.csv")

try:
    df = carregar_dados()

    # --- FILTROS (BARRA LATERAL) ---
    st.sidebar.header("Filtros do Painel")
    genero_selecionado = st.sidebar.multiselect(
        "Selecione o Gênero:",
        options=df["genero"].dropna().unique(),
        default=df["genero"].dropna().unique()
    )

    # Aplica o filtro na tabela
    df_filtrado = df[df["genero"].isin(genero_selecionado)]

    # --- MÉTRICAS RÁPIDAS (KPIs) ---
    st.subheader("Visão Geral da Amostra")
    col1, col2, col3 = st.columns(3)
    col1.metric("Estudantes Analisados", f"{len(df_filtrado):,}")
    col2.metric("Nível Médio de Estresse", f"{df_filtrado['nivel_estresse'].mean():.1f} / 10")
    col3.metric("Qualidade Média do Sono", f"{df_filtrado['qualidade_sono'].mean():.1f} / 10")

    st.divider()

    # --- GRÁFICOS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("1. Sono vs. Depressão")
        fig_sono = px.box(
            df_filtrado, 
            x="indicador_depressao", 
            y="qualidade_sono",
            color="indicador_depressao",
            labels={
                "qualidade_sono": "Qualidade do Sono", 
                "indicador_depressao": "Sintomas Depressivos"
            }
        )
        st.plotly_chart(fig_sono, use_container_width=True)

    with c2:
        st.subheader("2. Estresse Médio por Gênero")
        df_estresse = df_filtrado.groupby("genero")["nivel_estresse"].mean().reset_index()
        fig_estresse = px.bar(
            df_estresse, 
            x="genero", 
            y="nivel_estresse",
            color="genero",
            text_auto=".1f", # Mostra a nota exata em cima de cada barra
            labels={
                "genero": "Gênero", 
                "nivel_estresse": "Estresse Médio (0-10)"
            }
        )
        st.plotly_chart(fig_estresse, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ ERRO: O arquivo 'base_tratada.csv' não está na mesma pasta que este script. Coloque os dois juntos e rode novamente.")