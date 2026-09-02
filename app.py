import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Rede Social x Estresse")
df = pd.read_csv("base_tratada.csv")
df_grafico = df.drop_duplicates(subset=["Social_Media_Hours"]).sample(10, random_state=42)
df_grafico = df_grafico.sort_values(by="Social_Media_Hours")

def formata_hora(valor):
    h = int(valor)
    m = int((valor - h) * 60)
    return f"{h}:{m:02d}"

rotulos_tempo = [formata_hora(t) for t in df_grafico["Social_Media_Hours"]]
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(range(10), df_grafico["nivel_estresse"], color="#1f77b4")
ax.set_title("Rede Social x Estresse")
ax.set_xlabel("Tempo de uso de Redes Sociais")
ax.set_ylabel("Nível de Estresse")
ax.set_xticks(range(10))
ax.set_xticklabels(rotulos_tempo)
st.pyplot(fig)

