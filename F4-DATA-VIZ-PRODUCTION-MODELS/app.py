import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import joblib
import numpy as np
import plotly.express as px
from statsmodels.tsa.seasonal import seasonal_decompose


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

def plot_predict(current_week_dates, current_week_prices, next_week_dates, next_week_predictions):
    # Criar as figuras
    fig = go.Figure()

    # Adicionar os preços atuais
    fig.add_trace(go.Scatter(x=current_week_dates, y=current_week_prices,
                             mode='lines+markers',
                             name='Preços Atuais',
                             line=dict(color='blue'),
                             marker=dict(symbol='circle')))

    # Adicionar as previsões para a próxima semana
    fig.add_trace(go.Scatter(x=next_week_dates, y=next_week_predictions,
                             mode='lines+markers',
                             name='Previsões para a Próxima Semana',
                             line=dict(color='red', dash='dash'),
                             marker=dict(symbol='circle')))

    # Atualizar o layout do gráfico
    fig.update_layout(
        title='Preços Reais e Previsões para as Últimas Duas Semanas',
        xaxis_title='Data',
        yaxis_title='Preço',
        xaxis=dict(
            tickformat='%Y-%m-%d',
            tickmode='linear'
        ),
        legend=dict(
            x=0.01, y=0.99,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        autosize=False,
        width=1000,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=4
        ),
        #   paper_bgcolor="LightSteelBlue"
    )

    # Exibir o gráfico
#   fig.show()
    st.plotly_chart(fig)

y = df['Preco'].values  # Output é o preço atual

model = joblib.load('./modelo.pkl')

# st.write(model.predict(y[-1].reshape(1, -1)))

# Fazer previsões para a próxima semana usando os últimos dados conhecidos
last_known_data = y[-1].reshape(1, -1)
next_week_predictions = []
for _ in range(7):  # para cada dia da próxima semana
    next_day_pred = model.predict(last_known_data)[0]
    next_week_predictions.append(next_day_pred)
    last_known_data = np.roll(last_known_data, -1)
    last_known_data[0, -1] = next_day_pred

# As datas correspondentes à próxima semana
next_week_dates = pd.date_range(df['Data'].iloc[-1], periods=8)[1:]

# Selecionar os dados da semana atual (últimos 7 dias do dataset)
current_week_dates = df['Data'].iloc[-7:]
current_week_prices = df['Preco'].iloc[-7:]


fig = px.line(data_frame=df, x='Data', y='Preco')

# fig.show()

st.plotly_chart(fig, use_container_width=True)

# st.dataframe(df)

st.write("# Previsões")
plot_predict(current_week_dates, current_week_prices,
             next_week_dates, next_week_predictions)

# Analise Pri
# Atribuir o dataframe a uma nova variável dfp
dfp = df

# Convertendo a coluna 'Data' para o tipo datetime
dfp['Data'] = pd.to_datetime(dfp['Data'])

# Extraindo o ano da coluna 'Data'
dfp['Ano'] = dfp['Data'].dt.year

# Agrupando os dados por ano e calculando a média dos preços
preco_anual = dfp.groupby('Ano')['Preco'].mean()

#Variações Anuais do Preço do Petróleo Brent

st.write("# Variações Anuais do Preço do Petróleo Brent")

# Convertendo a coluna 'Data' para o tipo datetime
df['Data'] = pd.to_datetime(df['Data'])

# Extraindo o ano da coluna 'Data'
df['Ano'] = df['Data'].dt.year

# Agrupando os dados por ano e calculando a média dos preços
preco_anual = df.groupby('Ano')['Preco'].mean()

# Criando o gráfico de barras
fig = go.Figure()

fig.add_trace(go.Bar(
    x=preco_anual.index,
    y=preco_anual.values,
    text=[round(value, 2) for value in preco_anual.values],
    textposition='outside',
    textangle=45  # Inclinação do texto
))

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)

# Convertendo a coluna 'Data' para o tipo datetime
dfp['Data'] = pd.to_datetime(dfp['Data'])

# Extraindo o ano da coluna 'Data'
dfp['Ano'] = dfp['Data'].dt.year

# Filtrando os dados para incluir apenas o ano de 2011
dados_2011 = dfp[dfp['Ano'] == 2011]

# Extraindo o mês da coluna 'Data'
dados_2011['Mês'] = dados_2011['Data'].dt.month

# Calculando a média mensal dos preços
media_mensal_2011 = dados_2011.groupby('Mês')['Preco'].mean()

# Criando o gráfico de barras
fig = go.Figure()

