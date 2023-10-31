import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import locale
import plotly.express as px

from streamlit.delta_generator import DeltaGenerator

tipo_de_vinho = 'Vinho De Mesa'

st.set_page_config(
    page_title="Tech Challenge - Grupo 26",
    page_icon="🍷",
    # layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_dados_de_vinhos():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/icarocarmona/tech_challenge_f1/main/dados/trusted/dados_de_vinhos.csv", sep=";")
    # filtra apenas vinho de mesa
    dados = df[df['Tipo Vinho'] == tipo_de_vinho]
    # .reset_index(drop=True)
    dados['Vl Litro'] = dados['Valor U$'] / dados['Quantidade (L)']
    return dados


@st.cache_data
def load_dados_producao():
    return pd.read_csv(
        'https://raw.githubusercontent.com/icarocarmona/tech_challenge_f1/main/dados/raw/Producao.csv', sep=';')


@st.cache_data
def load_dados_com_pais(df_filtrado):
    country = pd.read_csv(
        'https://raw.githubusercontent.com/icarocarmona/tech_challenge_f1/main/dados/raw/countries-with-regional-codes.csv')
    paises = pd.read_csv(
        'https://raw.githubusercontent.com/icarocarmona/tech_challenge_f1/main/dados/raw/pais.csv', encoding='latin-1', sep=';')

    df_sem_zero = df_filtrado[df_filtrado['Quantidade (L)'] > 0]
    df_sem_zero.loc[df_sem_zero['Destino'] == 'Países Baixos',
                    'Destino'] = 'Países Baixos (Holanda)'

    df_completo = df_sem_zero.merge(
        paises, left_on='Destino', right_on='NO_PAIS', how='left')
    df_completo = df_completo.merge(
        country, left_on='CO_PAIS_ISON3', right_on='country-code', how='left')

    return df_completo

# Função para formatar os rótulos do eixo Y em unidades legíveis

def fontes_referencia():
    st.write("### Fontes de pesquisas:")
    st.write("- A história do vinho no Brasil. Blog Cervejaria Leopondina. Disponível em: <https://blog.famigliavalduga.com.br/a-historia-do-vinho-no-brasil-conheca-a-trajetoria-da-bebida-em-territorio-nacional/>")
    st.write("- Cresce exportação de vinho brasileiro. Jornal O Tempo. Disponível em<https://www.otempo.com.br/economia/cresce-exportacao-de-vinho-brasileiro-1.270988>")
    st.write("- No copo dos estrangeiros. Jornal do Vinho. Disponível em: <https://www.jornaldovinho.com.br/novo/no-copo-dos-estrangeiros/>")
    st.write("- Exportação de vinho brasileiro bate recorde de janeiro a setembro de 2021. CNN BRasil. Disponível em: <https://www.cnnbrasil.com.br/economia/exportacao-de-vinho-brasileiro-bate-recorde-de-janeiro-a-setembro-de-2021/>")

def format_millions(value, pos):
    if value >= 1e3 and value < 1e6:
        value = value / 1e3
        return f'{value:.0f}k'
    if value >= 1e6 and value < 1e7:
        value = value / 1e6
        return f'{value:.0f}M'
    if value > 1e7:
        value = value / 1e7
        return f'{value:.0f}B'
    return f'{value:.0f}'


def top10_paises(dados: pd.DataFrame, tab: DeltaGenerator):

    df = dados[dados['Ano'].between(*user_num_input)]
    top_10_paises = df.groupby(by='Destino')['Valor U$'].sum(
    ).sort_values(ascending=False).head(10).index
    vinhos_de_mesa_filtrado = df[dados['Destino'].isin(top_10_paises)]
    vinhos_de_mesa_filtrado = vinhos_de_mesa_filtrado[vinhos_de_mesa_filtrado['Valor U$'] > 0]

    fig = plt.figure(figsize=(10, 4))
    sns.set_theme(style='dark')
    sns.lineplot(data=vinhos_de_mesa_filtrado,
                 x='Ano', y='Valor U$', hue='Destino')
    tab.pyplot(fig)

    fig2 = plt.figure(figsize=(10, 4))
    sns.lineplot(data=vinhos_de_mesa_filtrado, x='Ano',
                 y='Valor U$', hue='Tipo Vinho')
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


def producao_de_vinho():

    tabela = load_dados_producao()

    # Suponhamos que você tenha um DataFrame chamado "tabela" com os dados
    # Vamos usar o método "melt" para reorganizar a tabela

    # Primeiro, crie uma lista de anos das colunas da tabela
    anos = [str(ano) for ano in range(1970, 2023)]

    # Use o método "melt" para transformar a tabela
    tabela_melted = tabela.melt(id_vars=[
                                "id", "produto"], value_vars=anos, var_name="Ano", value_name="Quantidade (L)")

    # Suponhamos que você tenha uma tabela_melted com os dados reorganizados

    # Filtrar linhas para "Vinho de Mesa" e "Rosado"
    produtos_desejados = tabela_melted[tabela_melted['produto'].isin(
        ["VINHO DE MESA", "VINHO FINO DE MESA (VINÍFERA)"])]

    # Filtrar apenas os 15 anos mais recentes
    anos_recentes = [str(ano) for ano in range(2017, 2022)]  # 2018 a 2022
    produtos_desejados = produtos_desejados[produtos_desejados['Ano'].isin(
        anos_recentes)]

    # Normalizar as quantidades (dividir por 1.000)
    produtos_desejados.loc[:,
                           'Quantidade (L)'] = produtos_desejados['Quantidade (L)'] / 1000

    # Criar o gráfico de barras empilhadas
    fig = plt.figure(figsize=(18, 8))
    sns.set(style="whitegrid")
    ax = sns.barplot(data=produtos_desejados, x="Ano",
                     y="Quantidade (L)", hue="produto")

    # Adicionar rótulos de dados nas barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}K', (p.get_x(
        ) + p.get_width() / 2., p.get_height()), ha='center', va='bottom')

    plt.title(
        "Quantidade de litros produzidos nos últimos 15 Anos para Vinho de Mesa e VINHO FINO DE MESA (VINÍFERA")
    plt.xlabel("Ano")
    plt.ylabel("Quantidade (milhares de litros)")
    plt.xticks(rotation=45)
    plt.legend(title="Produto")

    st.pyplot(fig)


