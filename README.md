# Rede de Acesso

Radar de Inclusão Digital e Conectividade nos Municípios Brasileiros.

## Sobre o Projeto

O projeto **Rede de Acesso** reúne e apresenta dados relacionados ao acesso à internet e à renda nos municípios brasileiros.

A aplicação foi desenvolvida em Python com Streamlit e permite explorar indicadores por unidade da federação e município, consultar informações coletadas por Web Scraping e acrescentar dados complementares por meio de arquivos CSV.

No TP3, a aplicação foi reorganizada em múltiplas páginas e integrada a uma API desenvolvida com FastAPI. A interface Streamlit passou a consumir os dados processados por meio dessa API, estabelecendo uma separação entre a camada de apresentação e a camada de acesso aos dados.

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
- consultar os dados por meio de uma API desenvolvida com FastAPI;
- realizar consultas GET de municípios pelo código IBGE;
- consultar a lista de municípios disponíveis;
- consultar as notícias coletadas por Web Scraping;
- realizar requisições POST para comparação entre municípios;
- consumir a própria FastAPI diretamente pela interface Streamlit;
- tratar a indisponibilidade temporária da API sem interromper toda a aplicação.

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

O script utiliza `requests` e `BeautifulSoup` para coletar notícias do portal oficial do Ministério das Comunicações.

No TP3, a coleta foi ampliada para considerar as páginas mensais de **outubro e novembro de 2026**, incluindo a paginação disponível no portal.

O processo percorre automaticamente as páginas de cada mês até encontrar uma página sem novos registros.

Para cada notícia são coletados:

- título;
- data de publicação;
- resumo;
- link.

A listagem mensal do Ministério das Comunicações apresenta a data de última modificação do conteúdo. Para evitar que essa informação seja confundida com a data original de publicação, o script acessa também a página individual de cada notícia e coleta a data disponibilizada no elemento `documentPublished`.

No teste realizado após a atualização do processo, foram coletadas **89 notícias**, sendo 44 referentes à página de novembro e 45 referentes à página de outubro de 2026.

O resultado é armazenado em:

`02_data_ingest_understanding/data/noticias_mcom.csv`

A coleta é executada separadamente da aplicação Streamlit. O arquivo gerado é posteriormente disponibilizado pela FastAPI para consumo da interface.

### Avaliação do uso de Selenium

Foi avaliada a necessidade de utilização do Selenium antes da definição da tecnologia de coleta.

O diagnóstico está registrado no script:

`02_data_ingest_understanding/diagnostico_scraping_mcom.py`

O teste realizado na página de notícias do Ministério das Comunicações retornou status HTTP 200 e identificou títulos de notícias diretamente no HTML recebido pelo `requests`.

Dessa forma, foi verificado que os dados necessários para a coleta já estavam disponíveis no HTML entregue pelo servidor, sem necessidade de executar JavaScript ou realizar interações com o navegador.

Por esse motivo, a combinação `requests` + `BeautifulSoup` foi considerada suficiente para a fonte utilizada. O Selenium não foi incluído porque acrescentaria uma dependência e uma camada de complexidade sem necessidade técnica para esse caso.

## FastAPI

No TP3, foi criada uma API com FastAPI para disponibilizar os dados processados do projeto.

O arquivo responsável pela API é:

`api.py`

A API utiliza os arquivos processados armazenados em:

`02_data_ingest_understanding/data/`

Os principais endpoints são:

### GET `/`

Retorna informações básicas sobre o projeto e o status da API.

### GET `/municipios`

Retorna a lista de municípios e seus respectivos indicadores disponíveis na base processada.

### GET `/municipios/{codigo_ibge}`

Consulta os indicadores de um município utilizando seu código IBGE.

Exemplo:

`/municipios/3304557`

### GET `/noticias`

Retorna as notícias coletadas pelo processo de Web Scraping.

### POST `/comparacao`

Recebe uma lista de códigos IBGE e retorna os indicadores dos municípios solicitados para comparação.

A documentação automática da API pode ser acessada, com o servidor em execução, em:

`http://127.0.0.1:8000/docs`

## Integração Streamlit e FastAPI

As requisições realizadas pela aplicação Streamlit foram centralizadas no arquivo:

`src/cliente_api.py`

Esse módulo concentra as chamadas HTTP utilizadas pelas páginas da aplicação para consultar os endpoints da FastAPI.

A integração é utilizada nas páginas de:

- Análise Municipal;
- Notícias e Conectividade;
- Dados Complementares;
- API.

Dessa forma, as páginas da interface não precisam acessar diretamente os arquivos CSV internos para obter os dados principais do projeto.

A arquitetura utilizada pode ser representada de forma simplificada como:

`Streamlit → cliente_api.py → FastAPI → dados processados`

## Configuração da URL da API

O endereço da FastAPI não fica fixado diretamente nas páginas da aplicação.

A configuração é centralizada no arquivo:

`config.py`

Por padrão, o projeto utiliza:

`http://127.0.0.1:8000`

Também é possível definir outro endereço utilizando a variável de ambiente:

`REDE_API_URL`

Exemplo no PowerShell:

```powershell
$env:REDE_API_URL="http://127.0.0.1:8000"
```

Essa estrutura evita espalhar o endereço da API por diferentes arquivos da aplicação e facilita futuras alterações no ambiente de execução.

## Tratamento de Indisponibilidade da API

As páginas principais que dependem da FastAPI tratam erros de conexão.

Caso a API esteja desligada ou temporariamente indisponível, o Streamlit apresenta uma mensagem amigável ao usuário em vez de exibir um traceback.

O comportamento foi testado nas páginas:

- Análise Municipal;
- Notícias e Conectividade;
- Dados Complementares.

Após a API ser iniciada novamente, as páginas voltam a carregar os dados normalmente.

## Session State

O `st.session_state` é utilizado para manter informações específicas da sessão do usuário.

Entre os usos atuais estão:

- manutenção das seleções realizadas nos filtros;
- armazenamento temporário dos dados enviados por upload;
- utilização dos dados complementares em outras partes da aplicação durante a mesma sessão.

## Preparação para Uso Futuro de LLM

No TP3 ainda não foi realizada a integração com um modelo de linguagem.

Como evolução do projeto, uma LLM poderá ser utilizada para processar informações textuais relacionadas aos dados de conectividade, mantendo a análise vinculada ao escopo e às informações disponíveis no projeto.

A integração deverá preservar o caráter descritivo da aplicação e evitar inferências causais que não sejam sustentadas pelos dados.

## Como Executar o Projeto

### 1. Criar o ambiente virtual

```powershell
py -m venv .venv
```

### 2. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a execução do script de ativação, pode ser necessário liberar a execução apenas para a sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

### 3. Instalar as dependências

```powershell
py -m pip install -r requirements.txt
```

### 4. Executar a FastAPI

Em um terminal:

```powershell
py -m uvicorn api:app --reload
```

A API ficará disponível, por padrão, em:

`http://127.0.0.1:8000`

A documentação automática poderá ser consultada em:

`http://127.0.0.1:8000/docs`

### 5. Executar o Streamlit

Em outro terminal, com o mesmo ambiente virtual ativado:

```powershell
py -m streamlit run app.py
```

## Versionamento

O projeto está disponível no GitHub:

https://github.com/amandamesquita-infnet/rede-de-acesso

## Uso de Inteligência Artificial

Uma ferramenta de Inteligência Artificial foi utilizada como apoio durante o desenvolvimento do projeto.

- **ChatGPT - OpenAI, GPT-5.6 Sol:** utilizado como apoio na organização do projeto, revisão da arquitetura, identificação de problemas, depuração e correção de erros.