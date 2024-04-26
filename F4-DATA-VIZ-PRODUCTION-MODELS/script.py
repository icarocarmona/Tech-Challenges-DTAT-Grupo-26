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
print(df.head())
df.to_csv('./petroleo_bruto.csv')
