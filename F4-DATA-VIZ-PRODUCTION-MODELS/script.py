import requests
from bs4 import BeautifulSoup
import pandas as pd

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
df = pd.DataFrame(data, columns=['Data', 'Preço - petróleo bruto - Brent (FOB)'])
df = df.drop(index=df.index[:2])

df = df.reset_index(drop=True)
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

print(df.head())
df.to_csv('./petroleo_bruto.csv', sep=',', index=False, encoding='utf-8')
