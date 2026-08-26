import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração visual da página
st.set_page_config(page_title="Saúde Mental - Universitários", layout="wide")

st.title("🧠 Dashboard: Saúde Mental e Hábitos de Universitários")
st.markdown("Análise dos fatores associados à depressão, estresse e rotina acadêmica.")

# Carrega a base de dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("base_tratada.csv")
    
    # TRADUÇÕES DOS DADOS
    if "Depression" in df.columns:
        df["Depression"] = df["Depression"].replace({True: "Sim", False: "Não", "True": "Sim", "False": "Não"})
    
    if "genero" in df.columns:
        df["genero"] = df["genero"].replace({"Female": "Feminino", "Male": "Masculino", "Other": "Outros"})
        
    return df

try:
    df = carregar_dados()

    # --- FILTROS (BARRA LATERAL) ---
    st.sidebar.header("⚙️ Filtros do Painel")
    
    # 1. Filtro de Gênero (Caixa de múltipla escolha)
    genero_selecionado = st.sidebar.multiselect(
        "Selecione o Gênero:",
        options=df["genero"].dropna().unique(),
        default=df["genero"].dropna().unique()
    )

    # 2. Filtro de Tempo de Sono (Barra deslizante)
    sono_min = float(df["Sleep_Duration"].min())
    sono_max = float(df["Sleep_Duration"].max())
    sono_selecionado = st.sidebar.slider(
        "Faixa de Tempo de Sono (horas):",
        min_value=sono_min,
        max_value=sono_max,
        value=(sono_min, sono_max)
    )

    # 3. Filtro de Horas de Estudo (Barra deslizante)
    estudo_min = float(df["Study_Hours"].min())
    estudo_max = float(df["Study_Hours"].max())
    estudo_selecionado = st.sidebar.slider(
        "Faixa de Horas de Estudo (diárias):",
        min_value=estudo_min,
        max_value=estudo_max,
        value=(estudo_min, estudo_max)
    )

    # Aplica TODOS os filtros na tabela ao mesmo tempo
    df_filtrado = df[
        (df["genero"].isin(genero_selecionado)) &
        (df["Sleep_Duration"] >= sono_selecionado[0]) & 
        (df["Sleep_Duration"] <= sono_selecionado[1]) &
        (df["Study_Hours"] >= estudo_selecionado[0]) & 
        (df["Study_Hours"] <= estudo_selecionado[1])
    ]

    # --- MÉTRICAS RÁPIDAS (KPIs) ---
    st.subheader("Visão Geral da Amostra")
    col1, col2, col3 = st.columns(3)
    col1.metric("Estudantes Analisados", f"{len(df_filtrado):,}")
    
    if not df_filtrado.empty:
        col2.metric("Nível Médio de Estresse", f"{df_filtrado['nivel_estresse'].mean():.1f}")
        col3.metric("Média de Horas de Sono", f"{df_filtrado['Sleep_Duration'].mean():.1f} h")
    else:
        col2.metric("Nível Médio de Estresse", "0")
        col3.metric("Média de Horas de Sono", "0 h")

    st.divider()

    # --- PRIMEIRA LINHA DE GRÁFICOS ---
    if not df_filtrado.empty:
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("1. Sono vs. Depressão")
            fig_sono = px.box(
                df_filtrado, 
                x="Depression", 
                y="Sleep_Duration",
                color="Depression",
                labels={
                    "Sleep_Duration": "Horas de Sono", 
                    "Depression": "Sintomas Depressivos"
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
                text_auto=".1f",
                labels={
                    "genero": "Gênero", 
                    "nivel_estresse": "Estresse Médio"
                }
            )
            st.plotly_chart(fig_estresse, use_container_width=True)

        st.divider()

        # --- SEGUNDA LINHA DE GRÁFICOS ---
        c3, c4 = st.columns(2)

        with c3:
            st.subheader("3. Estudo vs. Desempenho (Notas)")
            fig_estudo = px.scatter(
                df_filtrado,
                x="Study_Hours",
                y="CGPA",
                color="genero",
                labels={
                    "Study_Hours": "Horas de Estudo Diárias", 
                    "CGPA": "Nota (CGPA)",
                    "genero": "Gênero"
                }
            )
            st.plotly_chart(fig_estudo, use_container_width=True)

        with c4:
            st.subheader("4. Redes Sociais vs. Estresse")
            fig_redes = px.scatter(
                df_filtrado,
                x="Social_Media_Hours",
                y="nivel_estresse",
                color="Depression",
                labels={
                    "Social_Media_Hours": "Horas em Redes Sociais", 
                    "nivel_estresse": "Nível de Estresse",
                    "Depression": "Sintomas Depressivos"
                }
            )
            st.plotly_chart(fig_redes, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados. Ajuste os filtros na barra lateral.")

except FileNotFoundError:
    st.error("⚠️ ERRO: O arquivo 'base_tratada.csv' não foi encontrado.")
