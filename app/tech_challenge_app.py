import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.pyplot as plt


from streamlit.delta_generator import DeltaGenerator 


@st.cache_data
def load_data():
    dados = pd.read_csv("https://raw.githubusercontent.com/icarocarmona/tech_challenge_f1/main/dados/trusted/dados_de_vinhos.csv", sep=";" )
    # filtra apenas vinho de mesa
    dados = dados[dados['Tipo Vinho'] == 'Vinho De Mesa'].reset_index(drop=True)
    dados['Vl Litro'] = dados['Valor U$'] / dados['Quantidade (L)']
    return dados

def top10_paises(dados: pd.DataFrame, tab: DeltaGenerator):
    
    df = dados[dados['Ano'].between(*user_num_input)]
    top_10_paises = df.groupby(by='Destino')['Valor U$'].sum().sort_values(ascending=False).head(10).index
    vinhos_de_mesa_filtrado = df[dados['Destino'].isin(top_10_paises)]
    vinhos_de_mesa_filtrado = vinhos_de_mesa_filtrado[vinhos_de_mesa_filtrado['Valor U$'] > 0 ]

    fig = plt.figure(figsize=(10, 4))
    sns.set_theme(style='dark')
    sns.lineplot(data=vinhos_de_mesa_filtrado,
            x='Ano', y= 'Valor U$', hue='Destino')
    tab.pyplot(fig)

    fig2 = plt.figure(figsize=(10, 4))
    sns.lineplot(data=vinhos_de_mesa_filtrado, x='Ano', y='Valor U$', hue='Tipo Vinho')
    tab2.pyplot(fig2)

def agg_ano(dados, tab):
    df = dados[dados['Ano'].between(*user_num_input)]

    agg_ano = df.groupby(by='Ano')[['Valor U$', 'Quantidade (L)']].sum()
    fig = plt.figure(figsize=(10, 4))
    sns.lineplot(agg_ano)
    tab.pyplot(fig)


    agg_ano['Vl Litro'] = agg_ano['Valor U$']/agg_ano['Quantidade (L)']

    fig = plt.figure(figsize=(10, 4))
    sns.lineplot(y=agg_ano['Valor U$'], x=agg_ano.index)
    
    tab.pyplot(fig)



    

st.write('# Tech challenge')
# carregando os dados
df = load_data()
tab1, tab2, tab3 = st.tabs(["🎯 Objetivo", "📈 Chart", "🗃 Data"])

tab3.table(df.head(10))

# Montando o filtro de ano
_min = 1970
_max = 2022
user_num_input = tab2.slider("Filtro de ano", min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
)

top10_paises(df, tab2)
agg_ano(df, tab2)
