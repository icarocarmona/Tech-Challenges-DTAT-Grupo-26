import pandas as pd

# Carregar o arquivo CSV
url = "https://raw.githubusercontent.com/icarocarmona/Tech-Challenges-DTAT-Grupo-26/main/F4-DATA-VIZ-PRODUCTION-MODELS/petroleo_bruto.csv"
df = pd.read_csv(url)

# Verificar as primeiras linhas do dataframe
print(df.head())

# Verificar informações sobre o dataframe
print(df.info())

# Estatísticas descritivas básicas
print(df.describe())

# Verificar se há valores nulos
print(df.isnull().sum())
