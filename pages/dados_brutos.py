import streamlit as st
import requests
import pandas as pd


url = 'https://labdados.com/produtos'

response = requests.get(url)

if response.status_code == 200:
    data = pd.DataFrame.from_dict(response.json())
else:
    st.error('Erro ao acessar a API')
    st.stop()

data['Data da Compra'] = pd.to_datetime(
    data['Data da Compra'], format='%d/%m/%Y'
)

with st.expander('Colunas'):
    colunas = st.multiselect(
        'Selecione as colunas',
        list(data.columns),
        list(data.columns),
    )


st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect(
        'Selecione os produtos',
        data['Produto'].unique(),
        data['Produto'].unique(),
    )

with st.sidebar.expander('Preco do produto'):
    preco = st.slider(
        'Selecione o preço',
        min_value=int(data['Preço'].min()),
        max_value=int(data['Preço'].max()),
        value=(
            int(data['Preço'].min()),
            int(data['Preço'].max()),
        ),
    )

with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input(
        'Selecione a data',
        (
            data['Data da Compra'].min(),
            data['Data da Compra'].max(),
        ),
    )

with st.sidebar.expander('Frete da venda'):
    frete = st.slider('Frete', 0, 250, (0, 250))

with st.sidebar.expander('Vendedor'):
    vendedores = st.multiselect(
        'Selecione os vendedores',
        data['Vendedor'].unique(),
        data['Vendedor'].unique(),
    )

with st.sidebar.expander('Local da compra'):
    local_compra = st.multiselect(
        'Selecione o local da compra',
        data['Local da compra'].unique(),
        data['Local da compra'].unique(),
    )

with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider(
        'Selecione a avaliação da compra',
        min_value=1,
        max_value=5,
        value=(1, 5),
    )

with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect(
        'Selecione o tipo de pagamento',
        data['Tipo de pagamento'].unique(),
        data['Tipo de pagamento'].unique(),
    )

with st.sidebar.expander('Quantidade de parcelas'):
    qtd_parcelas = st.slider(
        'Selecione a quantidade de parcelas',
        min_value=1,
        max_value=24,
        value=(1, 24),
    )

query = '''
Produto in @produtos and \
`Categoria do Produto` in @categoria and \
@preco[0] <= Preço <= @preco[1] and \
@frete[0] <= Frete <= @frete[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
Vendedor in @vendedores and \
`Local da compra` in @local_compra and \
@avaliacao[0]<= `Avaliação da compra` <= @avaliacao[1] and \
`Tipo de pagamento` in @tipo_pagamento and \
@qtd_parcelas[0] <= `Quantidade de parcelas` <= @qtd_parcelas[1]
'''

dados_filtrados = data.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(
    'A tabela possui :blue[{0}] linhas e :blue[{1}] colunas'.format(
        dados_filtrados.shape[0], dados_filtrados.shape[1]
    )
)
