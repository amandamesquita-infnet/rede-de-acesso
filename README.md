# Rede de Acesso

Radar de Inclusão Digital e Conectividade nos Municípios Brasileiros.

## Sobre o Projeto

O projeto **Rede de Acesso** reúne e apresenta dados relacionados ao acesso à internet e à renda nos municípios brasileiros.

A aplicação foi desenvolvida em Python com Streamlit e permite explorar indicadores por unidade da federação e município, consultar informações coletadas por Web Scraping, acrescentar dados complementares por meio de arquivos CSV e realizar classificação temática de textos utilizando um modelo de linguagem executado localmente.

No TP3, a aplicação foi reorganizada em múltiplas páginas e integrada a uma API desenvolvida com FastAPI. A interface Streamlit passou a consumir os dados processados por meio dessa API, estabelecendo uma separação entre a camada de apresentação e a camada de acesso aos dados.

No TP4, a arquitetura foi ampliada com a integração de um modelo local para classificação zero-shot de textos relacionados às notícias do Ministério das Comunicações. O modelo é carregado pela FastAPI e pode ser utilizado pelo Streamlit sem depender de um serviço externo durante a inferência.

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

No projeto, foram desenvolvidas etapas de definição do problema de negócio, coleta, tratamento, integração, exploração, modelagem, avaliação e disponibilização dos dados.

No TP4, a etapa de Modeling passou a incluir a avaliação comparativa de modelos locais para classificação temática de textos.

### TDSP

A organização dos diretórios segue as fases do Team Data Science Process (TDSP):

1. Business Understanding
2. Data Ingest & Understanding
3. Modeling
4. Deployment
5. Acceptance

O **Project Charter** está localizado em `01_business_understanding`.

O **Data Summary Report**, os scripts de coleta e tratamento dos dados e os arquivos CSV estão localizados em `02_data_ingest_understanding`.

Os scripts e resultados utilizados para comparação dos modelos estão localizados em `03_modeling`.

A justificativa detalhada da escolha do modelo está disponível em:

`docs/escolha_do_modelo.md`

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
- classificar textos em categorias relacionadas ao projeto utilizando um modelo local;
- visualizar a categoria sugerida e as pontuações atribuídas pelo modelo;
- tratar a indisponibilidade temporária da API ou do modelo sem interromper toda a aplicação.

## Aplicação Multipágina

A aplicação utiliza `st.navigation` e `st.Page`.

As funcionalidades estão distribuídas nas seguintes páginas:

- **Início:** apresentação do projeto, problema de negócio, objetivo e ODS;
- **Análise Municipal:** filtros, indicadores municipais, comparação estadual e panorama nacional;
- **Notícias:** dados coletados por Web Scraping, tabela, nuvem de palavras e frequência de termos;
- **Análise com Modelo Local:** classificação temática de textos utilizando o modelo integrado à FastAPI;
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

A API disponibiliza os dados processados do projeto e o serviço de classificação temática.

O arquivo responsável pela API é:

`api.py`

Os dados processados utilizados pelas rotas estão armazenados em:

`02_data_ingest_understanding/data/`

### GET `/`

Retorna informações básicas sobre o projeto, o status da API e informa se o modelo local foi carregado.

Exemplo de resposta:

```json
{
  "projeto": "Rede de Acesso",
  "status": "API disponível",
  "documentacao": "/docs",
  "modelo_carregado": true
}
```

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

### POST `/processar_texto`

Recebe um texto enviado pelo usuário e utiliza o modelo local para realizar sua classificação temática.

As categorias possíveis são:

- `RADIODIFUSAO`
- `CONECTIVIDADE_INFRAESTRUTURA`
- `ENDERECAMENTO_CORREIOS`
- `INCLUSAO_CAPACITACAO_DIGITAL`
- `USO_E_SETOR_DE_TELECOMUNICACOES`
- `GESTAO_POLITICAS_PUBLICAS`

A resposta contém:

- tipo de análise;
- texto processado;
- categoria sugerida;
- pontuação da categoria principal;
- pontuação de todas as categorias;
- identificação do modelo utilizado.

A pontuação retornada representa a preferência do modelo entre as categorias apresentadas e **não deve ser interpretada como probabilidade real de acerto**.

A documentação automática da API pode ser acessada, com o servidor em execução, em:

`http://127.0.0.1:8000/docs`

## Response Models e Validação

As rotas da FastAPI utilizam modelos Pydantic para validar a estrutura das respostas.

Entre os modelos utilizados estão:

- `StatusAPI`;
- `Noticia`;
- `ListaNoticias`;
- `Municipio`;
- `ListaMunicipios`;
- `PedidoAnalise`;
- `ResultadoAnalise`.

