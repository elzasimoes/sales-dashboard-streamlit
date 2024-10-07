import streamlit as st
import pandas as pd
import plotly.express as px

# Dados da API
data = []

# Criando o DataFrame
df = pd.DataFrame(data)

# Agrupando os dados por usuário para somar o esforço total e manter a alocação de horas por dia
grouped = df.groupby(['user', 'exit_hour']).agg(
    total_effort=pd.NamedAgg(column='effort', aggfunc='sum'),
    test_allocated_hour_per_user=pd.NamedAgg(column='test_allocated_hour_per_user', aggfunc='first')
).reset_index()

# Criando uma nova coluna que combina o nome do usuário com o horário de saída
grouped['user_with_exit'] = grouped['user'] + ' (Exit: ' + grouped['exit_hour'] + ')'

# Calculando o tempo livre para cada usuário
grouped['free_time'] = grouped['test_allocated_hour_per_user'] - grouped['total_effort']

# Gerando o gráfico de barras empilhadas
fig = px.bar(grouped, 
             x='user_with_exit', 
             y=['total_effort', 'free_time'], 
             title="Alocação de Tempo por Usuário",
             labels={'value': 'Horas', 'user_with_exit': 'Usuário (Horário de Saída)'},
             color_discrete_sequence=['#636EFA', '#00CC96'])

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig)
