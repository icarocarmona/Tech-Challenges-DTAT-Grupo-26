import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import joblib
import numpy as np
import plotly.express as px

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
