import streamlit as st
import pandas as pd

st.title("Rede Social x Estresse")

df = pd.read_csv("base_tratada.csv")

# Filtra para ter apenas 1 estudante por quantidade de horas e pega 10 aleatórios
df_grafico = df.drop_duplicates(subset=["Social_Media_Hours"]).sample(10, random_state=42)
df_grafico = df_grafico.sort_values(by="Social_Media_Hours")

# Função para formatar o número (ex: 2.5 vira 2:30)
def formata_hora(valor):
    h = int(valor)
    m = int((valor - h) * 60)
    return f"{h}:{m:02d}"

# Cria a coluna com as horas formatadas
df_grafico["Tempo de Uso"] = df_grafico["Social_Media_Hours"].apply(formata_hora)

# Define o tempo como índice para o gráfico manter a ordem do menor para o maior
df_grafico = df_grafico.set_index("Tempo de Uso")

# Gera o gráfico com as legendas laterais (labels)
st.bar_chart(
    df_grafico["nivel_estresse"],
    x_label="Tempo de uso de Redes Sociais",
    y_label="Nível de Estresse"
