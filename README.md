# Origem da Proposta

Este projeto é parte de um experimento desenvolvido para a disciplina de Tópicos Especiais em Bancos de Dados, com foco em dados não estruturados. O objetivo principal é explorar e analisar dados não estruturados usando o Elasticsearch e criar um dashboard interativo para visualização dos resultados.

O projeto utiliza dois conjuntos de dados como base:

1. [Brazilian E-commerce Dataset por Olist](https://gamma.app/docs/Brazilian-E-commerce-DataSet-por-Olist-sievdfhkbil3v1e?mode=doc): Este conjunto de dados contém informações sobre pedidos de e-commerce no Brasil, incluindo dados de produtos, vendedores, clientes e avaliações de clientes. Ele será usado como DataSet na análise de dados não estruturados.

2. [Eficiência do Elasticsearch na Análise de Dados](https://gamma.app/docs/Eficiencia-do-Elasticsearch-na-Analise-de-Dados-36fc7s8xuhqq4um?mode=doc): Este documento detalha a proposta do projeto e destaca a importância do Elasticsearch na análise de dados não estruturados. Ele serve como base teórica e conceitual para o experimento.

## O ElastiDash

ElastiDash é a plataforma desenvolvida neste projeto, permitindo a visualização dos dados não estruturados em tempo real usando Elasticsearch. Com ElastiDash, é possível criar dashboards interativos para monitorar métricas importantes, acompanhar tendências ao longo do tempo e explorar insights detalhados com gráficos flexíveis.

## Como Instalar e Executar

Para instalar e executar este projeto localmente, siga estas etapas simples:

### Pré-requisitos

Certifique-se de ter Python e todas as dependências do projeto instaladas em sua máquina local.

### Clonar o Repositório

Clone este repositório para o seu ambiente local usando o seguinte comando:

```bash
git clone https://github.com/RayssaRoseno/ElastiDash.git
```

## Dependências

Certifique-se de ter as seguintes bibliotecas Python instaladas:

- pandas
- matplotlib
- seaborn
- dash
- dash-bootstrap-components

Você pode instalá-las executando o seguinte comando:

```bash
pip install pandas matplotlib seaborn dash dash-bootstrap-components
```
### Executar o ElastiDash

Após a instalação das dependências, você pode executar com o seguinte comando:

```bash
python Dash.py
```

Isso iniciará o servidor local e você poderá acessar o ElastiDash em seu navegador.

```bashe
Ex.: "Dash is running on http://127.0.0.1:8050/"
```
