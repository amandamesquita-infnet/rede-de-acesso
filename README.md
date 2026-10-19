# Rede de Acesso

Radar de Inclusão Digital e Conectividade nos Municípios Brasileiros.

## Sobre o Projeto

O projeto **Rede de Acesso** busca reunir e apresentar dados relacionados ao acesso à internet e à renda nos municípios brasileiros.

A aplicação foi desenvolvida em Python com Streamlit e permite explorar indicadores por unidade da federação e município, visualizar informações coletadas por Web Scraping e acrescentar dados complementares por meio de arquivos CSV.

No TP3, a aplicação foi reorganizada em múltiplas páginas e integrada a uma API desenvolvida com FastAPI, permitindo também a consulta estruturada dos dados processados.

## Problema de Negócio

O projeto é orientado pela seguinte questão:

> Quais municípios brasileiros apresentam maiores limitações de acesso digital e como essa condição se relaciona com indicadores de renda?

A análise possui caráter descritivo e comparativo e não busca estabelecer relações de causa e efeito entre renda e acesso à internet.

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

No projeto, foram desenvolvidas principalmente as etapas de Business Understanding, Data Understanding, Data Preparation e Deployment, incluindo definição do problema de negócio, coleta, tratamento, integração, exploração e disponibilização dos dados.

### TDSP

A organização dos diretórios segue as fases do Team Data Science Process (TDSP):

1. Business Understanding
2. Data Ingest & Understanding
3. Modeling
4. Deployment
5. Acceptance

O **Project Charter** está localizado em `01_business_understanding`.

O **Data Summary Report**, os scripts de coleta e tratamento dos dados e os arquivos CSV estão localizados em `02_data_ingest_understanding`.

As demais pastas são mantidas para acompanhar a evolução do projeto.

## Fontes de Dados

Foram utilizadas as seguintes fontes:

- **IBGE - SIDRA:** dados do Censo Demográfico 2022 sobre acesso domiciliar à internet e rendimento domiciliar mediano per capita;
- **Ministério das Comunicações:** notícias coletadas por Web Scraping utilizando Requests e Beautiful Soup;
- **Dados complementares do usuário:** arquivos CSV enviados pela própria aplicação.

A integração dos dados municipais utiliza o código IBGE como chave.

## Funcionalidades

A aplicação permite:

- navegar entre diferentes páginas da aplicação;
- selecionar uma unidade da federação e um município;
- visualizar indicadores de acesso à internet e renda;
- comparar o município selecionado com os indicadores da sua unidade da federação;
- visualizar os municípios de uma UF em tabela;
- consultar um panorama nacional dos municípios com maiores percentuais de domicílios sem internet;
- consultar notícias coletadas por Web Scraping;
- visualizar uma nuvem de palavras;
- visualizar os termos mais frequentes encontrados nos títulos e resumos das notícias;
- enviar arquivos CSV com dados complementares;
- integrar os dados enviados utilizando o código IBGE;
- baixar dados processados em formato CSV;
- consultar dados por meio de uma API desenvolvida com FastAPI;
- realizar consultas GET de municípios pelo código IBGE;
- realizar requisições POST para comparação entre municípios;
- consumir a própria FastAPI diretamente pela interface Streamlit.

## Aplicação Multipágina

No TP3, a aplicação foi reorganizada utilizando `st.navigation` e `st.Page`.

As funcionalidades foram distribuídas nas seguintes páginas:

- **Início:** apresentação do projeto, problema de negócio, objetivo e ODS;
- **Análise Municipal:** filtros, indicadores municipais, comparação estadual e panorama nacional;
- **Notícias:** dados coletados por Web Scraping, tabela, nuvem de palavras e frequência de termos;
- **Dados Complementares:** upload, validação, integração e download de arquivos CSV;
- **API:** integração da interface Streamlit com a FastAPI do projeto.

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

### Avaliação do uso de Selenium

Foi avaliada a necessidade de utilização do Selenium nesta etapa.

Entretanto, as fontes atualmente utilizadas pelo projeto não dependem de interação dinâmica com páginas web. Os dados do IBGE são obtidos por meio de API e as informações necessárias da página do Ministério das Comunicações estão disponíveis no HTML e podem ser coletadas com Requests e Beautiful Soup.

Por esse motivo, o Selenium não foi utilizado, evitando dependências e complexidade adicionais sem benefício relevante para as fontes atuais.

## FastAPI

No TP3, foi criada uma API com FastAPI para disponibilizar os dados processados do projeto.

O arquivo responsável pela API é:

`api.py`

A API utiliza a base:

`02_data_ingest_understanding/data/dados_integrados.csv`

Os principais endpoints são:

### GET `/`

Retorna informações básicas sobre o projeto e o status da API.

### GET `/municipios/{codigo_ibge}`

Consulta os indicadores de um município utilizando seu código IBGE.

Exemplo:

`/municipios/3304557`

### POST `/comparacao`

Recebe uma lista de códigos IBGE e retorna os indicadores dos municípios solicitados para comparação.

A documentação automática da API pode ser acessada, com o servidor em execução, em:

`http://127.0.0.1:8000/docs`

## Integração Streamlit e FastAPI

A página **API** da aplicação Streamlit utiliza a biblioteca `requests` para consumir os endpoints da FastAPI.

A integração permite:

- verificar se a API está disponível;
- consultar um município por código IBGE;
- comparar dois municípios por meio de uma requisição POST.

Dessa forma, a aplicação apresenta uma separação entre a interface de visualização e a camada responsável por disponibilizar os dados.

## Cache e Session State

A aplicação utiliza `@st.cache_data` para evitar a leitura repetida dos arquivos de dados a cada interação com o Streamlit.

O `st.session_state` é utilizado para manter informações específicas da sessão do usuário, como seleções realizadas e dados enviados por upload.

## Preparação para Uso Futuro de LLM

Nesta etapa, ainda não foi realizada a integração com um modelo de linguagem.

Como evolução futura, pretende-se utilizar uma LLM para gerar resumos interpretativos dos indicadores de um município selecionado.

O modelo poderá receber como contexto informações como:

- percentual de domicílios sem acesso à internet;
- renda mediana per capita;
- comparação com os indicadores da unidade da federação;
- informações textuais provenientes das notícias coletadas.

A geração deverá permanecer descritiva, evitando inferir relações causais que não sejam sustentadas pelos dados.

## Como Executar o Projeto

1. Criar o ambiente virtual:

```bash
python -m venv .venv
```

2. Ativar o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Instalar as dependências:

```bash
python -m pip install -r requirements.txt
```

4. Executar a FastAPI:

```bash
python -m uvicorn api:app --reload
```

5. Em outro terminal, executar o Streamlit:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Versionamento

O projeto está disponível no GitHub:

https://github.com/amandamesquita-infnet/rede-de-acesso

## Uso de Inteligência Artificial

Uma ferramenta de Inteligência Artificial foi utilizada como apoio durante o desenvolvimento do projeto.

- **ChatGPT - OpenAI, GPT-5.6 Sol:** utilizado como apoio na organização do projeto e identificação e correção de erros.