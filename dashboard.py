import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from utils import Utils

utils = Utils()

st.set_page_config(layout='wide')

st.title('Sales Dashboard :shopping_trolley:')

url = 'https://labdados.com/produtos'
regioes = [
    'Brasil',
    'Centro-Oeste',
    'Nordeste',
    'Norte',
    'Sudeste',
    'Sul',
]

st.sidebar.title('Filtros')

regiao = st.sidebar.selectbox('Região', regioes)

if regiao == 'Brasil':
    regiao = ''

todos_anos = st.sidebar.checkbox(
    'Dados de todo o período', value=True
)

if todos_anos is True:
    ano = ''

else:
    ano = st.sidebar.slider('Ano', 2020, 2023)

query_string = {'regiao': regiao.lower(), 'ano': ano}
response = requests.get(url, params=query_string)
data = pd.DataFrame.from_dict(response.json())
data['Data da Compra'] = pd.to_datetime(
    data['Data da Compra'], format='%d/%m/%Y'
)

filtro_vendedores = st.sidebar.multiselect(
    'Vendedores', data['Vendedor'].unique()
)
if filtro_vendedores is True:
    data = data[data['Vendedor']].isin(filtro_vendedores)


# Tabelas

receita_estados = data.groupby('Local da compra')[
    ['Preço']
].sum()
receita_estados = (
    data.drop_duplicates(subset='Local da compra')[
        ['Local da compra', 'lat', 'lon']
    ]
    .merge(
        receita_estados,
        left_on='Local da compra',
        right_index=True,
    )
    .sort_values('Preço', ascending=False)
)

receita_mensal = (
    data.set_index('Data da Compra')
    .groupby(pd.Grouper(freq='M'))['Preço']
    .sum()
    .reset_index()
)
receita_mensal['Ano'] = receita_mensal[
    'Data da Compra'
].dt.year
receita_mensal['Mes'] = receita_mensal[
    'Data da Compra'
].dt.month_name()

receitas_categoria = (
    data.groupby('Categoria do Produto')[['Preço']]
    .sum()
    .sort_values('Preço', ascending=False)
)

fig_receita_estados = px.bar(
    receita_estados.head(),
    x='Local da compra',
    y='Preço',
    text_auto=True,
    title='Top Estados (Receita)',
)

fig_receita_estados.update_layout(yaxis_title='Receita')

fig_receita_categorias = px.bar(
    receitas_categoria,
    text_auto=True,
    title='Receita por categoria',
)

fig_receita_categorias.update_layout(yaxis_title='Receita')

# Tabela vendedores
vendedores = pd.DataFrame(
    data.groupby('Vendedor')['Preço'].agg(['sum', 'count'])
)


# Graficos
fig_mapa_receita = px.scatter_geo(
    receita_estados,
    lat='lat',
    lon='lon',
    scope='south america',
    size='Preço',
    template='seaborn',
    hover_name='Local da compra',
    hover_data={'lat': False, 'lon': False},
    title='Receita por Estado',
)


fig_receita_mensal = px.line(
    receita_mensal,
    x='Mes',
    y='Preço',
    markers=True,
    range_y=(0, receita_mensal.max()),
    color='Ano',
    line_dash='Ano',
    title='Receita mensal',
)

fig_receita_mensal.update_layout(yaxis_title='Receita')

# Visualização do streamlit

tab1, tab2, tab3 = st.tabs(
    ['Receita', 'Quantidade de Vendas', 'Vendedores']
)

with tab1:
    column1, column2 = st.columns(2)
    with column1:
        st.metric(
            'Receita',
            utils.format_number(data['Preço'].sum()),
            'R$',
        )
        st.plotly_chart(
            fig_mapa_receita, use_container_width=True
        )
        st.plotly_chart(
            fig_receita_estados, use_container_width=True
        )

    with column2:
        st.metric(
            'Quantidade de vendas',
            utils.format_number(data.shape[0]),
        )
        st.plotly_chart(
            fig_receita_mensal, use_container_width=True
        )
        st.plotly_chart(
            fig_receita_categorias, use_container_width=True
        )


with tab2:
    column1, column2 = st.columns(2)
    with column1:
        st.metric(
            'Receita',
            utils.format_number(data['Preço'].sum()),
            'R$',
        )

    with column2:
        st.metric(
            'Quantidade de vendas',
            utils.format_number(data.shape[0]),
        )

with tab3:
    column1, column2 = st.columns(2)

    quantidade_vendedores = st.number_input(
        'Quantidade de vendedores: ', 2, 10, 5
    )
    with column1:
        st.metric(
            'Receita',
            utils.format_number(data['Preço'].sum()),
            'R$',
        )
        fig_receita_vendedores = px.bar(
            vendedores[['sum']]
            .sort_values('sum', ascending=False)
            .head(quantidade_vendedores),
            x='sum',
            y=vendedores[['sum']]
            .sort_values('sum', ascending=False)
            .head(quantidade_vendedores)
            .index,
            text_auto=True,
            title=f'Top {quantidade_vendedores} vendedores (Receita)',
        )

        st.plotly_chart(fig_receita_vendedores)

    with column2:
        st.metric(
            'Quantidade de vendas',
            utils.format_number(data.shape[0]),
        )
        fig_vendas_vendedores = px.bar(
            vendedores[['count']]
            .sort_values('count', ascending=False)
            .head(quantidade_vendedores),
            x='count',
            y=vendedores[['count']]
            .sort_values('count', ascending=False)
            .head(quantidade_vendedores)
            .index,
            text_auto=True,
            title=f'Top {quantidade_vendedores} vendedores (Quantidade de vendas)',
        )

        st.plotly_chart(fig_vendas_vendedores)
