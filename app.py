import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Saúde Mental - Universitários", layout="wide")
st.title("🧠 Dashboard: Redes Sociais x Estresse")
st.markdown("Análise do impacto do tempo de tela no estresse.")

@st.cache_data
def carregar_dados():
    df = pd.read_csv("base_tratada.csv")
    substituicoes = {"Depression": {True: "Sim", False: "Não", "True": "Sim", "False": "Não"}, 
                     "genero": {"Female": "Feminino", "Male": "Masculino"}}
    return df.replace(substituicoes)

# Função para converter número decimal (ex: 2.75) para formato de hora (ex: 2:45)
def decimal_para_horas(valor_decimal):
    if pd.isna(valor_decimal): return "0:00"
    horas = int(valor_decimal)
    minutos = int(round((valor_decimal - horas) * 60))
    if minutos == 60:
        horas += 1
        minutos = 0
    return f"{horas}:{minutos:02d}"

try:
    df = carregar_dados()

    # --- FILTROS ---
    st.sidebar.header("⚙️ Filtros do Painel")
    
    opcoes_gen = [g for g in ["Masculino", "Feminino"] if g in df["genero"].dropna().unique()] or list(df["genero"].dropna().unique())
    f_gen = st.sidebar.multiselect("Gênero:", opcoes_gen, opcoes_gen)

    def criar_slider(label, coluna):
        vmin, vmax = float(df[coluna].min()), float(df[coluna].max())
        return st.sidebar.slider(label, vmin, vmax, (vmin, vmax))

    f_sono = criar_slider("Tempo de Sono (horas):", "Sleep_Duration")
    f_estudo = criar_slider("Horas de Estudo:", "Study_Hours")
    f_redes = criar_slider("Horas em Redes Sociais:", "Social_Media_Hours")

    dff = df[
        df["genero"].isin(f_gen) & 
        df["Sleep_Duration"].between(*f_sono) & 
        df["Study_Hours"].between(*f_estudo) & 
        df["Social_Media_Hours"].between(*f_redes)
    ]

    # --- MÉTRICAS ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Estudantes Analisados", len(dff))
    c2.metric("Estresse Médio", f"{dff['nivel_estresse'].mean():.1f}" if not dff.empty else "0")
    # Usa a nova função para mostrar no formato relógio no topo
    c3.metric("Média Redes Sociais", decimal_para_horas(dff['Social_Media_Hours'].mean()) if not dff.empty else "0:00")
    st.divider()

    # --- GRÁFICOS ---
    if not dff.empty:
        
        # 1. Gráfico Transformado - Ajustado para mostrar diferença real
        st.subheader("Redes Sociais x Estresse")
        
        # Agrupa sem arredondar agressivamente para mostrar a diferença real nas alturas
        media_estresse = dff.groupby(dff["Social_Media_Hours"].round(0))["nivel_estresse"].mean()

        fig1, ax1 = plt.subplots(figsize=(10, 4))
        media_estresse.plot.bar(ax=ax1, color="#1f77b4") 
        
        # Corta a base do eixo Y dinamicamente para ressaltar a diferença visual das barras
        min_y = max(0, media_estresse.min() - 0.5)
        ax1.set_ylim(min_y, media_estresse.max() + 0.5)
        
        ax1.set_title("Nível Médio de Estresse por Horas de Tela")
        ax1.set_xlabel("Horas em Redes Sociais (Agrupadas)")
        ax1.set_ylabel("Nível de Estresse")
        plt.xticks(rotation=0) 
        
        for bar in ax1.patches:
            if bar.get_height() > 0: 
                # Coloca a nota de estresse (ex: 3.4) com 1 casa decimal para mostrar precisão
                meio_da_barra_visivel = min_y + (bar.get_height() - min_y) / 2
                ax1.annotate(f"{bar.get_height():.1f}", 
                                (bar.get_x() + bar.get_width() / 2, meio_da_barra_visivel), 
                                ha='center', va='center', color='white', fontsize=12, fontweight='bold')
        
        st.pyplot(fig1)
        
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
                colors=["#1f77b4", "#ff7f0e"] 
            )
            st.pyplot(fig_pie)

        with col2:
            st.subheader("Redes Sociais x Depressão")
            media = dff.groupby("Depression")["Social_Media_Hours"].mean().rename({"Não": "Sem depressão", "Sim": "Com depressão"})
            
            fig_bar, ax_bar = plt.subplots(figsize=(8, 6))
            media.plot.bar(ax=ax_bar, color=["#2ca02c", "#d62728"]) 
            ax_bar.set_title("Média de uso de redes sociais")
            ax_bar.set_ylabel("Tempo Médio")
            plt.xticks(rotation=0) 
            
            # Adiciona os valores no formato relógio (ex: 2:45) dentro das barras
            for bar in ax_bar.patches:
                altura = bar.get_height()
                texto_horas = decimal_para_horas(altura)
                ax_bar.annotate(texto_horas, 
                                (bar.get_x() + bar.get_width() / 2, altura / 2), 
                                ha='center', va='center', color='white', fontsize=14, fontweight='bold')
            
            st.pyplot(fig_bar)

    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")

except FileNotFoundError:
    st.error("⚠️ ERRO: O arquivo 'base_tratada.csv' não foi encontrado.")
