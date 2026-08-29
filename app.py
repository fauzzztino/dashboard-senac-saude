import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🧠 Rede Social x Estresse")

@st.cache_data
def carregar_dados():
    return pd.read_csv("base_tratada.csv")

# Converte decimal (ex: 2.75) para o formato de relógio (ex: 2:45)
def formatar_hora(v):
    h, m = int(v), int(round((v - int(v)) * 60))
    return f"{h + 1 if m == 60 else h}:{0 if m == 60 else m:02d}"

try:
    df = carregar_dados()
    
    # Pega 10 casos únicos ordenados pelo tempo de tela
    df_plot = df.drop_duplicates(subset=["Social_Media_Hours"]).sample(10, random_state=42).sort_values("Social_Media_Hours")

    # Renderiza o gráfico
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(range(10), df_plot["nivel_estresse"], color="#1f77b4")
    ax.set_ylim(0, df_plot["nivel_estresse"].max() + 1)
    ax.set_title("Rede Social x Estresse")
    ax.set_xlabel("Tempo de uso de Redes Sociais")
    ax.set_ylabel("Nível de Estresse")
    ax.set_xticks(range(10))
    ax.set_xticklabels([formatar_hora(h) for h in df_plot["Social_Media_Hours"]])
    
    st.pyplot(fig)

except FileNotFoundError:
    st.error("⚠️ Arquivo 'base_tratada.csv' não encontrado.")
