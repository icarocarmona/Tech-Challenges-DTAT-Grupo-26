import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import locale

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
home, tab2, tab3 = st.tabs(["🎯 Home", "📈 Chart", "🗃 Data"])


with tab3:
    st.dataframe(df, use_container_width=True, hide_index=True)


# Montando o filtro de ano
_min = 1970
_max = 2022
user_num_input = tab2.slider("Filtro de ano", min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
)

top10_paises(df, tab2)
agg_ano(df, tab2)





### HOME ### 

with home:
    # locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Isso define o formato para dólares americanos, ajuste conforme necessário


    st.write("# A história do vinho no Brasil:")
    st.write(" https://blog.famigliavalduga.com.br/a-historia-do-vinho-no-brasil-conheca-a-trajetoria-da-bebida-em-territorio-nacional/")

    st.write("O século XXI começou com boas perspectivas para o vinho no Brasil: a safra de 1999 teve reputação de ter sido uma das melhores produzidas por aqui até então. Nos anos 2000, o país continuou a se desenvolver nesse sentido, com tecnologias cada vez mais sofisticadas e preocupação crescente com a qualidade dos vinhos nacionais.")

    # df_filtrado = df[(df['Ano'] == 1999)][['Quantidade (L)','Valor U$']].sum()
    df_filtrado_2 = df[df['Ano'].isin([1999,2000, 2001, 2002])]
    soma_valores = df_filtrado_2.groupby('Ano')[['Quantidade (L)','Valor U$']].sum()
    df_soma_anos = soma_valores.reset_index()
    df_soma_anos.columns = ['Ano','Soma de Quantidade (L)' ,'Soma de Valor U$']
    df_soma_anos['Variação Vl Pct'] = df_soma_anos['Soma de Valor U$'].pct_change() * 100
    df_soma_anos['Variação Qtd Pct'] = df_soma_anos['Soma de Quantidade (L)'].pct_change() * 100


    valor_1999 = df_soma_anos[df_soma_anos['Ano'] == 1999]['Soma de Valor U$']
    qtd_1999 = df_soma_anos[df_soma_anos['Ano'] == 1999]['Soma de Quantidade (L)']

    valor_final = locale.format_string('%d', valor_1999, grouping=True)
    qtd_final = locale.format_string('%d', qtd_1999, grouping=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Ano", "1999")
    col2.metric("Quantidade (L)", f"{qtd_final}")
    col3.metric("Valor U$", f"$ {valor_final}")


    valor = df_soma_anos[df_soma_anos['Ano'] == 2000]['Soma de Valor U$']
    qtd = df_soma_anos[df_soma_anos['Ano'] == 2000]['Soma de Quantidade (L)']

    valor_final = locale.format_string('%d', valor, grouping=True)
    qtd_final = locale.format_string('%d', qtd, grouping=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Ano", "2000")
    col2.metric("Quantidade (L)", f"{qtd_final}" , "-7%")
    col3.metric("Valor U$", f"$ {valor_final}", "-14%")

    st.write("Em 2002, as vinícolas da região do Vale dos Vinhedos, na Serra Gaúcha, chegaram a receber do Instituto Nacional da Propriedade Industrial (INPI) o direito de ter um selo de identificação de procedência geográfica! Foi o primeiro passo em direção à cobiçada denominação de origem, além de garantir mais qualidade para as garrafas produzidas ali devido às exigências do selo.")
    st.bar_chart(data=df_soma_anos, x="Ano", y=["Soma de Valor U$", "Soma de Quantidade (L)"])