st.write('# Tech challenge')
# carregando os dados
df = load_dados_de_vinhos()
tab_home, tab_historico, tab_dados = st.tabs(
    ["🎯 Home", "📈 Análise", "🗃 Data"])


with tab_dados:
    paises = df['Destino'].unique()
    anos = df['Ano'].unique()

    options_paises = st.multiselect('Escolha um ou mais países', paises)
    options_anos = st.multiselect('Escolha um ou mais anos', anos)

    if not options_paises and not options_anos:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        # Crie um DataFrame filtrado com base nas seleções
        filtered_df = df[df['Destino'].isin(
            options_paises) & df['Ano'].isin(options_anos)]
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)


# Montando o filtro de ano
_min = 1970
_max = 2022
# user_num_input = tab2.slider("Filtro de ano", min_value=_min,
#                     max_value=_max,
#                     value=(_min, _max),
# )

# top10_paises(df, tab2)
# agg_ano(df, tab2)


### HOME ###
with tab_home:
    st.write("Este projeto é a entrega do desafio tecnológico da fase 1 de análise de dados e exploração. Nele, realizamos uma análise dos dados de exportação de vinho do Brasil, com foco especial no estado do Rio Grande do Sul.")

    st.write("### Integrantes do Grupo 26")

    df_home = pd.DataFrame({
        "Nome": ["Beatriz Vieira", "Icaro Carmona", "Priscila de França"],
        "linkedin": ["https://www.linkedin.com/in/beatrizrvieira/", "https://www.linkedin.com/in/icarocarmona/", "https://www.linkedin.com/in/pridefranca/"],
    })
    st.dataframe(df_home,
                 column_config={
                     "Nome": "Nome",
                     "linkedin": st.column_config.LinkColumn("Linkedin URL")
                 },
                 use_container_width=True,
                 hide_index=True,

                 )


