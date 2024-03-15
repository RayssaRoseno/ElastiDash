import pandas as pd
import json 
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Restante do seu código...

# Caminho para o arquivo JSON
caminho_arquivo = r'C:\Users\rayss\Desktop\elasticsearch-main\data_non_structured.json'

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

# Gráfico de Pizza para a Distribuição dos Status dos Pedidos
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
status_counts = df['order_status'].value_counts()
plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', colors=['lightcoral', 'lightgreen', 'lightblue'])
plt.title('Distribuição dos Status dos Pedidos')

# Gráfico de Barras para a Segmentação de Clientes com Base nas Pontuações de Revisão
plt.subplot(2, 2, 2)
df['review_score'] = pd.to_numeric(df['review_score'], errors='coerce')
df['segmento_cliente'] = pd.cut(df['review_score'], bins=[-1, 3, 5], labels=['Baixa Pontuação', 'Alta Pontuação'], right=False)
segmento_counts = df['segmento_cliente'].value_counts()
plt.bar(segmento_counts.index, segmento_counts, color=['lightcoral', 'lightgreen'])
plt.title('Segmentação de Clientes com Base nas Pontuações de Revisão')

# Gráfico de Linha para Análise Temporal
plt.subplot(2, 2, 3)
df['purchase_timestamp'] = pd.to_datetime(df['purchase_timestamp'])
df['mes'] = df['purchase_timestamp'].dt.to_period("M")
temporal_counts = df['mes'].value_counts().sort_index()
temporal_counts.plot(kind='line', marker='o', color='lightcoral')
plt.title('Atividade de Compra ao Longo do Tempo')
plt.xlabel('Mês')
plt.ylabel('Número de Compras')

# Histograma para a Distribuição das Pontuações de Revisão
plt.subplot(2, 2, 4)
plt.hist(df['review_score'].dropna(), bins=[1, 2, 3, 4, 5, 6], color='lightblue', edgecolor='black')
plt.title('Distribuição das Pontuações de Revisão')
plt.xlabel('Pontuação')
plt.ylabel('Número de Avaliações')

plt.tight_layout()

# Nuvem de Palavras para Comentários
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df['review_comment_message'].dropna()))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Nuvem de Palavras para Comentários')
plt.axis('off')

plt.show()
