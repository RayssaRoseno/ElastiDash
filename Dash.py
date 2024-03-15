## Importações ##
# from elasticsearch import Elasticsearch  # Parte com integração do Elasticsearch

import pandas as pd
import json 
import matplotlib.pyplot as plt
import seaborn as sns
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import os

## Parte com integração do Elasticsearch ##
"""
# Função para consultar o Elasticsearch e obter os dados atualizados
def consultar_elasticsearch():
    # Conecte-se ao Elasticsearch
    es = Elasticsearch()

    # Consulta para obter os dados do Elasticsearch
    resultados = es.search(index='seu_indice_aqui', body={'query': {'match_all': {}}})

    # Processar os resultados da consulta e retornar os dados relevantes
    dados = []
    for hit in resultados['hits']['hits']:
        documento = hit['_source']
        dados.append({
            'order_status': documento.get('order_status'),
            'purchase_timestamp': documento.get('purchase_timestamp'),
            'review_score': documento.get('review', {}).get('review_score'),
            'review_comment_message': documento.get('review', {}).get('review_comment_message')
        })

    return dados

# Atualizar os dados do DataFrame com os dados do Elasticsearch
def atualizar_dados_elasticsearch():
    dados_elasticsearch = consultar_elasticsearch()
    return pd.DataFrame(dados_elasticsearch)
"""

## Código existente ##
# Obter o diretório atual do arquivo Python
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Caminho para o arquivo JSON (usando um caminho relativo)
caminho_arquivo = os.path.join(diretorio_atual, 'data_non_structured.json')

# Lista para armazenar os dados processados
data = []

# Abrir o arquivo JSON e processar cada linha
with open(caminho_arquivo, 'r') as arquivo:
    for linha in arquivo:
        # Carregar o documento JSON
        documento = json.loads(linha)

        # Extrair as informações relevantes, ignorando linhas sem informações essenciais
        if 'order_status' in documento and 'purchase_timestamp' in documento and 'review' in documento:
            order_status = documento['order_status']
            purchase_timestamp = documento['purchase_timestamp']
            
            # Se a revisão estiver presente, extrair a pontuação e o comentário
            review = documento.get('review', {})
            review_score = review.get('review_score', None)
            review_comment_message = review.get('review_comment_message', None)

            # Adicionar as informações à lista de dados
            data.append({'order_status': order_status,
                         'purchase_timestamp': purchase_timestamp,
                         'review_score': review_score,
                         'review_comment_message': review_comment_message})

# Criar um DataFrame pandas com os dados
df = pd.DataFrame(data)

# Configurar o estilo dos gráficos
sns.set(style="whitegrid")

# Inicializar a aplicação Dash com Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do Dashboard com Bootstrap
app.layout = dbc.Container(
    [
        html.H1("ElastiDash em Tempo Real", className="display-4", style={'font-family': 'Arial'}),
        dcc.Graph(id='status-pedidos'),
        dcc.Graph(id='segmentacao-clientes'),
        dcc.Graph(id='atividade-tempo'),
        dcc.Graph(id='distribuicao-revisao'),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
    ],
    fluid=True
)

# Callbacks para atualizar os gráficos
@app.callback(
    [Output('status-pedidos', 'figure'),
     Output('segmentacao-clientes', 'figure'),
     Output('atividade-tempo', 'figure'),
     Output('distribuicao-revisao', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    # Gráficos atualizados aqui
    pass

if __name__ == '__main__':
    # Definindo o host e a porta
    host = '127.0.0.1'
    porta = 8050

    # Inicializando o aplicativo Dash
    app.run_server(debug=True, host=host, port=porta)