def plot_qtd_vinho_mesa_exp_ano(df):
    sns.set(style="whitegrid")
    g = sns.catplot(data=df, x='Ano',
                    y='Quantidade (L)', kind='bar', height=6, aspect=2)
    g.fig.suptitle(f'Quantidade {tipo_de_vinho} Exportados por Ano', y=1.02)
    plt.xlabel('Ano')
    plt.ylabel('Quantidade (L)')

    # Rotacionar os rótulos dos anos para torná-los mais legíveis
    g.set_xticklabels(rotation=45)
    st.pyplot(g)


def format_value(valor):
    return locale.format_string('%d', valor, grouping=True)


def analise_1990_ate_2000():
    # df_filtrado = df[(df['Ano'] == 1999)][['Quantidade (L)','Valor U$']].sum()
    df = monta_dataframe_analise_90_00()
    filtro_1990 = df['Ano'] == 1990
    filtro_2000 = df['Ano'] == 2000

    valor_1990 = format_value(df[filtro_1990]['Soma de Valor U$'])
    qtd_1990 = format_value(df[filtro_1990]['Soma de Quantidade (L)'])

    col1, col2, col3 = st.columns(3)
    col1.metric("Ano", "1990")
    col2.metric("Quantidade (L)", f"{valor_1990}")
    col3.metric("Valor U$", f"$ {qtd_1990}")

    valor_2000 = format_value(df[filtro_2000]['Soma de Valor U$'])
    qtd_2000 = format_value(df[filtro_2000]['Soma de Quantidade (L)'])

    variacao_qtd = format_value(df[filtro_2000]['Variação Qtd Pct'])
    variacao_vl = format_value(df[filtro_2000]['Variação Vl Pct'])

    col1, col2, col3 = st.columns(3)
    col1.metric("Ano", "2000")
    col2.metric("Quantidade (L)", f"{qtd_2000}", variacao_qtd)
    col3.metric("Valor U$", f"$ {valor_2000}", variacao_vl)


def analise_1990_2000(df_filtrado):
    # Filtrar os anos desejados
    df_6_anos = df_filtrado[df_filtrado['Ano'].between(1990, 2000)]

    # Defina o tamanho da figura
    fig = plt.figure(figsize=(10, 4))

    # Crie o gráfico de linhas
    ax = sns.lineplot(data=df_6_anos, x='Ano', y='Valor U$', label='Valor U$')
    ax = sns.lineplot(data=df_6_anos, x='Ano',
                      y='Quantidade (L)', label='Quantidade (L)')

    # Defina rótulos e legendas
    plt.xlabel('Ano')
    plt.ylabel('Valores')
    plt.title('Gráfico de Linhas com Valor e Quantidade')
    plt.legend()

    st.pyplot(fig)


def monta_dataframe_analise_90_00():
    df_filtrado_2 = df[df['Ano'].isin([1990, 2000])]
    soma_valores = df_filtrado_2.groupby(
        'Ano')[['Quantidade (L)', 'Valor U$']].sum()
    df_soma_anos = soma_valores.reset_index()
    df_soma_anos.columns = [
        'Ano', 'Soma de Quantidade (L)', 'Soma de Valor U$']
    df_soma_anos['Variação Vl Pct'] = df_soma_anos['Soma de Valor U$'].pct_change() * \
        100
    df_soma_anos['Variação Qtd Pct'] = df_soma_anos['Soma de Quantidade (L)'].pct_change(
    ) * 100

    return df_soma_anos


def analise_por_regiao(df):

    df_completo = load_dados_com_pais(df)

    fig = px.scatter(df_completo, x='Ano', y="Quantidade (L)",
                     size='Valor U$', color='region',
                     hover_name="name", log_x=True, size_max=60)
    st.plotly_chart(fig, use_container_width=True)


def analise_ultimos_15_anos():
    anos = list(range(2007, 2023))

    df_15_anos = df[df['Ano'].isin(anos)]
    df_15_anos.index = df_15_anos.index.astype(int)
    df_15_anos_com_venda = df_15_anos[df_15_anos['Valor U$'] != 0]
    count_vendas = df_15_anos_com_venda.groupby('Ano')[['Destino']].count()

    st.bar_chart(count_vendas)

    # Defina o tamanho da figura
    # fig = plt.figure(figsize=(10, 4))
    # ax = sns.lineplot(data=df_15_anos, x='Ano',
    #                   y='Valor U$', label='Quantidade')
    # ax = sns.lineplot(data=df_15_anos, x='Ano',
    #                   y='Quantidade (L)', label='Quantidade (L)')

    # # Defina rótulos e legendas
    # plt.xlabel('Ano')
    # plt.ylabel('Valores')
    # plt.title('Gráfico de Linhas com Valor e Quantidade')
    # plt.legend()

    # Exiba o gráfico
    # st.pyplot(fig)


