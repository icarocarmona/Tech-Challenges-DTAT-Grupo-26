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

st.dataframe(df)


st.write("# Previsões")
plot_predict(current_week_dates, current_week_prices, next_week_dates, next_week_predictions)

## Analise Pri

## Analise Pri
# Atribuir o dataframe a uma nova variável dfp
dfp = df

# Convertendo a coluna 'Data' para o tipo datetime
dfp['Data'] = pd.to_datetime(dfp['Data'])

# Extraindo o ano da coluna 'Data'
dfp['Ano'] = dfp['Data'].dt.year

# Agrupando os dados por ano e calculando a média dos preços
preco_anual = dfp.groupby('Ano')['Preco'].mean()

# Criando o gráfico de linha
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=preco_anual.index,
    y=preco_anual.values,
    mode='lines+markers',
    name='Preço Médio Anual'
))

# Adicionando título e rótulos
fig.update_layout(
    title='Variações Anuais do Preço do Petróleo Brent',
    xaxis_title='Ano',
    yaxis_title='Preço Médio',
    xaxis=dict(tickmode='linear')
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)

# Criando o gráfico de barras
fig = go.Figure()

fig.add_trace(go.Bar(
    x=preco_anual.index,
    y=preco_anual.values,
    text=[round(value, 2) for value in preco_anual.values],
    textposition='outside',
    textangle=45  # Inclinação do texto
))

# Adicionando título e rótulos
fig.update_layout(
    title='Variações Anuais do Preço do Petróleo Brent',
    xaxis_title='Ano',
    yaxis_title='Preço Médio',
    xaxis=dict(tickmode='linear')
)

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

## Analise Pri

#import streamlit as st

import streamlit as st

texto = """
Em 2011, o preço do petróleo Brent atingiu um máximo de 99,20 dólares por barril. 
O aumento foi causado por fatores como o alívio em relação às contas dos Estados Unidos, 
a fraqueza do dólar e as expectativas de um crescimento mais forte liderado pela China.

<a href="https://www.terra.com.br/economia/pesquisa-preco-do-petroleo-fica-acima-de-us-90-em-2011,d09fd0d6796ea310VgnCLD200000bbcceb0aRCRD.html#:~:text=O%20petr%C3%B3leo%20Brent%20subiu%20a%20US$%2099%2C20,crescimento%20mais%20forte%20liderado%20por%20China%20e">Fonte de informação</a>
"""

st.write(texto, unsafe_allow_html=True)

import streamlit as st

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
        ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    )
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)

## Analise Pri
# Atribuir o dataframe a uma nova variável dfp
dfp = df

# Convertendo a coluna 'Data' para o tipo datetime
dfp['Data'] = pd.to_datetime(dfp['Data'])

# Extraindo o ano da coluna 'Data'
dfp['Ano'] = dfp['Data'].dt.year

# Calcular a média do preço do petróleo para cada ano
media_por_ano = dfp.groupby('Ano').mean()['Preco']

# Criando o gráfico de linha
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=media_por_ano.index,
    y=media_por_ano.values,
    mode='lines+markers',
    line=dict(color='orange'),
    marker=dict(symbol='circle', size=8),
    name='Preço Médio Anual'
))

# Configurando o layout
fig.update_layout(
    title='Média do Preço do Petróleo por Ano',
    xaxis_title='Ano',
    yaxis_title='Preço em Dólar',
    xaxis=dict(tickmode='linear'),
    yaxis=dict(tickformat=".2f")
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)

df = load_dataset()
dfp = df.copy()

# Convertendo a coluna 'Data' para o tipo datetime
dfp['Data'] = pd.to_datetime(dfp['Data'])
dfp.set_index('Data', inplace=True)

# Decompor a série temporal
decomposicao = seasonal_decompose(dfp['Preco'], model='additive', period=12)

# Criar figuras individuais para cada componente da decomposição
fig_observed = go.Scatter(x=dfp.index, y=decomposicao.observed, mode='lines', name='Observado')
fig_trend = go.Scatter(x=dfp.index, y=decomposicao.trend, mode='lines', name='Tendência')
fig_seasonal = go.Scatter(x=dfp.index, y=decomposicao.seasonal, mode='lines', name='Sazonalidade')
fig_residual = go.Scatter(x=dfp.index, y=decomposicao.resid, mode='lines', name='Resíduo')

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