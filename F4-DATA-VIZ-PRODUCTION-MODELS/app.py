import streamlit as st
import pandas as pd


@st.cache_data
def load_dataset():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/icarocarmona/Tech-Challenges-DTAT-Grupo-26/main/F4-DATA-VIZ-PRODUCTION-MODELS/petroleo_bruto.csv")
    return df


# Inicio do visual

st.set_page_config(
    page_title="Tech Challenge - Grupo 26",
    page_icon="⛽",
    # layout="wide",
    initial_sidebar_state="expanded",
)

st.header('⛽ Tech Challege - Grupo 26', divider='rainbow')

df = load_dataset()

#Alterando o nome da segunda coluna
df.rename(columns={df.columns[1]: 'Preco'}, inplace=True)

# Alterando o tipo da coluna para datetime
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

# Removendo linhas com valores não numéricos na coluna 'Preco'
df = df[~df['Preco'].str.contains('[^0-9.,]', na=False)]

# Convertendo a coluna Preco para float
df['Preco'] = df['Preco'].str.replace(',', '.').astype(float)

# Ordernando a coluna Data
df = df.sort_values(by='Data', ascending=True)

df = df.reset_index()
df = df.drop('index', axis=1)

import plotly.express as px

fig = px.line(data_frame=df, x='Data', y='Preco')

fig.show()

st.plotly_chart(fig, use_container_width=True)

st.dataframe(df)
