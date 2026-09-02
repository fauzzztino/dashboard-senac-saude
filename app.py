import streamlit as st
import pandas as pd
import altair as alt

st.title("Rede Social x Estresse")

df = pd.read_csv("base_tratada.csv")

# Arredonda o tempo de tela para horas cheias
df["Social_Media_Hours"] = df["Social_Media_Hours"].round()

# Filtra, pega 10 amostras e ordena
df_grafico = df.drop_duplicates(subset=["Social_Media_Hours"]).sample(10, random_state=42)
df_grafico = df_grafico.sort_values(by="Social_Media_Hours")

# Função para exibir horas exatas
def formata_hora(valor):
    h = int(valor)
    return f"{h}:00"

# Cria a coluna de texto formatada
df_grafico["Tempo de Uso"] = df_grafico["Social_Media_Hours"].apply(formata_hora)

# Cria o gráfico usando o Altair para forçar os números do eixo X na horizontal (labelAngle=0)
chart = alt.Chart(df_grafico).mark_bar().encode(
    x=alt.X(
        'Tempo de Uso:N', 
        sort=None, 
        title='Tempo de uso de Redes Sociais',
        axis=alt.Axis(labelAngle=0) # <--- Força o texto a ficar na horizontal!
    ),
    y=alt.Y(
        'nivel_estresse:Q', 
        title='Nível de Estresse'
    )
)

# Exibe o gráfico na tela mantendo o tema do Streamlit
st.altair_chart(chart, use_container_width=True)
