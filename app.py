import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração visual da página
st.set_page_config(page_title="Saúde Mental - Universitários", layout="wide")

st.title("🧠 Dashboard: Saúde Mental e Hábitos de Universitários")
st.markdown("Análise detalhada dos fatores associados ao estresse e à depressão acadêmica.")

# Paleta de cores de alto contraste padrão
CORES_ALTO_CONTRASTE = px.colors.qualitative.Bold

# Carrega a base de dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("base_tratada.csv")
    
    if "Depression" in df.columns:
        df["Depression"] = df["Depression"].replace({True: "Sim", False: "Não", "True": "Sim", "False": "Não"})
    
    if "genero" in df.columns:
        df["genero"] = df["genero"].replace({"Female": "Feminino", "Male": "Masculino", "Other": "Outros"})
        
    return df

try:
    df = carregar_dados()

    # --- FILTROS (BARRA LATERAL) ---
    st.sidebar.header("⚙️ Filtros do Painel")
    
    opcoes_genero_disponiveis = [g for g in ["Masculino", "Feminino"] if g in df["genero"].dropna().unique()]
    if not opcoes_genero_disponiveis:
        opcoes_genero_disponiveis = list(df["genero"].dropna().unique())

    genero_selecionado = st.sidebar.multiselect(
        "Selecione o Gênero:",
        options=opcoes_genero_disponiveis,
        default=opcoes_genero_disponiveis
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
        col2.metric("Nível Médio de Estresse", f"{df_filtrado['nivel_estresse'].mean():.0f}")
        col3.metric("Média de Horas de Sono", f"{df_filtrado['Sleep_Duration'].mean():.0f} h")
    else:
        col2.metric("Nível Médio de Estresse", "0")
        col3.metric("Média de Horas de Sono", "0 h")

    st.divider()

    if not df_filtrado.empty:
        # --- PRIMEIRA LINHA DE GRÁFICOS (1 e 2) ---
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("1. Notas x Estresse")
            df_g1 = df_filtrado.copy()
            df_g1["CGPA_Group"] = df_g1["CGPA"].round(1)
            df_g1 = df_g1.groupby("CGPA_Group")["nivel_estresse"].mean().reset_index()
            df_g1["nivel_estresse"] = df_g1["nivel_estresse"].round(0)
            
            fig1 = px.bar(
                df_g1,
                x="CGPA_Group",
                y="nivel_estresse",
                color_discrete_sequence=CORES_ALTO_CONTRASTE,
                labels={
                    "CGPA_Group": "Nota (CGPA)", 
                    "nivel_estresse": "Nível Médio de Estresse"
                }
            )
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            st.subheader("2. Sono x Estresse")
            df_g2 = df_filtrado.copy()
            df_g2["Sono_Group"] = df_g2["Sleep_Duration"].round(0)
            df_g2 = df_g2.groupby("Sono_Group")["nivel_estresse"].mean().reset_index()
            df_g2["nivel_estresse"] = df_g2["nivel_estresse"].round(0)
            
            fig2 = px.line(
                df_g2,
                x="Sono_Group",
                y="nivel_estresse",
                markers=True,
                color_discrete_sequence=CORES_ALTO_CONTRASTE,
                labels={
                    "Sono_Group": "Horas de Sono",
                    "nivel_estresse": "Nível Médio de Estresse"
                }
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        # --- SEGUNDA LINHA DE GRÁFICOS (3 e 4) ---
        c3, c4 = st.columns(2)

        with c3:
            st.subheader("3. Depressão x Estresse")
            df_g3 = df_filtrado.groupby("Depression")["nivel_estresse"].mean().reset_index()
            df_g3["nivel_estresse"] = df_g3["nivel_estresse"].round(0)
            
            fig3 = px.bar(
                df_g3,
                x="Depression",
                y="nivel_estresse",
                color="Depression",
                color_discrete_sequence=CORES_ALTO_CONTRASTE,
                labels={
                    "Depression": "Sintomas Depressivos",
                    "nivel_estresse": "Nível Médio de Estresse"
                }
            )
            st.plotly_chart(fig3, use_container_width=True)

        with c4:
            st.subheader("4. Atividade Física x Estresse")
            coluna_ativ = "Physical_Activity_Minutes" if "Physical_Activity_Minutes" in df_filtrado.columns else "atividade_fisica"
            df_g4 = df_filtrado.copy()
            # Se for coluna de minutos, agrupa em faixas de 30 min para limpar o gráfico
            if coluna_ativ in df_g4.columns and df_g4[coluna_ativ].dtype in ['float64', 'int64']:
                df_g4["Ativ_Group"] = (df_g4[coluna_ativ] // 30) * 30
                eixo_x = "Ativ_Group"
                label_x = "Atividade Física (Minutos - Agrupados)"
            else:
                eixo_x = coluna_ativ
                label_x = "Pratica Atividade Física"
                
            df_g4 = df_g4.groupby(eixo_x)["nivel_estresse"].mean().reset_index()
            df_g4["nivel_estresse"] = df_g4["nivel_estresse"].round(0)
            
            fig4 = px.bar(
                df_g4,
                x=eixo_x,
                y="nivel_estresse",
                color_discrete_sequence=CORES_ALTO_CONTRASTE,
                labels={
                    eixo_x: label_x,
                    "nivel_estresse": "Nível Médio de Estresse"
                }
            )
            st.plotly_chart(fig4, use_container_width=True)

        st.divider()

        # --- TERCEIRA LINHA DE GRÁFICOS (5 e 6) ---
        c5, c6 = st.columns(2)

        with c5:
            st.subheader("5. Redes Sociais x Estresse")
            df_g5 = df_filtrado.copy()
            df_g5["Social_Group"] = df_g5["Social_Media_Hours"].round(0)
            df_g5 = df_g5.groupby("Social_Group")["nivel_estresse"].mean().reset_index()
            df_g5["nivel_estresse"] = df_g5["nivel_estresse"].round(0)
            
            fig5 = px.line(
                df_g5,
                x="Social_Group",
                y="nivel_estresse",
                markers=True,
                color_discrete_sequence=CORES_ALTO_CONTRASTE,
                labels={
                    "Social_Group": "Horas em Redes Sociais",
                    "nivel_estresse": "Nível Médio de Estresse"
                }
            )
            st.plotly_chart(fig5, use_container_width=True)

        with c6:
            st.subheader("6. Redes Sociais x Depressão")
            df_g6 = df_filtrado.copy()
            df_g6["Social_Group"] = df_g6["Social_Media_Hours"].round(0)
            df_g6 = df_g6.groupby("Depression")["Social_Group"].mean().reset_index()
            df_g6["Social_Group"] = df_g6["Social_Group"].round(1)
            
            fig6 = px.bar(
                df_g6,
                x="Depression",
                y="Social_Group",
                color="Depression",
                color_discrete_sequence=CORES_ALTO_CONTRASTE,
                labels={
                    "Depression": "Sintomas Depressivos",
                    "Social_Group": "Média de Horas em Redes Sociais"
                }
            )
            st.plotly_chart(fig6, use_container_width=True)

    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados. Ajuste os filtros na barra lateral.")

except FileNotFoundError:
    st.error("⚠️ ERRO: O arquivo 'base_tratada.csv' não foi encontrado.")
