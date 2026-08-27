import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração visual da página
st.set_page_config(page_title="Saúde Mental - Universitários", layout="wide")

st.title("🧠 Dashboard: Saúde Mental e Hábitos de Universitários")
st.markdown("Análise dos fatores associados à depressão, estresse e rotina acadêmica.")

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
            st.subheader("1. Horas de Estudo x Notas")
            # Arredonda as horas de estudo para agrupar as barras e evitar poluição visual
            df_g1 = df_filtrado.copy()
            df_g1["Study_Hours_Group"] = df_g1["Study_Hours"].round(0)
            df_g1 = df_g1.groupby("Study_Hours_Group")["CGPA"].mean().reset_index()
            df_g1["CGPA"] = df_g1["CGPA"].round(1)
            
            fig1 = px.bar(
                df_g1,
                x="Study_Hours_Group",
                y="CGPA",
                color_discrete_sequence=CORES_ALTO_CONTRASTE,
                labels={
                    "Study_Hours_Group": "Horas de Estudo Diárias (Arredondadas)", 
                    "CGPA": "Média da Nota (CGPA)"
                }
            )
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            st.subheader("2. Atividade Física x Depressão")
            coluna_ativ = "Physical_Activity_Minutes" if "Physical_Activity_Minutes" in df_filtrado.columns else "atividade_fisica"
            df_g2 = df_filtrado.groupby("Depression")[coluna_ativ].mean().reset_index()
            df_g2[coluna_ativ] = df_g2[coluna_ativ].round(0)
            
            fig2 = px.bar(
                df_g2,
                x="Depression",
                y=coluna_ativ,
                color="Depression",
                color_discrete_sequence=CORES_ALTO_CONTRASTE,
                labels={
                    "Depression": "Sintomas Depressivos",
                    coluna_ativ: "Média de Atividade Física (Minutos)"
                }
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        # --- SEGUNDA LINHA DE GRÁFICOS (3 e 4) ---
        c3, c4 = st.columns(2)

        with c3:
            st.subheader("3. Redes Sociais x Notas")
            # Arredonda as horas de redes sociais para reduzir o número de barras
            df_g3 = df_filtrado.copy()
            df_g3["Social_Group"] = df_g3["Social_Media_Hours"].round(0)
            df_g3 = df_g3.groupby("Social_Group")["CGPA"].mean().reset_index()
            df_g3["CGPA"] = df_g3["CGPA"].round(1)
            
            fig3 = px.bar(
                df_g3,
                x="Social_Group",
                y="CGPA",
                color_discrete_sequence=CORES_ALTO_CONTRASTE,
                labels={
                    "Social_Group": "Horas em Redes Sociais (Arredondadas)",
                    "CGPA": "Média da Nota (CGPA)"
                }
            )
            st.plotly_chart(fig3, use_container_width=True)

        with c4:
            st.subheader("4. Redes Sociais, Sono e Depressão")
            # Agrupa as redes sociais em blocos inteiros para a linha não ficar picotada
            df_g4 = df_filtrado.copy()
            df_g4["Social_Group"] = df_g4["Social_Media_Hours"].round(0)
            df_g4 = df_g4.groupby(["Social_Group", "Depression"])["Sleep_Duration"].mean().reset_index()
            df_g4["Sleep_Duration"] = df_g4["Sleep_Duration"].round(1)
            
            fig4 = px.line(
                df_g4,
                x="Social_Group",
                y="Sleep_Duration",
                color="Depression",
                markers=True,
                color_discrete_sequence=CORES_ALTO_CONTRASTE,
                labels={
                    "Social_Group": "Horas em Redes Sociais",
                    "Sleep_Duration": "Média de Horas de Sono",
                    "Depression": "Sintomas Depressivos"
                }
            )
            st.plotly_chart(fig4, use_container_width=True)

        st.divider()

        # --- TERCEIRA LINHA DE GRÁFICO (5) ---
        st.subheader("5. Notas x Estresse")
        # Arredonda as notas para agrupar as barras do estresse de forma limpa
        df_g5 = df_filtrado.copy()
        df_g5["CGPA_Group"] = df_g5["CGPA"].round(1)
        df_g5 = df_g5.groupby("CGPA_Group")["nivel_estresse"].mean().reset_index()
        df_g5["nivel_estresse"] = df_g5["nivel_estresse"].round(0)
        
        fig5 = px.bar(
            df_g5,
            x="CGPA_Group",
            y="nivel_estresse",
            color_discrete_sequence=CORES_ALTO_CONTRASTE,
            labels={
                "CGPA_Group": "Nota (CGPA Arredondada)",
                "nivel_estresse": "Nível Médio de Estresse"
            }
        )
        st.plotly_chart(fig5, use_container_width=True)

    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados. Ajuste os filtros na barra lateral.")

except FileNotFoundError:
    st.error("⚠️ ERRO: O arquivo 'base_tratada.csv' não foi encontrado.")