O endpoint `/processar_texto` aceita textos entre 10 e 5000 caracteres.

Campos adicionais não previstos no corpo da requisição são rejeitados pela validação da API.

Entradas inválidas retornam resposta HTTP `422`.

## Tratamento de Erros

A aplicação utiliza tratamento de erros tanto na FastAPI quanto no Streamlit.

### HTTP 404

É utilizado quando um município solicitado não é encontrado.

### HTTP 422

É utilizado para erros de validação da entrada, como textos abaixo do tamanho mínimo ou campos adicionais não permitidos.

### HTTP 503

Caso o modelo local não possa ser carregado, o endpoint `/processar_texto` retorna `503 Service Unavailable`.

As outras rotas da API permanecem disponíveis.

Esse comportamento foi testado removendo temporariamente a pasta local do modelo. Nesse cenário:

- `GET /` continuou respondendo normalmente;
- `modelo_carregado` foi apresentado como `false`;
- `POST /processar_texto` retornou HTTP 503;
- após a restauração do modelo, a API voltou a informar `modelo_carregado: true`.

### HTTP 500

Erros internos inesperados são tratados pela API e retornam uma resposta JSON padronizada, enquanto o detalhe técnico é registrado no log.

### Timeout

O cliente utilizado pelo Streamlit define limite de tempo para as requisições.

Na análise com o modelo local, o timeout foi definido em 30 segundos.

## Integração Streamlit e FastAPI

As requisições realizadas pela aplicação Streamlit foram centralizadas no arquivo:

`src/cliente_api.py`

Esse módulo concentra as chamadas HTTP utilizadas pelas páginas da aplicação para consultar os endpoints da FastAPI.

A integração é utilizada nas páginas de:

- Análise Municipal;
- Notícias e Conectividade;
- Análise com Modelo Local;
- Dados Complementares;
- API.

A arquitetura utilizada pode ser representada de forma simplificada como:

`Streamlit → cliente_api.py → FastAPI → dados processados / modelo local`

O Streamlit não carrega diretamente o modelo de linguagem.

A interface envia o texto para a FastAPI por meio de `POST /processar_texto` e apresenta ao usuário a resposta validada pela API.

## Modelo Local

### Tarefa

O modelo é utilizado para classificação temática zero-shot de textos relacionados ao escopo do projeto.

A classificação utiliza seis categorias previamente definidas.

### Banco de Provas

Foi criado um banco de provas com **30 notícias reais** coletadas pelo projeto.

Os textos foram rotulados manualmente antes dos testes dos modelos.

O conjunto possui cinco exemplos para cada uma das seis categorias.

O arquivo utilizado é:

`03_modeling/banco_de_provas.csv`

### Modelos Avaliados

Foram avaliados dois modelos candidatos:

1. `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`
2. `MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli`

Os dois modelos receberam o mesmo banco de provas, as mesmas categorias e o mesmo texto de hipótese.

### Resultados

| Métrica | mDeBERTa | MiniLMv2 |
|---|---:|---:|
| Acertos | 8/30 | 14/30 |
| Acurácia | 26,67% | **46,67%** |
| Tempo de carregamento local | 3,67 s | 3,85 s |
| Tempo total de inferência | 7,37 s | **2,04 s** |
| Tempo médio por notícia | 0,25 s | **0,07 s** |
| Pico de memória CUDA | 556,00 MB | **418,71 MB** |

### Modelo Escolhido

O modelo selecionado foi:

`MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli`

A escolha considerou o desempenho no banco de provas do próprio projeto e o custo computacional medido na máquina utilizada para desenvolvimento.

O MiniLMv2 apresentou maior acurácia, menor tempo de inferência e menor utilização de memória da GPU.

A acurácia obtida, entretanto, ainda é limitada. Por isso, a classificação é apresentada na aplicação como uma **sugestão do modelo**, e não como uma classificação definitiva.

A justificativa detalhada está disponível em:

`docs/escolha_do_modelo.md`

## Ambiente Utilizado para o Modelo

Os testes foram realizados no seguinte equipamento:

- **CPU:** Intel Core i5-12450HX;
- **RAM:** 31,73 GB;
- **GPU:** NVIDIA GeForce RTX 3050 Laptop GPU;
- **VRAM:** 6 GB;
- **PyTorch:** 2.11.0+cu128;
- **Transformers:** 5.23.0;
- **SentencePiece:** 0.2.3;
- **CUDA reconhecida pelo PyTorch:** sim.

