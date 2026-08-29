import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

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

    # Aplica todos os filtros de uma vez
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

    # --- GRÁFICOS ---
    if not dff.empty:
        # 1. Gráfico Plotly Original (Redes Sociais x Estresse)
        df_plot = dff.sample(min(100, len(dff)), random_state=42)
        df_plot = df_plot.groupby(df_plot["Social_Media_Hours"].round(0))["nivel_estresse"].mean().round(0).reset_index()

        fig = px.line(
            df_plot, x="Social_Media_Hours", y="nivel_estresse", markers=True,
            color_discrete_sequence=px.colors.qualitative.Bold,
            labels={"Social_Media_Hours": "Horas em Redes Sociais", "nivel_estresse": "Nível Médio de Estresse"}
        )
        fig.update_layout(xaxis_title_font=dict(size=16), yaxis_title_font=dict(size=16))
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()

        # 2. Seu código integrado (Matplotlib)
        quantidade = dff["Depression"].value_counts().rename({"Não": "Sem depressão", "Sim": "Com depressão"})

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Distribuição de estudantes por depressão")
            fig_pie, ax_pie = plt.subplots(figsize=(8, 6))
            total = quantidade.sum()

            ax_pie.pie(
                quantidade,
                labels=quantidade.index,
                autopct=lambda pct: f"{pct:.1f}%\n({int(pct * total / 100):,})",
                colors=["#1f77b4", "#ff7f0e"] # Cores mais vivas para a pizza
            )
            st.pyplot(fig_pie)

        with col2:
            st.subheader("Redes Sociais x Depressão") # <--- Traduzido aqui!
            media = dff.groupby("Depression")["Social_Media_Hours"].mean().rename({"Não": "Sem depressão", "Sim": "Com depressão"})
            
            fig_bar, ax_bar = plt.subplots(figsize=(8, 6))
            bars = media.plot.bar(ax=ax_bar, color=["#2ca02c", "#d62728"]) 
            ax_bar.set_title("Média de uso de redes sociais")
            ax_bar.set_ylabel("Horas")
            plt.xticks(rotation=0) 
            
            # Adiciona os valores dentro das barras
            for bar in ax_bar.patches:
                # O texto vai ficar bem no meio da barra (altura / 2)
                ax_bar.annotate(f"{bar.get_height():.1f} h", 
                                (bar.get_x() + bar.get_width() / 2, bar.get_height() / 2), 
                                ha='center', va='center', color='white', fontsize=14, fontweight='bold')
            
            st.pyplot(fig_bar)

    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")

except FileNotFoundError:
    st.error("⚠️ ERRO: O arquivo 'base_tratada.csv' não foi encontrado.")
