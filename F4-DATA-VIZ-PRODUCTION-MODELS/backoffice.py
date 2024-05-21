import boto3
import pickle
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from io import BytesIO

st.set_page_config(
    page_title="🚀 BackOffice 🧑‍🚀 | Tech Challenge - Grupo 26",
    page_icon="🚀",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://github.com/icarocarmona/Tech-Challenges-DTAT-Grupo-26/issues",
        'About': "# Este projeto faz parte de uma das entregas da Pós-Tech em Data Analytics."
    }

)

st.header('🚀 BackOffice 🧑‍🚀| Tech Challege - Grupo 26', divider='rainbow')


@st.cache_data
def load_dataset():
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    dados_csv = response['Body'].read()
    df = pd.read_csv(BytesIO(dados_csv))
    return df


# Suas credenciais AWS
aws_access_key_id = st.secrets["aws_access_key_id"]
aws_secret_access_key = st.secrets["aws_secret_access_key"]
bucket_name = 'modelo-postech'
object_key = 'petroleo_bruto.csv'
object_key_model = 'modelo.pkl'

# Crie uma sessão no boto3
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Crie um cliente S3
s3 = session.client('s3')
csv_data = None


@st.cache_data
def load_dataset():
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    dados_csv = response['Body'].read()
    df = pd.read_csv(BytesIO(dados_csv))
    return df


st.write("## Atualizar Dados na Nuvem")
st.write("Ao clicar, os dados serão coletados automaticamente do site e enviados para a AWS")
if st.button("Coletar e Atualizar Dados"):
    # URL da página
    url = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view'

    # Fazendo o download da página
    response = requests.get(url)
    html = response.content

    # Parseando o HTML com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Encontrando a tabela na página
    table = soup.find('table', {'class': 'dxgvControl'})

    # Extraindo os dados da tabela
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            data.append([cols[0].text.strip(), cols[1].text.strip()])

    # Criando um DataFrame com os dados extraídos
    df = pd.DataFrame(
        data, columns=['Data', 'Preço - petróleo bruto - Brent (FOB)'])
    df = df.drop(index=df.index[:2])

    df = df.reset_index(drop=True)
    # Alterando o nome da segunda coluna
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

    st.write("Dados coletados do site do ipeadata")
    st.write(df.tail())

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue().encode('utf-8')

    # Fazer upload do arquivo CSV para o S3
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=csv_data)
    st.write("DataFrame salvo como arquivo CSV no S3 com sucesso!")
    st.balloons()


st.write("## Atualizar Modelo")
st.write("Ao clicar no botão abaixo o modelo será retreinado e enviado para a AWS")
if st.button("Retreinar Modelo"):
    df = load_dataset()
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
    df = df.sort_values(by='Data', ascending=True).reset_index(drop=True)

    # É uma boa prática criar recursos de atraso (lag features) para séries temporais
    # Vamos criar alguns para nosso modelo
    # Criar recursos de atraso (lag features)
    lags = 7
    for lag in range(1, lags + 1):
        df[f'Preco_lag_{lag}'] = df['Preco'].shift(lag)

    # Removemos quaisquer linhas com valores NaN que foram criados ao fazer o shift
    df = df.dropna()

    # Preparando os dados para treinamento
    X = df[['Preco_lag_1']].values  # Inputs são os preços atrasados
    y = df['Preco'].values  # Output é o preço atual

    # Dividir os dados em conjuntos de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, shuffle=False)

    # Criar e treinar o modelo de Gradient Boosting
    # model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42, loss='squared_error')

    model = GradientBoostingRegressor(
        n_estimators=300, learning_rate=0.1, max_depth=5, random_state=42, loss='squared_error')

    model.fit(X_train, y_train)

    # Salvar o modelo
    # model = joblib.dump(model, 'modelo.pkl')
    model_data = pickle.dumps(model)

    # Fazer previsões
    predictions = model.predict(X_test)

    # Avaliar o modelo
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    st.write(f"Mean Squared Error: {mse}")
    st.write(f"Mean Absolute Error: {mae}")

    # Calculando o R^2
    r2 = r2_score(y_test, predictions)
    st.write(f"Coeficiente de Determinação (R^2): {r2}")

    # Fazer previsões para a próxima semana usando os últimos dados conhecidos
    last_known_data = X[-1].reshape(1, -1)
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

    for week, pred in zip(next_week_dates, next_week_predictions):
        st.write(f'{week}: {pred:.2f}')

    # Fazer upload do arquivo CSV para o S3
    s3.put_object(Bucket=bucket_name, Key=object_key_model, Body=model_data)
    st.write("Modelo atualizado no S3 com sucesso!")
    st.balloons()
