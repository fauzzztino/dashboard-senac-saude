import streamlit as st
import pandas as pd

st.title("Rede Social x Estresse")

df = pd.read_csv("base_tratada.csv")
df_grafico = df.drop_duplicates(subset=["Social_Media_Hours"]).sample(10, random_state=42)
df_grafico = df_grafico.sort_values(by="Social_Media_Hours")

def formata_hora(valor):
    h = int(valor)
    m = int((valor - h) * 60)
    return f"{h}:{m:02d}"

df_grafico["Tempo de Uso"] = df_grafico["Social_Media_Hours"].apply(formata_hora)

df_grafico = df_grafico.set_index("Tempo de Uso")

st.bar_chart(
    df_grafico["nivel_estresse"],
    x_label="Tempo de uso de Redes Sociais",
    y_label="Nível de Estresse"
)
