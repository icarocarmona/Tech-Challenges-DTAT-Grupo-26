import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from tensorflow.keras.layers import LSTM, Dense, Reshape
from tensorflow.keras.models import Sequential
import plotly.graph_objs as go

import plotly.express as px
import yfinance as yf

import streamlit as st

sns.set(style='whitegrid', palette='muted', font_scale=1.5)

rcParams['figure.figsize'] = 14, 8

RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

symbol = '^BVSP'
start_date = '2018-01-01'
end_date = '2024-01-31'

bvsp_full = yf.download(symbol, start=start_date, end=end_date)

"""# Analise exploratoria"""

bvsp_full.head(2)

st.line_chart(bvsp_full['Adj Close'])

"""Possível motivo: https://veja.abril.com.br/economia/guerra-comercial-entre-china-e-eua-faz-bolsa-cair-25-e-dolar-subir-17

No grafico acima é possivel visualizar as oscilações da Bolsa de valores em 2018 Guerra Comercial EUA-China. A escalada das tensões comerciais entre os Estados Unidos e a China teve um impacto significativo nos mercados globais, causando volatilidade nas bolsas. Em janeiro de 2019, as negociações comerciais entre os EUA e a China mostraram progresso, aliviando parte da tensão e impulsionando os mercados.
Pandemia de COVID-19: A crise sanitária global começou a afetar os mercados em fevereiro de 2020, levando a quedas acentuadas nas bolsas de valores em todo o mundo.

Possível motivo: https://valorinveste.globo.com/objetivo/hora-de-investir/noticia/2020/03/31/ibovespa-tem-maior-queda-mensal-em-22-anos-dolar-maior-alta-desde-ataque-as-torres-gemeas-em-2011.ghtml
Em 2020 Colapso do Mercado de Ações se inicia em março. A pandemia de COVID-19 levou a uma venda generalizada de ativos, com grandes quedas nos principais índices de ações. Para combater os impactos econômicos da pandemia, bancos centrais ao redor do mundo implementaram políticas de afrouxamento monetário e estímulos econômicos. Após as quedas iniciais, os mercados começaram a se recuperar rapidamente, impulsionados por medidas de estímulo e otimismo em relação ao desenvolvimento de vacinas contra a COVID-19.
Os mercados continuaram a se recuperar em 2021, à medida que a vacinação contra a COVID-19 avançava e as perspectivas econômicas melhoravam.

Possível motivo: https://valorinveste.globo.com/mercados/renda-variavel/bolsas-e-indices/noticia/2022/12/31/retrospectiva-da-bolsa-em-2022-veja-mes-a-mes-o-sobe-e-desce-que-rendeu-5percent.ghtml
Em 2022 foi um ano de altos e baixos. De acordo com o Valor Investe, o Ibovespa teve um crescimento de 5% no ano, apesar de ter passado por uma queda de 19% em junho de 2022.

Preocupações com a inflação e as mudanças nas políticas monetárias dos bancos centrais influenciaram a volatilidade em alguns momentos.
Empresas de tecnologia continuaram a desempenhar um papel importante nas oscilações do mercado, com investidores atentos a notícias e eventos relacionados a essas empresas.
"""

""" analisar apenas 2022 em diante"""

df = bvsp_full.loc[(bvsp_full.index >= '2023-01-01') &
                   (bvsp_full.index < '2024-01-12')]

st.line_chart(df['Adj Close'])

"""# analisando período jan-2023 até jan-2024"""


symbol = '^BVSP'
start_date = '2023-01-01'
end_date = '2024-01-16'

df = yf.download(symbol, start=start_date, end=end_date)

# cópia do dataframe
df_limpo = df
df_limpo.reset_index(inplace=True)
# transformando em datetime
df_limpo['Date'] = pd.to_datetime(df_limpo['Date'])
# Removendo colunas desnecessárias
df_limpo = df.drop(columns=['Open', 'High', 'Low', 'Volume', 'Close'])
# definindo data como índice
df_limpo = df_limpo.set_index('Date')

"""# Relação Date x Open"""

fig = plt.figure(figsize=(15, 10))
plt.plot(df['Date'], df['Open'], label='BVSP')

st.pyplot(fig)

"""# Detalhando períodos de queda aparente

# Maior pico de queda aparente aconnteceu entre 2023-03 e 2023-05"""

periodo1 = (df['Date'] >= '2023-03-01') & (df['Date'] <= '2023-05-01')

df_periodo1 = df[periodo1]

fig = plt.figure(figsize=(15, 10))
plt.plot(df_periodo1['Date'], df_periodo1['Open'], label='BVSP')

st.pyplot(fig)