def analise_mercosul(df):
    paises_mercosul = ["Brasil", "Argentina", "Uruguai", "Paraguai"]

    mercosul = df[df['Destino'].isin(paises_mercosul)]
    # mercosul = mercosul.set_index('Ano')
    # mercosul.index = mercosul.index.astype(int)

    fig = px.line(mercosul.query("Ano>=2012"),
                  x="Ano", y="Valor U$", color='Destino')

    # fig.update_layout(title_text="Mercosul")

    st.plotly_chart(fig, use_container_width=True)


def plotbar(df, y_column='Valor U$'):
    # sns.set_theme(style='dark')
    sns.set(style='whitegrid')
    # sns.set_palette("Set2")

    # Defina o tamanho da figura
    fig = plt.figure(figsize=(15, 4))

    # Crie o gráfico de barras
    ax = sns.barplot(data=df, x="Ano", y=y_column, hue='Destino')

    # Calcule a média e a mediana
    media = df[y_column].mean()
    mediana = df[y_column].median()

    # Adiciona linhas representando a média e a mediana no gráfico
    plt.axhline(media, color='r', linestyle='--',
                label=f'Média ({format_millions(media,0)} U$)')
    plt.axhline(mediana, color='g', linestyle='--',
                label=f'Mediana ({format_millions(mediana,0)} U$)')

    # Adiciona formatação nos valores
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_millions))

    # Ajuste os rótulos do eixo x manualmente
    # ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df['Ano'].unique(), rotation=45)

    # Adicione uma legenda
    plt.legend()

    # Exiba o gráfico
    st.pyplot(fig)


def analise_geral_10_anos(df):
    fig = px.line(df.query("Ano>=2012"),
                  x="Ano", y="Valor U$", color='Destino')

    st.plotly_chart(fig, use_container_width=True)


def analise_paraguai(df):
    rows_with_zeros = (df == 0).any(axis=1)
    df2 = df[~rows_with_zeros]
    df2 = df2[df2['Destino'] == 'Paraguai']

    df2['Variação Percentual'] = df2['Valor U$'].pct_change() * 100

    df2['Variação Percentual'] = df2['Variação Percentual'].fillna(0)
    # Formate os valores com duas casas decimais
    df2['Variação Percentual'] = df2['Variação Percentual'].round(2)

    cascata = df2.iloc[-10:]

    fig = go.Figure(go.Waterfall(
        x=cascata['Ano'],
        y=cascata['Variação Percentual'],
        text=cascata['Variação Percentual'],
        textposition="outside",
    ))

    fig.update_layout(
        title="Exportação para o Paraguai nos ulitmos 10 anos",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)


def analise_2010_2021(df_filtrado):
    # Supondo que df_filtrado é o DataFrame original

    # Filtrar os anos desejados
    df_6_anos = df_filtrado[df_filtrado['Ano'].between(2010, 2021)]

    # Defina o tamanho da figura
    fig = plt.figure(figsize=(10, 4))

    # Crie o gráfico de linhas
    ax = sns.lineplot(data=df_6_anos, x='Ano', y='Valor U$', label='Valor U$')
    ax = sns.lineplot(data=df_6_anos, x='Ano',
                      y='Quantidade (L)', label='Quantidade (L)')

    # Defina rótulos e legendas
    plt.xlabel('Ano')
    plt.ylabel('Valores')
    plt.title('Gráfico de Linhas com Valor e Quantidade')
    plt.legend()

    st.pyplot(fig)


