import streamlit as st
import pandas as pd

st.title("Rede Social x Estresse")

df = pd.read_csv("base_tratada.csv")

# Arredonda o tempo de tela para horas cheias (ex: 1.0, 2.0...)
df["Social_Media_Hours"] = df["Social_Media_Hours"].round()

# Agrupa por hora e calcula a MÉDIA do nível de estresse de todos os alunos da base
df_grafico = df.groupby("Social_Media_Hours")["nivel_estresse"].mean().reset_index()

# Ordena do menor para o maior tempo
df_grafico = df_grafico.sort_values(by="Social_Media_Hours")

# Função para exibir horas exatas (ex: 2:00, 3:00)
def formata_hora(valor):
    h = int(valor)
    return f"{h}:00"

# Cria a coluna de texto formatada
df_grafico["Tempo de Uso"] = df_grafico["Social_Media_Hours"].apply(formata_hora)

# Garante que o gráfico respeite a ordem cronológica correta
df_grafico["Tempo de Uso"] = pd.Categorical(
    df_grafico["Tempo de Uso"], 
    categories=[f"{int(h)}:00" for h in df_grafico["Social_Media_Hours"]], 
    ordered=True
)

df_grafico = df_grafico.set_index("Tempo de Uso")

# Gera o gráfico com a legenda atualizada para indicar que são médias
st.bar_chart(
    df_grafico["nivel_estresse"],
    x_label="Tempo de uso de Redes Sociais",
    y_label="Média do Nível de Estresse"
)