fig.add_trace(go.Bar(
    x=media_mensal_2011.index,
    y=media_mensal_2011.values,
    text=[round(value, 2) for value in media_mensal_2011.values],
    textposition='outside',
    marker_color='skyblue'
))

# Adicionando título e rótulos
fig.update_layout(
    title='Média Mensal do Preço do Petróleo Brent em 2011',
    xaxis_title='Mês',
    yaxis_title='Preço Médio',
    xaxis=dict(tickmode='linear'),
    xaxis_tickangle=45  # Rotacionando os rótulos do eixo x para melhor legibilidade
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)

# Analise Pri

texto = """
Em 2011, o preço do petróleo Brent atingiu um máximo de 99,20 dólares por barril.
O aumento foi causado por fatores como o alívio em relação às contas dos Estados Unidos,
a fraqueza do dólar e as expectativas de um crescimento mais forte liderado pela China.

<a href="https://www.terra.com.br/economia/pesquisa-preco-do-petroleo-fica-acima-de-us-90-em-2011,d09fd0d6796ea310VgnCLD200000bbcceb0aRCRD.html#:~:text=O%20petr%C3%B3leo%20Brent%20subiu%20a%20US$%2099%2C20,crescimento%20mais%20forte%20liderado%20por%20China%20e">Fonte de informação</a>
"""

st.write(texto, unsafe_allow_html=True)

texto = """
Em 2015, o preço do barril de petróleo Brent fechou a 31 de dezembro a 37,10 dólares, o que representa uma queda anual de 34,7% em relação ao preço de 56,82 dólares em 2014. No entanto, em maio de 2015, o barril de Brent atingiu a sua máxima do ano, a 69,63 dólares.

<a href="https://exame.com/invest/mercados/barril-do-brent-encerra-2015-com-queda-anual-de-34-7/">Fonte de informação</a>
"""

st.write(texto, unsafe_allow_html=True)

# Atribuir o dataframe a uma nova variável dfp
dfp = df

# Convertendo a coluna 'Data' para o tipo datetime
dfp['Data'] = pd.to_datetime(dfp['Data'])

# Extraindo o ano da coluna 'Data'
dfp['Ano'] = dfp['Data'].dt.year

# Calcular a média do preço do petróleo para cada mês ao longo dos anos
dfp['Mês'] = dfp['Data'].dt.month
media_por_mes = dfp.groupby('Mês')['Preco'].mean()

# Criando o gráfico de linha
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=media_por_mes.index,
    y=media_por_mes.values,
    mode='lines+markers',
    line=dict(color='green'),
    marker=dict(symbol='circle', size=8),
    name='Preço Médio Mensal'
))

# Configurando o layout
fig.update_layout(
    title='Média do Preço do Petróleo por Mês',
    xaxis_title='Mês',
    yaxis_title='Preço em Dólar',
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                  'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    )
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)

# Analise Pri
# Atribuir o dataframe a uma nova variável dfp
dfp = df

# Convertendo a coluna 'Data' para o tipo datetime
dfp['Data'] = pd.to_datetime(dfp['Data'])

# Extraindo o ano da coluna 'Data'
dfp['Ano'] = dfp['Data'].dt.year

# Calcular a média do preço do petróleo para cada ano
media_por_ano = dfp.groupby('Ano').mean()['Preco']

# ANO 2016

st.write("# Análise ano 2016")

# Pegando ano de 2016
dados_2016 = dfp[dfp['Ano'] == 2016]
dados_2016.reset_index(inplace=True)
# Pegando meses da coluna de Data
dados_2016['Mes'] = dados_2016['Data'].dt.month

# Media mensal
media_mensal_2016 = dados_2016.groupby('Mes')['Preco'].mean()

ano2016 = go.Figure()

ano2016.add_trace(go.Scatter(
    x=dados_2016['Preco'].index,
    y=media_mensal_2016.values,
    mode='lines+markers',
    name='Média 2016'
))

# Adicionando título e rótulos
ano2016.update_layout(
    title='Média mensal do preço do petróleo brent no ano de 2016',
    xaxis_title='Ano',
    yaxis_title='Preço Médio',
    xaxis=dict(tickmode='linear')
)

st.plotly_chart(ano2016, use_container_width=True)

st.write("Anuário estatístico: https://www.gov.br/anp/pt-br/centrais-de-conteudo/publicacoes/anuario-estatistico/anuario-estatistico-2016 --/-- Petróleo abaixo de 50 dólares: https://g1.globo.com/economia/mercados/noticia/2016/10/petroleo-segue-abaixo-de-us-50-ha-mais-de-1-ano-veja-impactos.html")

# ANO 2020