def conclusao(df):
    recomendacao = list(['Uruguai', 'Paraguai', 'China'])
    df_22 = df[df['Ano'] == 2022]

    total_venvido_22 = df_22['Valor U$'].sum()

    df_filtrado_22 = df_22[df_22['Destino'].isin(recomendacao)]
    total_venvido_pelos_3 = df_filtrado_22['Valor U$'].sum()

    percentagem = (total_venvido_pelos_3 / total_venvido_22) * 100

    st.write("## Conclusão")
    st.write(
        f"""
        Com base nos dados e comparações apresentadas, sugerimos futuros investimentos na China, Paraguai e Uruguai. 

        China e Paraguai já são países já consolidados no mercado de importação de vinhos brasileiros, visando acordos futuros Paraguai continuará sendo um dos principais importadores, temas fiscais e de tributação são favoráveis para continuar e aumentar a facilitação na exportação/importação.

        Visando expansão de mercado, Uruguai é um dos países que mais obtém destaque para o futuro. Com um dado analisado de 2022 vimos que China, Paraguai e Uruguai representam {percentagem:.2f}% da venda total de exportações de vinho do Brasil, tendo uma crescente nos últimos dois anos. Um dos pontos de atenção positiva é que o Uruguai também faz parte do Mercosul, onde acordos tributários e de cooperação são bastante discutidos e visados por ambos os países.

        Sobre os investimentos na China, este ano tivemos a notícia que 15 acordos foram assinados para fomentar a cooperação entre Brasil e China, áreas como pesquisa e educação, comunicação e principalmente comércio estão contemplados. Os acordos trazem uma novidade na economia que ajudará a facilitar as transações. As negociações diretas poderão ser feitas sem precisar do dólar, o que tornaria as operações mais baratas e vantajosas para investidores.
        """)


