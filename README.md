# Rede de Acesso

Radar de Inclusão Digital e Conectividade nos Municípios Brasileiros.

## Sobre o Projeto

O projeto **Rede de Acesso** busca reunir e apresentar dados relacionados ao acesso à internet e à renda nos municípios brasileiros.

A aplicação foi desenvolvida em Python com Streamlit e permite explorar os indicadores por unidade da federação e município, além de visualizar informações coletadas por Web Scraping e acrescentar dados complementares por meio de arquivos CSV.

## Metodologia

O desenvolvimento do projeto utiliza como referência as metodologias CRISP-DM e TDSP.

### CRISP-DM

O CRISP-DM orienta o processo analítico a partir das seguintes etapas:

1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation
6. Deployment

No projeto, foram desenvolvidas principalmente as etapas de Business Understanding, Data Understanding e Data Preparation, incluindo a definição do problema de negócio, coleta, tratamento, integração e exploração dos dados.

### TDSP

A organização dos diretórios segue as fases do Team Data Science Process (TDSP):

1. Business Understanding
2. Data Ingest & Understanding
3. Modeling
4. Deployment
5. Acceptance

O **Project Charter** está localizado em `01_business_understanding`.

O **Data Summary Report**, os scripts de coleta e tratamento dos dados e os arquivos CSV estão localizados em `02_data_ingest_understanding`.

As demais pastas foram mantidas para acompanhar a evolução do projeto nas próximas etapas.

## Fontes de Dados

Nesta etapa foram utilizadas as seguintes fontes:

- **IBGE - SIDRA:** dados do Censo Demográfico 2022 sobre acesso domiciliar à internet e rendimento domiciliar mediano per capita;
- **Ministério das Comunicações:** notícias coletadas por Web Scraping utilizando Beautiful Soup;
- **Dados complementares do usuário:** arquivos CSV que podem ser enviados pela própria aplicação.

A integração dos dados municipais utiliza o código IBGE como chave.

## Funcionalidades

A aplicação permite:

- selecionar uma unidade da federação;
- selecionar um município;
- visualizar indicadores de acesso à internet e renda;
- comparar o município selecionado com os valores da sua unidade da federação;
- visualizar os municípios de uma UF em uma tabela;
- visualizar um panorama nacional dos municípios com maiores percentuais de domicílios sem internet;
- consultar notícias coletadas por Web Scraping;
- visualizar uma nuvem de palavras criada a partir das notícias;
- visualizar os termos mais frequentes encontrados nos títulos e resumos;
- enviar um arquivo CSV com dados complementares;
- integrar os dados enviados utilizando o código IBGE;
- baixar os dados filtrados e processados em formato CSV.

## Web Scraping

A coleta de notícias é realizada pelo script:

`02_data_ingest_understanding/coleta_noticias_mcom.py`

O script utiliza `requests` e `BeautifulSoup` para coletar informações da página de notícias do Ministério das Comunicações.

São coletados:

- título;
- data;
- resumo;
- link.

O resultado é armazenado em:

`02_data_ingest_understanding/data/noticias_mcom.csv`

A coleta é executada separadamente da aplicação Streamlit. O aplicativo utiliza o arquivo CSV já gerado.

## Cache e Session State

A aplicação utiliza `@st.cache_data` para evitar a leitura repetida dos arquivos de dados a cada interação com o Streamlit.

O `st.session_state` é utilizado para manter informações específicas da sessão do usuário, como as seleções realizadas e os dados enviados por upload.

## Como Executar o Projeto

1. Criar um ambiente virtual Python:

```bash
python -m venv .venv
```

2. Ativar o ambiente virtual:

```bash
.\.venv\Scripts\Activate.ps1
```

3. Instalar as dependências:

```bash
python -m pip install -r requirements.txt
```

4. Caso seja necessário realizar novamente a coleta das notícias:

```bash
python .\02_data_ingest_understanding\coleta_noticias_mcom.py
```

5. Executar a aplicação:

```bash
python -m streamlit run app.py
```

## Estrutura do Projeto

```text
Amanda_Mesquita_PB_TP2/
│
├── 01_business_understanding/
│   └── project_charter.md
│
├── 02_data_ingest_understanding/
│   ├── coleta_ibge.py
│   ├── coleta_renda.py
│   ├── integra_dados.py
│   ├── coleta_noticias_mcom.py
│   ├── data_summary_report.md
│   └── data/
│       ├── acesso_internet_municipios.csv
│       ├── renda_municipios.csv
│       ├── dados_integrados.csv
│       └── noticias_mcom.csv
│
├── 03_modeling/
├── 04_deployment/
├── 05_acceptance/
│
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Versionamento

O projeto utiliza Git para controle de versão e está disponível no GitHub:

https://github.com/amandamesquita-infnet/rede-de-acesso

## Uso de Inteligência Artificial

Uma ferramenta de Inteligência Artificial foram utilizadas como apoio durante o desenvolvimento do projeto.

- **ChatGPT - OpenAI, GPT-5.6 Sol:** utilizado como apoio na organização do projeto, revisão de código, identificação e correção de erros.

A ferramenta foi usada como suporte ao processo de desenvolvimento, com revisão e execução do código realizadas por mim (autora).