# Rede de Acesso

Radar de Inclusão Digital e Conectividade nos Municípios Brasileiros.

## Sobre o Projeto

O projeto **Rede de Acesso** reúne e apresenta dados relacionados ao acesso à internet e à renda nos municípios brasileiros.

A aplicação foi desenvolvida em Python com Streamlit e FastAPI e permite explorar indicadores municipais, consultar informações coletadas por Web Scraping, utilizar um modelo local de classificação temática e interagir com um Assistente ESG com memória conversacional.

O projeto evoluiu ao longo dos Testes de Performance, incorporando coleta e integração de dados, visualizações, API, modelagem de linguagem natural e uso de LLM com Prompt Engineering.

## Problema de Negócio

O projeto é orientado pela seguinte questão:

> Quais municípios brasileiros apresentam maiores limitações de acesso digital e como essa condição se relaciona com indicadores de renda?

A análise possui caráter descritivo e comparativo e não busca estabelecer relações de causa e efeito entre renda e acesso à internet.

## Relação com ESG e ODS

O projeto está relacionado principalmente à dimensão social de ESG, ao permitir observar diferenças territoriais de acesso digital e renda.

A solução está associada principalmente aos seguintes Objetivos de Desenvolvimento Sustentável:

- **ODS 4 — Educação de Qualidade**
- **ODS 9 — Indústria, Inovação e Infraestrutura**
- **ODS 10 — Redução das Desigualdades**

## Metodologia

O desenvolvimento utiliza como referência as metodologias CRISP-DM e TDSP.

### CRISP-DM

1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation
6. Deployment

### TDSP

A organização dos diretórios segue as fases do Team Data Science Process:

1. Business Understanding
2. Data Ingest & Understanding
3. Modeling
4. Deployment
5. Acceptance

O **Project Charter** está localizado em:

`01_business_understanding/project_charter.md`

O **Data Summary Report**, os scripts de coleta e tratamento e os arquivos de dados estão localizados em:

`02_data_ingest_understanding/`

Os arquivos de avaliação dos modelos estão localizados em:

`03_modeling/`

## Fontes de Dados

Foram utilizadas as seguintes fontes:

- **IBGE — SIDRA:** dados do Censo Demográfico 2022 sobre acesso domiciliar à internet e rendimento domiciliar mediano per capita;
- **Ministério das Comunicações:** notícias coletadas por Web Scraping utilizando `requests` e `BeautifulSoup`;
- **Dados complementares do usuário:** arquivos CSV enviados pela própria aplicação.

A integração dos dados municipais utiliza o código IBGE como chave.

## Ciclo de Ciência de Dados

O fluxo consolidado do projeto é:

`Coleta → Tratamento → Integração → Análise → Modelagem/IA → Interpretação → Apresentação`

A solução utiliza os dados coletados em diferentes etapas:

- coleta via API SIDRA e Web Scraping;
- limpeza e padronização dos dados;
- integração das bases municipais;
- análise quantitativa com Python e Pandas;
- classificação temática com modelo local;
- interpretação dos indicadores com LLM;
- apresentação dos resultados em dashboard interativo.

## Funcionalidades

A aplicação permite:

- navegar entre diferentes páginas;
- selecionar unidade da federação e município;
- visualizar indicadores de acesso à internet e renda;
- comparar municípios e indicadores estaduais;
- visualizar tabelas e gráficos;
- consultar notícias coletadas por Web Scraping;
- visualizar nuvem de palavras e frequência de termos;
- enviar arquivos CSV com dados complementares;
- integrar dados pelo código IBGE;
- baixar dados processados;
- consultar os dados por meio de FastAPI;
- realizar classificação temática de textos com modelo local;
- utilizar um Assistente ESG com memória conversacional;
- fazer perguntas sucessivas preservando o contexto da conversa.

## Aplicação Multipágina

A navegação da aplicação é implementada com `st.navigation` e `st.Page`.

As principais páginas são:

- **Início:** apresentação do projeto, problema de negócio, objetivo e ODS;
- **Análise Municipal:** filtros, indicadores, comparações e visualizações;
- **Notícias:** conteúdo coletado por Web Scraping;
- **Análise com Modelo Local:** classificação temática de textos;
- **Assistente ESG:** interação em linguagem natural com memória conversacional;
- **Dados Complementares:** upload e integração de dados adicionais;
- **API:** demonstração da integração entre Streamlit e FastAPI.

## Web Scraping

A coleta de notícias é realizada pelo script:

`02_data_ingest_understanding/coleta_noticias_mcom.py`

O script utiliza `requests` e `BeautifulSoup`.

São coletados:

- título;
- data;
- resumo;
- link.

O resultado é armazenado em:

