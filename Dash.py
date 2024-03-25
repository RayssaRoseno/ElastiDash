import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io
from elasticsearch import Elasticsearch
import random

es = Elasticsearch(["http://127.0.0.1:9200"])

atual_index = 0  # Inicialize a variável fora da função

def consultar_elasticsearch(tamanho_lote, indice_inicial):
    # Conecte-se ao Elasticsearch
    es = Elasticsearch()

    # Consulta para obter valores em lotes, ordenados pelo purchase_timestamp
    consulta = {
        "size": tamanho_lote,  # Tamanho do lote
        "from": 0,  # Índice inicial
        "query": {
            "match_all": {}  # Consulta para recuperar todos os documentos
        },
        "sort": [
            {"purchase_timestamp": {"order": "asc"}}  # Ordenar pelo purchase_timestamp em ordem ascendente
        ]
    }

    resultados = es.search(index="salles", body=consulta)

    # Processar os resultados da consulta e retornar os dados relevantes
    dados = []
    for hit in resultados['hits']['hits']:
        review_message = hit['_source']['review']['review_comment_message']
        review_score = hit['_source']['review']['review_score']
        purchase_timestamp = hit['_source']['purchase_timestamp']
        order_status = hit['_source']['order_status']
        dados.append({
            'order_status': order_status,
            'purchase_timestamp': purchase_timestamp,
            'review_score': review_score,
            'review_comment_message': review_message
        })

    return dados


def atualizar_dados_elasticsearch():
    global atual_index  # Use a palavra-chave global para indicar que você está referenciando a variável global
    atual_index += 100  # Atualize o valor da variável global
    dados_elasticsearch = consultar_elasticsearch(atual_index, 0)
    df = pd.DataFrame(dados_elasticsearch)
    return df


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.H1("ElastiDash em Tempo Real", className="display-4", style={'font-family': 'Arial'}),
        html.Img(id='status-pedidos-img'),
        html.Img(id='segmentacao-clientes-img'),
        html.Img(id='atividade-tempo-img'),
        html.Img(id='distribuicao-revisao-img'),
        dcc.Interval(id='interval-component', interval=2000, n_intervals=0)
    ],
    fluid=True
)

def fig_to_uri(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode('utf-8')

@app.callback(
    [Output('status-pedidos-img', 'src'),
     Output('segmentacao-clientes-img', 'src'),
     Output('atividade-tempo-img', 'src'),
     Output('distribuicao-revisao-img', 'src')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    dados_atualizados = atualizar_dados_elasticsearch()

    plt.figure()
    sns.countplot(x='order_status', data=dados_atualizados)
    fig_status_pedidos = plt.gcf()

    dados_atualizados['ano'] = pd.to_datetime(dados_atualizados['purchase_timestamp']).dt.year

    # Agrupar os dados por mes e contar o número de ocorrências em cada mes
    dados_agrupados_por_ano = dados_atualizados.groupby('ano').size()

    # Plotar o histograma agrupado por ano
    plt.figure()
    sns.barplot(x=dados_agrupados_por_ano.index, y=dados_agrupados_por_ano.values)
    plt.xlabel('Ano')
    plt.ylabel('Número de Compras')
    plt.title('Número de Compras por ano')
    plt.xticks(rotation=45)  # Ajustar a rotação dos rótulos no eixo x
    plt.tight_layout()  # Garante que os rótulos não se sobreponham
    fig_segmentacao_clientes = plt.gcf()

    plt.figure()
    sns.barplot(x=dados_atualizados['review_score'].dropna(), y=dados_atualizados.index, color='skyblue')
    plt.xlabel('Pontuação de Revisão')
    plt.ylabel('Índice')
    plt.title('Atividade ao Longo do Tempo')
    fig_atividade_tempo = plt.gcf()

    plt.figure()
    sns.histplot(dados_atualizados['review_score'].dropna(), kde=True)
    fig_distribuicao_revisao = plt.gcf()

    src_status_pedidos = fig_to_uri(fig_status_pedidos)
    src_segmentacao_clientes = fig_to_uri(fig_segmentacao_clientes)
    src_atividade_tempo = fig_to_uri(fig_atividade_tempo)
    src_distribuicao_revisao = fig_to_uri(fig_distribuicao_revisao)

    return src_status_pedidos, src_segmentacao_clientes, src_atividade_tempo, src_distribuicao_revisao


if __name__ == '__main__':
    host = '127.0.0.1'
    porta = 8050
    app.run_server(debug=True, host=host, port=porta)