st.write("# Análise ano 2020")

# Pegando ano de 2020
dados_2020 = df[df['Ano'] == 2020]
dados_2020.reset_index(inplace=True)

# Pegando meses da coluna de Data
dados_2020['Mes'] = dados_2020['Data'].dt.month

# Media mensal
media_mensal_2020 = dados_2020.groupby('Mes')['Preco'].mean()

ano2020 = go.Figure()

ano2020.add_trace(go.Scatter(
    x=media_mensal_2020.index,
    y=dados_2020['Preco'].values,
    mode='lines+markers',
    name='Média 2020'
))

# Adicionando título e rótulos
ano2020.update_layout(
    title='Média mensal do preço do petróleo brent no ano de 2020',
    xaxis_title='Ano',
    yaxis_title='Preço Médio',
    xaxis=dict(tickmode='linear')
)

st.plotly_chart(ano2020, use_container_width=True)

# JUSTIFICATIVA st.write("## Mês de abril, primeiro indice negativo: https://g1.globo.com/economia/noticia/2020/04/20/preco-do-petroleo-americano-despenca-quase-40percent-e-vai-abaixo-de-us-12-o-barril.ghtml --/-- Análise 2020: https://einvestidor.estadao.com.br/investimentos/preco-petroleo-2020/#:~:text=O%20temor%20relacionado%20%C3%A0%20prov%C3%A1vel,25%20para%20US%2468%2C60.)

# ANO 2023

st.write("# Análise ano 2023")

# Pegando ano de 2020
dados_2023 = df[df['Ano'] == 2023]
dados_2023.reset_index(inplace=True)

# Pegando meses da coluna de Data
dados_2023['Mes'] = dados_2023['Data'].dt.month

# Media mensal
media_mensal_2023 = dados_2023.groupby('Mes')['Preco'].mean()

ano2023 = go.Figure()

ano2023.add_trace(go.Scatter(
    x=media_mensal_2023.index,
    y=dados_2023['Preco'].values,
    mode='lines+markers',
    name='Média 2020'
))

# Adicionando título e rótulos
ano2023.update_layout(
    title='Média mensal do preço do petróleo brent no ano de 2023',
    xaxis_title='Ano',
    yaxis_title='Preço Médio',
    xaxis=dict(tickmode='linear')
)

st.plotly_chart(ano2023, use_container_width=True)

# JUSTIFICATIVA st.write("## Geral GOV: https://www.gov.br/anp/pt-br/canais_atendimento/imprensa/noticias-comunicados/reservas-provadas-de-petroleo-no-brasil-crescem-7-em-2023#:~:text=Em%202023%2C%20houve%20aumento%20de,prov%C3%A1veis%20e%20poss%C3%ADveis%20(3P). --/-- Highlights: https://agenciabrasil.ebc.com.br/economia/noticia/2024-02/producao-media-de-petroleo-e-gas-bate-recorde-em-2023-informa-anp)

# Convertendo a coluna 'Data' para o tipo datetime
dfp.set_index('Data', inplace=True)

# Decompor a série temporal
decomposicao = seasonal_decompose(dfp['Preco'], model='additive', period=12)

# Criar figuras individuais para cada componente da decomposição
fig_observed = go.Scatter(
    x=dfp.index, y=decomposicao.observed, mode='lines', name='Observado')
fig_trend = go.Scatter(x=dfp.index, y=decomposicao.trend,
                       mode='lines', name='Tendência')
fig_seasonal = go.Scatter(x=dfp.index, y=decomposicao.seasonal,
                          mode='lines', name='Sazonalidade')
fig_residual = go.Scatter(x=dfp.index, y=decomposicao.resid,
                          mode='lines', name='Resíduo')

# Criar o subplot
fig = go.Figure()

fig.add_trace(fig_observed)
fig.add_trace(fig_trend)
fig.add_trace(fig_seasonal)
fig.add_trace(fig_residual)

# Configurar o layout
fig.update_layout(
    title='Decomposição da Série Temporal',
    xaxis_title='Data',
    yaxis_title='Preço',
    xaxis=dict(tickmode='auto', tickformat='%Y-%m')
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)

st.write("Utilizamos a decomposição de séries temporais para entender o que compõem a série e como eles contribuem para suas variações ao longo do tempo. Ela foi útil para identificarmos padrões e tendências em dados temporais. Remover efeitos sazonais para análise de tendências de longo prazo." 
         
"Avaliar a eficácia de modelos de previsão e detecção de anomalias e apoiar a tomada de decisões. O gráfico foi valioso para entender a estrutura e o comportamento de dados temporais.")