`02_data_ingest_understanding/data/noticias_mcom.csv`

A coleta é executada separadamente da aplicação Streamlit.

### Avaliação do uso de Selenium

Foi avaliada a necessidade de utilização do Selenium.

Como os dados necessários estavam disponíveis diretamente no HTML retornado pelo servidor, a combinação `requests` + `BeautifulSoup` foi suficiente.

O Selenium não foi utilizado porque acrescentaria complexidade sem necessidade técnica para a fonte analisada.

## FastAPI

A FastAPI disponibiliza os dados processados e funcionalidades utilizadas pela aplicação.

O arquivo principal é:

`api.py`

A documentação automática pode ser acessada, com a API em execução, em:

`http://127.0.0.1:8000/docs`

A comunicação entre Streamlit e FastAPI é centralizada em:

`src/cliente_api.py`

## Modelo Local

O projeto utiliza o modelo:

`MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli`

O modelo foi selecionado após comparação com outro modelo multilíngue utilizando um banco de provas com notícias reais coletadas pelo projeto.

Sua função é realizar **classificação temática zero-shot** dos textos.

As classificações apresentadas pela aplicação devem ser interpretadas como sugestões temáticas.

## Assistente ESG com Memória Conversacional

No TP5 foi incorporado um Assistente ESG utilizando um LLM acessado pela API da Groq.

A funcionalidade permite realizar perguntas sobre os indicadores municipais e manter o contexto entre interações sucessivas.

A memória conversacional é mantida durante a sessão utilizando:

`st.session_state`

Para evitar crescimento indefinido do contexto, a aplicação envia ao modelo apenas uma janela das interações mais recentes.

### Separação entre cálculo e LLM

Os cálculos quantitativos são realizados pela aplicação com Python e Pandas.

Entre os indicadores fornecidos ao Assistente ESG estão:

- média do percentual de domicílios sem internet;
- mediana da renda per capita;
- municípios com maior e menor percentual sem internet;
- municípios com maior e menor renda mediana per capita.

O LLM é utilizado para interpretar os fatos calculados e gerar respostas em linguagem natural.

## Prompt Engineering

O prompt do Assistente ESG foi estruturado para:

- responder em português;
- utilizar somente os fatos fornecidos pela aplicação;
- não inventar municípios, indicadores ou valores;
- não alterar os resultados calculados em Python;
- evitar relações causais não sustentadas pelos dados;
- informar quando a informação solicitada não estiver disponível;
- relacionar os resultados aos ODS quando pertinente.

Durante os testes, o assistente manteve o contexto entre perguntas e também recusou fornecer uma informação que não fazia parte dos dados disponibilizados.

## Segurança da Chave da API

A chave da Groq não é armazenada no código-fonte.

Ela deve ser configurada localmente no arquivo:

`.env`

O arquivo `.env` está incluído no `.gitignore` e não deve ser enviado ao GitHub.

## Como Executar o Projeto

### 1. Criar o ambiente virtual

No Windows:

```powershell
py -m venv .venv
```

### 2. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a execução do script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Depois:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 4. Configurar a chave da Groq

Crie um arquivo chamado:

`.env`

na raiz do projeto.

Adicione:

```text
GROQ_API_KEY=sua_chave_da_groq
```

Substitua `sua_chave_da_groq` por uma chave válida.

**Nunca envie esse arquivo para o GitHub.**

### 5. Executar a FastAPI

Em um terminal com o ambiente virtual ativado:

```powershell
python -m uvicorn api:app --reload
```

A API ficará disponível em:

`http://127.0.0.1:8000`

Documentação:

`http://127.0.0.1:8000/docs`

### 6. Executar o Streamlit

Em outro terminal, com o ambiente virtual ativado:

```powershell
python -m streamlit run app.py
```

A aplicação ficará disponível normalmente em:

`http://localhost:8501`

## Versionamento

Repositório do projeto:

https://github.com/amandamesquita-infnet/rede-de-acesso

## Uso de Inteligência Artificial

Ferramentas e modelos de Inteligência Artificial foram utilizados durante o desenvolvimento do projeto:

- **ChatGPT — OpenAI, GPT-5.6 Sol:** apoio à revisão da arquitetura, depuração, e identificação de erros;
- **Groq API — modelo `openai/gpt-oss-20b`:** utilizado no Assistente ESG para interpretação dos fatos fornecidos pela aplicação e manutenção do contexto conversacional;
- **Hugging Face — `MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli`:** modelo local utilizado para classificação temática zero-shot.

As respostas produzidas pelo Assistente ESG são limitadas ao contexto disponibilizado pela aplicação, e os cálculos quantitativos permanecem sob responsabilidade do código Python.