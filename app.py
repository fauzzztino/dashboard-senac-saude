import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título da página
st.title("Dashboard de Saúde Mental")
st.subheader("Análise: Rede Social x Estresse")

# Carrega a base de dados
dados = pd.read_csv("base_tratada.csv")

# 1. Filtra para não ter valores repetidos de horas de redes sociais
dados_unicos = dados.drop_duplicates(subset=["Social_Media_Hours"])

# 2. Pega uma amostra de 10 linhas e ordena pelo tempo de tela (do menor para o maior)
amostra_estudantes = dados_unicos.sample(n=10, random_state=42)
amostra_estudantes = amostra_estudantes.sort_values(by="Social_Media_Hours")

# 3. Função simples para converter o número decimal em horas e minutos (ex: 2.5 vira 2:30)
def converter_para_horas(valor):
    horas = int(valor)
    minutos = int((valor - horas) * 60)
    return f"{horas}:{minutos:02d}"

# Cria a lista com os horários formatados para usar no eixo X
eixo_x_horas = []
for tempo in amostra_estudantes["Social_Media_Hours"]:
    texto_formatado = converter_para_horas(tempo)
    eixo_x_horas.append(texto_formatado)

# 4. Monta o gráfico utilizando o Matplotlib de forma básica
figura, eixo = plt.subplots(figsize=(10, 5))

# Desenha as colunas
eixo.bar(range(10), amostra_estudantes["nivel_estresse"], color="#1f77b4")

# Configurações visuais simples do gráfico
eixo.set_title("Relação entre Rede Social e Nível de Estresse")
eixo.set_xlabel("Tempo de uso de Redes Sociais")
eixo.set_ylabel("Nível de Estresse")

# Define os rótulos do eixo X com os horários convertidos
eixo.set_xticks(range(10))
eixo.set_xticklabels(eixo_x_horas)

# Exibe o gráfico na tela do Streamlit
st.pyplot(figura)
