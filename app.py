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
    
    if "Depression" in df.columns:
        df["Depression"] = df["Depression"].replace({True: "Sim", False: "Não", "True": "Sim", "False": "Não"})
    
    if "genero" in df.columns:
        df["genero"] = df["genero"].replace({"Female": "Feminino", "Male": "Masculino", "Other": "Outros"})
        
    if "atividade_fisica" in df.columns:
        df["atividade_fisica"] = df["atividade_fisica"].replace({True: "Sim", False: "Não", "True": "Sim", "False": "Não", 1: "Sim", 0: "Não"})
        
    return df

try:
    df = carregar_dados()

    # --- FILTROS (BARRA LATERAL) ---
    st.sidebar.header("⚙️ Filtros do Painel")
    
    genero_selecionado = st.sidebar.multiselect(
        "Selecione o Gênero:",
        options=df["genero"].dropna().unique(),
        default=df["genero"].dropna().unique()
    )

    sono_min = float(df["Sleep_Duration"].min())
    sono_max = float(df["Sleep_Duration"].max())
    sono_selecionado = st.sidebar.slider(
        "Faixa de Tempo de Sono (horas):",
        min_value=sono_min,
        max_value=sono_max,
        value=(sono_min, sono_max)
    )

    estudo_min = float(df["Study_Hours"].min())
    estudo_max = float(df["Study_Hours"].max())
    estudo_selecionado = st.sidebar.slider(
        "Faixa de Horas de Estudo (diárias):",
        min_value=estudo_min,
        max_value=estudo_max,
        value=(estudo_min, estudo_max)
    )

    redes_min = float(df["Social_Media_Hours"].min())
    redes_max = float(df["Social_Media_Hours"].max())
    redes_selecionado = st.sidebar.slider(
        "Faixa de Horas em Redes Sociais:",
        min_value=redes_min,
        max_value=redes_max,
        value=(redes_min, redes_max)
    )

    # Aplica TODOS os filtros na tabela
    df_filtrado = df[
        (df["genero"].isin(genero_selecionado)) &
        (df["Sleep_Duration"] >= sono_selecionado[0]) & 
        (df["Sleep_Duration"] <= sono_selecionado[1]) &
        (df["Study_Hours"] >= estudo_selecionado[0]) & 
        (df["Study_Hours"] <= estudo_selecionado[1]) &
        (df["Social_Media_Hours"] >= redes_selecionado[0]) & 
        (df["Social_Media_Hours"] <= redes_selecionado[1])
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

    if not df_filtrado.empty:
        # --- PRIMEIRA LINHA DE GRÁFICOS (1 e 2) ---
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("1. Horas de Estudo x Notas")
            fig_estudo_notas = px.scatter(
                df_filtrado,
                x="Study_Hours",
                y="CGPA",
                color="genero",
                opacity=0.4,
                labels={
                    "Study_Hours": "Horas de Estudo Diárias", 
                    "CGPA": "Nota (CGPA)",
                    "genero": "Gênero"
                }
            )
            st.plotly_chart(fig_estudo_notas, use_container_width=True)

        with c2:
            st.subheader("2. Atividade Física x Depressão")
            df_ativ = df_filtrado.groupby(["atividade_fisica", "Depression"]).size().reset_index(name="Quantidade")
            fig_ativ = px.bar(
                df_ativ,
                x="atividade_fisica",
                y="Quantidade",
                color="Depression",
                barmode="group",
                text_auto=True,
                labels={
                    "atividade_fisica": "Pratica Atividade Física",
                    "Quantidade": "Total de Estudantes",
                    "Depression": "Sintomas Depressivos"
                }
            )
            st.plotly_chart(fig_ativ, use_container_width=True)

        st.divider()

        # --- SEGUNDA LINHA DE GRÁFICOS (3 e 4) ---
        c3, c4 = st.columns(2)

        with c3:
            st.subheader("3. Redes Sociais x Notas")
            df_redes_notas = df_filtrado.groupby("Social_Media_Hours")["CGPA"].mean().reset_index()
            fig_redes_notas = px.line(
                df_redes_notas,
                x="Social_Media_Hours",
                y="CGPA",
                markers=True,
                labels={
                    "Social_Media_Hours": "Horas em Redes Sociais",
                    "CGPA": "Média da Nota (CGPA)"
                }
            )
            st.plotly_chart(fig_redes_notas, use_container_width=True)

        with c4:
            st.subheader("4. Redes Sociais x Depressão")
            df_redes_dep = df_filtrado.groupby("Depression")["Social_Media_Hours"].mean().reset_index()
            fig_redes_dep = px.bar(
                df_redes_dep,
                x="Depression",
                y="Social_Media_Hours",
                color="Depression",
                text_auto=".1f",
                labels={
                    "Depression": "Sintomas Depressivos",
                    "Social_Media_Hours": "Média de Horas em Redes Sociais"
                }
            )
            st.plotly_chart(fig_redes_dep, use_container_width=True)

        st.divider()

        # --- TERCEIRA LINHA DE GRÁFICO (5) ---
        st.subheader("5. Notas x Estresse")
        fig_notas_estresse = px.density_heatmap(
            df_filtrado,
            x="CGPA",
            y="nivel_estresse",
            color_continuous_scale="Blues",
            labels={
                "CGPA": "Nota (CGPA)",
                "nivel_estresse": "Nível de Estresse"
            }
        )
        st.plotly_chart(fig_notas_estresse, use_container_width=True)

    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados. Ajuste os filtros na barra lateral.")

except FileNotFoundError:
    st.error("⚠️ ERRO: O arquivo 'base_tratada.csv' não foi encontrado.")
