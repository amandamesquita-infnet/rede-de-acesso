# Rede de Acesso

Radar de Inclusão Digital e conectividade nos municípios brasileiros.

## Metodologia

O desenvolvimento do projeto usa como referência as metodologias CRISP-DM e TDSP.

### CRISP-DM

O CRISP-DM orienta o processo analítico a partir das seguintes etapas:

1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation
6. Deployment

No estágio atual do projeto, o foco está principalmente nas etapas de Business Understanding, Data Understanding e Data Preparation, com a definição do problema de negócio, identificação das fontes, coleta inicial e integração dos dados.

### TDSP

A organização dos diretórios do projeto segue as fases do Team Data Science Process (TDSP):

1. Business Understanding
2. Data Ingest & Understanding
3. Modeling
4. Deployment
5. Acceptance

Os artefatos iniciais do projeto estão organizados de acordo com essas fases. O Project Charter pode ser encontrado em `01_business_understanding` e o Data Summary Report, junto dos scripts de coleta e tratamento inicial dos dados, encontra-se em `02_data_ingest_understanding`.

## Como executar o projeto

1. Criar e ativar um ambiente virtual Python.

2. Instalar as dependências:

```bash
pip install -r requirements.txt