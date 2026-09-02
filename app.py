import streamlit as st
import pandas as pd

st.title("Rede Social x Estresse")

df = pd.read_csv("base_tratada.csv")

# Arredonda o tempo de tela para horas cheias (ex: 1.0, 2.0...)
df["Social_Media_Hours"] = df["Social_Media_Hours"].round()

# Filtra para ter apenas 1 estudante por hora, seleciona 10 amostras e ordena
df_grafico = df.drop_duplicates(subset=["Social_Media_Hours"]).sample(10, random_state=42)
df_grafico = df_grafico.sort_values(by="Social_Media_Hours")

# Função para exibir horas exatas (ex: 1:00, 2:00)
def formata_hora(valor):
    h = int(valor)
    return f"{h}:00"

# Cria a coluna de texto formatada
df_grafico["Tempo de Uso"] = df_grafico["Social_Media_Hours"].apply(formata_hora)

# Garante que o gráfico respeite a ordem cronológica correta (do menor para o maior)
df_grafico["Tempo de Uso"] = pd.Categorical(
    df_grafico["Tempo de Uso"], 
    categories=[f"{int(h)}:00" for h in sorted(df_grafico["Social_Media_Hours"].unique())], 
    ordered=True
)

df_grafico = df_grafico.sort_values(by="Social_Media_Hours")

# Define o tempo formatado como índice para o Streamlit exibi-lo na horizontal embaixo das barras
df_grafico = df_grafico.set_index("Tempo de Uso")

# Gera o gráfico adaptado ao tema do Streamlit com as legendas nos eixos
st.bar_chart(
    df_grafico["nivel_estresse"],
    x_label="Tempo de uso de Redes Sociais",
    y_label="Nível de Estresse"
)