Durante o benchmark do modelo escolhido, o pico de memória CUDA foi de aproximadamente **418,71 MB**.

O tempo médio medido foi de aproximadamente **0,07 segundo por notícia** no banco de provas utilizado.

O código também prevê execução em CPU caso CUDA não esteja disponível, embora os resultados registrados neste projeto tenham sido obtidos utilizando a GPU descrita acima.

## Download e Execução Local do Modelo

O download do modelo é realizado separadamente da inicialização da API.

O script responsável é:

`src/baixar_modelo.py`

Para baixar e salvar o modelo dentro do projeto:

```powershell
py -m src.baixar_modelo
```

O modelo será armazenado em:

`modelos/minilm_multilingual`

A pasta `modelos/` está incluída no `.gitignore` para evitar o envio dos arquivos de pesos para o repositório Git.

Durante a execução da FastAPI, o modelo é carregado a partir dessa pasta utilizando `local_files_only=True`.

Dessa forma, após o download inicial, a inferência não depende de uma conexão com o Hugging Face ou outro serviço de nuvem.

O módulo responsável pelo carregamento e pela inferência é:

`src/analisador_llm.py`

## Carregamento do Modelo

A FastAPI utiliza `lifespan` para carregar o modelo uma única vez durante a inicialização da aplicação.

O modelo permanece disponível para as requisições seguintes e não é recarregado a cada chamada de `/processar_texto`.

Caso o carregamento falhe, a exceção é tratada e a API continua disponível para as outras funcionalidades.

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

## Tratamento de Indisponibilidade no Streamlit

As páginas que dependem da FastAPI tratam erros de conexão.

Caso a API esteja desligada ou temporariamente indisponível, o Streamlit apresenta uma mensagem amigável ao usuário em vez de exibir um traceback.

Na página **Análise com Modelo Local**, também são tratados:

- erro de validação da entrada;
- indisponibilidade do modelo;
- timeout;
- falha de comunicação com a FastAPI.

Quando o modelo retorna HTTP 503, a interface informa:

> O modelo de análise está indisponível. As demais rotas da API continuam funcionando.

## Session State

O `st.session_state` é utilizado para manter informações específicas da sessão do usuário.

Entre os usos atuais estão:

- manutenção das seleções realizadas nos filtros;
- armazenamento temporário dos dados enviados por upload;
- utilização dos dados complementares em outras partes da aplicação durante a mesma sessão.

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

### 3. Instalar as dependências completas

Para executar o Streamlit, a FastAPI e o modelo local:

```powershell
py -m pip install -r requirements-api.txt
```

O arquivo `requirements-api.txt` utiliza o `requirements.txt` como base e acrescenta as dependências necessárias para o modelo local.

### 4. Baixar o modelo

Antes de iniciar a API pela primeira vez:

```powershell
py -m src.baixar_modelo
```

O download é uma etapa separada da execução da API.

Após essa etapa, o modelo será utilizado localmente.

### 5. Executar a FastAPI

Em um terminal:

```powershell
py -m uvicorn api:app --reload
```

A API ficará disponível, por padrão, em:

`http://127.0.0.1:8000`

A documentação automática poderá ser consultada em:

`http://127.0.0.1:8000/docs`

### 6. Executar o Streamlit

Em outro terminal, com o mesmo ambiente virtual ativado:

```powershell
py -m streamlit run app.py
```

O endereço local será informado pelo próprio Streamlit no terminal.

## Estrutura Relacionada ao TP4

Os principais arquivos acrescentados ou utilizados no TP4 são:

```text
03_modeling/
├── avaliar_modelo_1.py
├── avaliar_modelo_2.py
├── banco_de_provas.csv
├── criar_banco_de_provas.py
├── resultado_modelo_1.csv
├── resultado_modelo_2.csv
└── teste_modelo_1.py

docs/
└── escolha_do_modelo.md

src/
├── analisador_llm.py
├── baixar_modelo.py
└── cliente_api.py

pages/
└── analise_llm.py

api.py
requirements-api.txt
```

Os pesos do modelo são armazenados localmente na pasta `modelos/`, que não é versionada no Git.

## Versionamento

O projeto está disponível no GitHub:

https://github.com/amandamesquita-infnet/rede-de-acesso

O desenvolvimento do TP4 foi realizado inicialmente no branch:

`tp4-llm`

## Uso de Inteligência Artificial

Uma ferramenta de Inteligência Artificial foi utilizada como apoio durante o desenvolvimento do projeto.

- **ChatGPT - OpenAI, GPT-5.6 Sol:** utilizado como apoio na organização do projeto, revisão da arquitetura, identificação de problemas, depuração e correção de erros.