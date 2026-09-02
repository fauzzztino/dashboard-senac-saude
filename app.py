import streamlit as st
import pandas as pd

st.title("Rede Social x Estresse")

df = pd.read_csv("base_tratada.csv")

# 1. Arredondamos as horas para números inteiros (ex: 2.75 vira 3, 1.2 vira 1)
df["Horas Arredondadas"] = df["Social_Media_Hours"].round().astype(int)

# 2. Agrupamos por tempo de tela e calculamos a MÉDIA de estresse (Conceito de Banco de Dados)
df_agrupado = df.groupby("Horas Arredondadas")["nivel_estresse"].mean().reset_index()

# 3. Criamos um texto bonito para o eixo X (ex: "2 horas") e definimos como índice
df_agrupado["Tempo de Uso"] = df_agrupado["Horas Arredondadas"].astype(str) + " horas"
df_agrupado = df_agrupado.set_index("Tempo de Uso")

# 4. Geramos o gráfico
st.bar_chart(
    df_agrupado["nivel_estresse"],
    x_label="Tempo de uso de Redes Sociais",
    y_label="Média do Nível de Estresse"
)
