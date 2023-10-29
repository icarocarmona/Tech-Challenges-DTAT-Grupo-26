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
    anos_recentes = [str(ano) for ano in range(2007, 2023)]  # 2008 a 2022
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
        "Quantidade de Litros Vendidos nos Últimos 15 Anos para Vinho de Mesa e VINHO FINO DE MESA (VINÍFERA")
    plt.xlabel("Ano")
    plt.ylabel("Quantidade (milhares de litros)")
    plt.xticks(rotation=45)
    plt.legend(title="Produto")

    mesa = produtos_desejados[produtos_desejados['produto'] == 'VINHO DE MESA']
    fino = produtos_desejados[produtos_desejados['produto']
                              == 'VINHO FINO DE MESA (VINÍFERA)']

    # st.table(fino)
    # st.table(mesa)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=anos_recentes,
        y=fino['Quantidade (L)'],
        name='Vinho Fino',
        marker_color='rgb(194,8,90)'
    ))
    fig2.add_trace(go.Bar(
        x=anos_recentes,
        y=mesa['Quantidade (L)'],
        name='Vinho de Mesa',
        marker_color='rgb(113,47,121)'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig2.update_layout(title_text='Quantidade de Litros produzidos nos Últimos 15 Anos de Vinho de Mesa e Vinho Fino (VINÍFERA)',
                       barmode='group', xaxis_tickangle=-45)
    # st.plotly_chart(fig2, use_container_width=True)

    st.pyplot(fig)


st.write('# Tech challenge')
# carregando os dados
df = load_dados_de_vinhos()
tab_home, tab_historico, tab_dados = st.tabs(
    ["🎯 Home", "📈 Historico", "🗃 Data"])


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
    df_home = pd.DataFrame({
        "Nome": ["Bea", "Icaro", "Pri"],
        "linkedin": ["https://www.linkedin.com/", "https://www.linkedin.com/", "https://www.linkedin.com/"],
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

    st.write("""        
    Embora as exportações tenham sido modestas até meados dos anos 2000, houve um crescimento notável de 2010 a 2021. O Brasil expandiu sua presença em mercados estrangeiros, ampliando a diversidade de vinhos exportados, não se restringindo apenas a espumantes, mas incluindo variedades de tintos, brancos e rosés, principalmente para países como EUA, Reino Unido, China e Canadá.
        
            <PRI VAI MANDAR>

    Apesar do crescimento, as exportações brasileiras de vinho ainda representam uma pequena parcela do mercado global, devido a desafios como competitividade de preços, barreiras comerciais e a consolidação de uma imagem de qualidade consistente. O Brasil observou um crescimento constante na exportação de vinhos ao longo do tempo, refletindo melhorias na qualidade e aceitação internacional, embora ainda esteja em processo de consolidação no mercado global de vinhos.
        """)

    # st.bar_chart(data=df_soma_anos, x="Ano", y=[
    #              "Soma de Valor U$", "Soma de Quantidade (L)"])

    st.write('A pauta de países compradores nos ultimos 15 anos também ampliou-se de 38 para 76, indicando que novos consumidores externos estão adquirindo e conhecendo o vinho brasileiro.')

    analise_ultimos_15_anos()

    st.write("Texto da explicação da producao ")
    producao_de_vinho()