with tab_historico:
    # locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Isso define o formato para dólares americanos, ajuste conforme necessário

    st.write("# A história da exportação do vinho no Brasil:")
    st.write("""
            Entre 1970 e 2021, a exportação de vinhos brasileiros cresceu consideravelmente. Inicialmente, a presença no mercado global era limitada. Nas décadas de 1970 e 1980, os vinhos brasileiros enfrentaram dificuldades para competir com os tradicionais da Europa e América do Sul, devido ao desenvolvimento incipiente em qualidade, tecnologia e reputação.
        """)

    # Crie um gráfico usando Seaborn catplot
    plot_qtd_vinho_mesa_exp_ano(df)

    st.write("""
    A partir dos anos 1990 e 2000, houve avanços. O reconhecimento internacional cresceu, impulsionado pela melhoria na qualidade dos vinhos, investimentos em novas técnicas de vinificação e foco em variedades locais, especialmente na Serra Gaúcha, destacando-se na produção de espumantes.
    """)

    analise_1990_ate_2000()

    analise_1990_2000(df)

    st.write("""        
    Embora as exportações tenham sido modestas até meados dos anos 2000, houve um crescimento notável de 2010 a 2021. O Brasil expandiu sua presença em mercados estrangeiros, ampliando a diversidade de vinhos exportados, não se restringindo apenas a espumantes, mas incluindo variedades de tintos, brancos e rosés, principalmente para países como EUA, Reino Unido, China e Canadá.
    """)

    analise_2010_2021(df)

    st.write("""
        Apesar do crescimento, as exportações brasileiras de vinho ainda representam uma pequena parcela do mercado global, devido a desafios como competitividade de preços, barreiras comerciais e a consolidação de uma imagem de qualidade consistente. O Brasil observou um crescimento constante na exportação de vinhos ao longo do tempo, refletindo melhorias na qualidade e aceitação internacional, embora ainda esteja em processo de consolidação no mercado global de vinhos.
    """)

    # st.bar_chart(data=df_soma_anos, x="Ano", y=[
    #              "Soma de Valor U$", "Soma de Quantidade (L)"])

    st.write('A pauta de países compradores nos ultimos 15 anos também ampliou-se de 38 para 76, indicando que novos consumidores externos estão adquirindo e conhecendo o vinho brasileiro.')

    analise_ultimos_15_anos()

    st.write("""
    Foi constatado que o inverno de 2017 apresentou menos horas de frio, diminundo a emissão de brotos pelas uvas viníferas de estado. (IBRAVIN, 2018).

    Em 2019 a produção de uva no Rio Grande do Sul cai quase 40% frente a 2018, a redução foi causada, principalmente, pela queda de granizo que comprometeu parreirais em municípios da Serra Gaúcha.

    Já em em 2020 a exportação de vinho brasileiro bate recorde de janeiro a setembro de 2021, o vinho brasileiro foram comprados por 63 países entre janeiro e setembro de 2021. A taxa de aumento da produção de vinho foi de aproximadamente 38.7% de 2020 para 2021 e de cerca de 11.6% de 2021 para 2022.
    """)

    producao_de_vinho()

    st.write("No gráfico abaixo, podemos perceber que países da América têm uma representatividade maior a partir de 2015, liderados pelo Paraguai.")
    analise_por_regiao(df[(df['Ano'] >= 2007)])

    st.write("""
    O destaque de exportações para a Russia em 2013, é parcialmente atribuído às políticas do governo federal, como o Programa de Financiamento à Exportação (PEP), que ofereceu apoio, especialmente para exportações à Rússia, e ao programa Wine of Brasil.  No entanto, a partir de 2014, houve uma significativa redução nas exportações. Essa diminuição pode ter sido influenciada por uma série de fatores, incluindo mudanças nas políticas, variações na demanda externa, concorrência de outros mercados ou condições econômicas tanto no Brasil quanto nos países importadores.
    """)
    analise_geral_10_anos(df)

    st.write("""
    Podemos perceber que a China tem uma boa média, sendo consolidada como cliente recorrente. Ela tem sido afetada por problemas já descritos anteriormente nos últimos 15 anos. A China é um país importante para exportação devido à sua parceria e participação no BRICS.

    Segundo informações do governo brasileiro China é o principal parceiro comercial do Brasil, a China comprou 90% de toda a exportação brasileira destinada aos BRICS, cerca de US\$ 89.4 bilhões. A Índia importou 6,3% (cerca de US\$ 6,3 bilhões), a Rússia foi destino de 2% das exportações (US\$ 1,96 bilhão) e a África do Sul, de 1,7% (US\$ 1,7 bilhão). [Ref.](https://www.gov.br/planalto/pt-br/assuntos/reuniao-do-brics/historia-do-brics/#:~:text=Principal%20parceiro%20comercial%20do%20Brasil%2C%20a%20China%20comprou,%C3%81frica%20do%20Sul%2C%20de%201%2C7%25%20%28US%24%201%2C7%20bilh%C3%A3o%29.)
    """)
    plotbar(df[(df['Destino'] == 'China') & (df['Ano'] >= 2007)])

    st.write("""
    ### Mercosul
             
    Dentro do Mercosul, há acordos e políticas comerciais que visam facilitar o comércio entre os países membros, reduzindo ou eliminando tarifas alfandegárias em muitos produtos, principalmente o vinho.

    A isenção de impostos alfandegários no comércio de vinho entre os países do Mercosul pode representar uma vantagem competitiva para os produtores e exportadores em comparação com os produtores europeus. Essa isenção de tarifas pode resultar em custos menores para a importação e exportação de vinho entre os países membros, tornando os produtos do Mercosul mais competitivos no mercado interno dos países do bloco.
    """)
    analise_mercosul(df[(df['Ano'] >= 2007)])

    st.write("Podemos perceber que a exportação de vinho para o Uruguai é relativamente discreta, no entanto, nos últimos dois anos, observamos um crescimento significativo, atingindo a marca de 997 mil dólares em exportações. Esse aumento pode ter sido impulsionado por uma combinação de fatores, incluindo a qualidade do produto, uma demanda crescente e a competitividade dos preços, influenciada pelos acordos do Mercosul.")
    plotbar(df[(df['Destino'] == 'Uruguai') & (df['Ano'] >= 2007)])

    st.write("Embora China e Estados Unidos sejam considerados os mercados alvo, nosso principal destino exportador é o Paraguai responsável por 90% do crescimento das exportações totais de vinhos. ")
    plotbar(df[(df['Destino'] == 'Paraguai') & (df['Ano'] >= 2007)])
    st.write("Ao analisarmos os últimos 10 anos, notamos que o Paraguai manteve uma tendência crescente na importação de vinho brasileiro. Nos anos em que houve uma queda, isso geralmente esteve relacionado à produção e aos fatores que afetaram o Brasil.")
    analise_paraguai(df)

    conclusao(df)

    fontes_referencia()