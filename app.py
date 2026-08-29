import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Saúde Mental - Universitários", layout="wide")
st.title("🧠 Dashboard: Redes Sociais x Estresse")
st.markdown("Análise do impacto do tempo de tela no estresse (Amostra de até 100 estudantes).")

@st.cache_data
def carregar_dados():
    df = pd.read_csv("base_tratada.csv")
    # Substitui os valores de forma direta
    substituicoes = {"Depression": {True: "Sim", False: "Não", "True": "Sim", "False": "Não"}, 
                     "genero": {"Female": "Feminino", "Male": "Masculino"}}
    return df.replace(substituicoes)

try:
    df = carregar_dados()

    # --- FILTROS ---
    st.sidebar.header("⚙️ Filtros do Painel")
    
    # Filtro de Gênero
    opcoes_gen = [g for g in ["Masculino", "Feminino"] if g in df["genero"].dropna().unique()] or list(df["genero"].dropna().unique())
    f_gen = st.sidebar.multiselect("Gênero:", opcoes_gen, opcoes_gen)

    # Função enxuta para criar sliders
    def criar_slider(label, coluna):
        vmin, vmax = float(df[coluna].min()), float(df[coluna].max())
        return st.sidebar.slider(label, vmin, vmax, (vmin, vmax))

    f_sono = criar_slider("Tempo de Sono (horas):", "Sleep_Duration")
    f_estudo = criar_slider("Horas de Estudo:", "Study_Hours")
    f_redes = criar_slider("Horas em Redes Sociais:", "Social_Media_Hours")

    # Aplica todos os filtros de uma vez usando .between()
    dff = df[
        df["genero"].isin(f_gen) & 
        df["Sleep_Duration"].between(*f_sono) & 
        df["Study_Hours"].between(*f_estudo) & 
        df["Social_Media_Hours"].between(*f_redes)
    ]

    # --- MÉTRICAS ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Estudantes Analisados", len(dff))
    c2.metric("Estresse Médio", f"{dff['nivel_estresse'].mean():.0f}" if not dff.empty else "0")
    c3.metric("Média Redes Sociais", f"{dff['Social_Media_Hours'].mean():.1f} h" if not dff.empty else "0 h")
    st.divider()

    # --- GRÁFICO ---
    if not dff.empty:
        # Pega até 100 amostras e agrupa os dados em apenas 2 linhas de código
        df_plot = dff.sample(min(100, len(dff)), random_state=42)
        df_plot = df_plot.groupby(df_plot["Social_Media_Hours"].round(0))["nivel_estresse"].mean().round(0).reset_index()

        fig = px.line(
            df_plot, x="Social_Media_Hours", y="nivel_estresse", markers=True,
            color_discrete_sequence=px.colors.qualitative.Bold,
            labels={"Social_Media_Hours": "Horas em Redes Sociais", "nivel_estresse": "Nível Médio de Estresse"}
        )
        fig.update_layout(xaxis_title_font=dict(size=16), yaxis_title_font=dict(size=16))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")

except FileNotFoundError:
    st.error("⚠️ ERRO: O arquivo 'base_tratada.csv' não foi encontrado.")
