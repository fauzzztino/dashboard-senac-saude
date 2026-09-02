import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

sem_depressão = dados[dados["Depression"] == False]
com_depressão = dados[dados["Depression"] == True]
quantidade = dados["Depression"].value_counts()
quantidade.index = ["Sem depressão", "Com depressão"]

col1, col2 = st.columns(2)

with col1:
	st.subheader("Distribuição de estudantes por depressão")
	fig, ax = plt.subplots(figsize=(8, 6))
	total = quantidade.sum()

	ax.pie(
		quantidade,
		labels=quantidade.index,
		autopct=lambda pct: f"{pct:.1f}%\n({int(pct * total / 100):,})"
	)

	st.pyplot(fig)

media = dados.groupby("Depression")["Social_Media_Hours"].mean()
media.index = ["Sem depressão", "Com depressão"]

with col2:
	st.subheader("Social Media x Depression")
	fig, ax = plt.subplots(figsize=(8, 6))
	media.plot.bar(ax=ax, color=["#1f77b4", "#ff7f0e"])
	ax.bar_label(
        ax.containers[0],
        labels=[f"{valor:.2f} h" for valor in media],
        padding=3,
		fontsize=14
    )

	ax.set_title("Média de uso de redes sociais")
	ax.set_ylabel("Horas")
	ax.tick_params(axis="x", labelrotation=0)
	ax.set_ylim(0, 4)

	ax.plot(
		[0, 1],
		[media.iloc[0], media.iloc[0]],
		linestyle="--",
		color="#1f77b4"
	)

	st.pyplot(fig)
