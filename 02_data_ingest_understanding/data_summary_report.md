# Data Summary Report

## Visão Geral

Este documento apresenta as principais fontes de dados utilizadas no projeto **Rede de Acesso**, explicando a origem dos dados, suas principais variáveis, os procedimentos de coleta e tratamento e a forma como cada conjunto de dados é utilizado na aplicação.

O projeto utiliza dados do Censo Demográfico 2022 obtidos por meio da API SIDRA do IBGE, além de notícias do Ministério das Comunicações coletadas por Web Scraping.

A aplicação também permite que o usuário envie arquivos CSV com informações complementares sobre os municípios.

No TP3, os dados processados passaram a ser disponibilizados por meio de uma API desenvolvida com FastAPI, que é consumida pela interface Streamlit.

---

## Fontes de Dados

| Fonte | Conjunto de Dados | Abrangência | Forma de Obtenção | Uso no Projeto |
|---|---|---|---|---|
| IBGE - Censo Demográfico 2022 / SIDRA | Tabela 9936 - Domicílios particulares permanentes ocupados por existência de conexão domiciliar à Internet | 5.570 municípios brasileiros | API SIDRA | Identificar o percentual de domicílios sem conexão domiciliar à internet |
| IBGE - Censo Demográfico 2022 / SIDRA | Tabela 10295 - Rendimento domiciliar mensal per capita médio e mediano | 5.570 municípios brasileiros | API SIDRA | Representar a dimensão socioeconômica da análise |
| Ministério das Comunicações | Páginas de notícias do Ministério das Comunicações | Notícias relacionadas a telecomunicações, internet e conectividade | Web Scraping com Requests e Beautiful Soup | Acrescentar informações textuais ao projeto e analisar os termos mais frequentes nas notícias |
| Arquivo enviado pelo usuário | CSV com dados complementares | Depende do arquivo enviado | Upload pelo Streamlit | Permitir que novas informações sejam associadas aos municípios da base principal |

---

## Tipos de Dados

O projeto trabalha com dados estruturados, como os indicadores municipais do IBGE, e também com dados textuais obtidos a partir das notícias.

| Tipo de dado | Exemplos no projeto | Finalidade |
|---|---|---|
| Identificador | Código IBGE | Integrar diferentes bases de dados |
| Categórico | Município e unidade da federação | Identificar e agrupar os municípios |
| Numérico | Percentual de domicílios sem internet | Representar as limitações de acesso digital |
| Numérico | Rendimento domiciliar mediano per capita | Representar a situação socioeconômica |
| Data | Data de publicação das notícias | Identificar quando cada notícia foi publicada |
| Texto | Título e resumo das notícias | Criar análises de frequência e nuvem de palavras |
| URL | Link da notícia | Permitir acesso ao conteúdo original |
| Variável | Colunas enviadas pelo usuário | Complementar os dados existentes |

---

## Finalidade dos Dados

Os dados do IBGE são utilizados para comparar as condições de acesso à internet e renda entre os municípios brasileiros.

O percentual de domicílios sem conexão domiciliar à internet é utilizado como principal indicador de limitação de acesso digital. A renda mediana domiciliar per capita acrescenta uma dimensão socioeconômica à comparação entre os municípios.

As duas bases municipais são integradas pelo código IBGE.

As notícias coletadas por Web Scraping complementam os dados numéricos do projeto. A partir de seus títulos e resumos, a aplicação apresenta uma nuvem de palavras e os termos mais frequentes encontrados na coleta.

Além disso, o usuário pode enviar um arquivo CSV com novas informações. Para que essas informações sejam integradas à base principal, o arquivo deve conter a coluna `codigo_ibge`.

---

## Coleta dos Dados do IBGE

Foram realizadas duas coletas utilizando a API SIDRA do IBGE e dados do Censo Demográfico 2022.

### Acesso à Internet

A primeira coleta utilizou a Tabela 9936 para obter o percentual de domicílios particulares permanentes ocupados sem conexão domiciliar à internet.

A base resultante contém:

- 5.570 municípios;
- código IBGE;
- nome do município;
- percentual de domicílios sem conexão domiciliar à internet.

### Renda

A segunda coleta utilizou a Tabela 10295 para obter o rendimento nominal mediano mensal domiciliar per capita.

A base resultante contém:

- 5.570 municípios;
- código IBGE;
- nome do município;
- rendimento mediano domiciliar per capita.

### Integração dos Dados

As duas bases foram integradas por meio do código IBGE do município.

O resultado foi salvo no arquivo:

`02_data_ingest_understanding/data/dados_integrados.csv`

A base integrada contém os 5.570 municípios brasileiros e não apresenta valores ausentes nas variáveis utilizadas no projeto.

---

## Coleta por Web Scraping

A coleta textual é realizada nas páginas de notícias do **Ministério das Comunicações**, utilizando as bibliotecas `requests` e `BeautifulSoup`.

O processo é executado pelo arquivo:

`02_data_ingest_understanding/coleta_noticias_mcom.py`

No TP3, o processo de coleta foi revisado e ampliado.

Foram utilizadas as páginas mensais de:

- outubro de 2026;
- novembro de 2026.

O script percorre a paginação de cada mês em blocos de 20 registros e encerra a coleta quando encontra uma página sem novas notícias.

Na execução realizada para o projeto foram identificadas:

- 44 notícias referentes a novembro;
- 45 notícias referentes a outubro.

A coleta final contém **89 notícias**.

Para cada notícia são coletados os seguintes campos:

- `titulo`: título da notícia;
- `data`: data original de publicação;
- `resumo`: descrição resumida apresentada pelo portal;
- `link`: endereço da página original da notícia.

A listagem do portal apresenta informações de atualização das páginas. Para evitar que essa informação fosse confundida com a data original de publicação, o script também acessa a página individual de cada notícia e coleta a data disponibilizada no elemento correspondente à publicação.

O resultado é armazenado em:

`02_data_ingest_understanding/data/noticias_mcom.csv`

A coleta é executada separadamente da aplicação Streamlit. O arquivo processado é posteriormente disponibilizado pela FastAPI para consumo da interface.

### Avaliação do uso de Selenium

Antes da definição da técnica de coleta, foi avaliada a necessidade de utilização do Selenium.

O diagnóstico está registrado no script:

`02_data_ingest_understanding/diagnostico_scraping_mcom.py`

Os testes mostraram que os dados necessários já estavam disponíveis no HTML retornado pelo servidor e podiam ser acessados diretamente com `requests`.

Por esse motivo, a combinação `requests` + `BeautifulSoup` foi considerada suficiente para a fonte utilizada.

O Selenium não foi incorporado porque acrescentaria uma dependência e uma camada adicional de complexidade sem necessidade técnica para essa coleta.

---

## Arquivos de Dados Gerados

Os principais conjuntos de dados processados pelo projeto são:

| Arquivo | Registros | Conteúdo | Utilização |
|---|---:|---|---|
| `acesso_internet_municipios.csv` | 5.570 | Indicador municipal de domicílios sem acesso à internet | Base do indicador de inclusão digital |
| `renda_municipios.csv` | 5.570 | Renda mediana domiciliar per capita | Dimensão socioeconômica da análise |
| `dados_integrados.csv` | 5.570 | Integração dos indicadores de internet e renda | Análises municipais, visualizações e Assistente ESG |
| `noticias_mcom.csv` | 89 | Título, data, resumo e link das notícias coletadas | Análise textual, visualizações e modelagem temática |
| `banco_de_provas.csv` | 30 | Notícias reais rotuladas manualmente | Avaliação dos modelos de classificação |

---

## Qualidade dos Dados Municipais

A integração das bases de acesso à internet e renda foi realizada pelo campo `codigo_ibge`.

A base final `dados_integrados.csv` contém:

- 5.570 municípios;
- código IBGE;
- município e unidade da federação;
- percentual de domicílios sem conexão domiciliar à internet;
- renda mediana domiciliar per capita.

Nas variáveis utilizadas pela aplicação, a base integrada não apresenta valores ausentes.

O código IBGE é utilizado como identificador comum entre as fontes e também permite a associação de dados complementares enviados pelo usuário.

---

## FastAPI e Disponibilização dos Dados

No TP3 foi criada uma API com FastAPI para disponibilizar os dados processados do projeto.

O arquivo principal é:

`api.py`

A API utiliza os arquivos armazenados em:

`02_data_ingest_understanding/data/`

Entre suas funcionalidades estão:

- disponibilização dos indicadores municipais;
- consulta de município por código IBGE;
- disponibilização das notícias coletadas;
- comparação entre municípios;
- processamento de textos pelo modelo local incorporado posteriormente ao projeto.

A documentação automática da API pode ser acessada, durante sua execução local, em:

`http://127.0.0.1:8000/docs`

As chamadas da interface Streamlit são centralizadas no módulo:

`src/cliente_api.py`

Essa organização separa a interface da camada responsável por disponibilizar e processar os dados.

---

## Dados Complementares

A aplicação permite o envio de arquivos CSV com informações adicionais sobre os municípios.

Para que o arquivo seja associado à base principal, ele deve possuir a coluna:

`codigo_ibge`

O código IBGE funciona como chave de integração.

A funcionalidade permite acrescentar novas variáveis para exploração na aplicação sem modificar permanentemente a base original utilizada no projeto.

---

## Utilização dos Dados na Modelagem do TP4

No TP4, os dados textuais coletados por Web Scraping passaram a ser utilizados também em uma etapa de modelagem.

Foi definida uma tarefa de classificação temática zero-shot das notícias do Ministério das Comunicações.

As categorias utilizadas foram:

- Radiodifusão;
- Conectividade e infraestrutura;
- Endereçamento e Correios;
- Inclusão e capacitação digital;
- Uso e setor de telecomunicações;
- Gestão e políticas públicas.

Para avaliar os modelos, foi criado:

`03_modeling/banco_de_provas.csv`

O banco contém **30 notícias reais**, com cinco exemplos de cada uma das seis categorias.

Os exemplos foram rotulados manualmente antes da avaliação dos modelos.

Foram comparados:

- `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`;
- `MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli`.

O modelo selecionado foi:

`MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli`

No banco de provas utilizado no projeto, esse modelo apresentou **14 acertos em 30 exemplos**, correspondendo a **46,67% de acurácia**.

Embora o resultado demonstre limitações para a tarefa, o modelo apresentou desempenho superior ao outro candidato testado e também menor tempo de inferência e menor consumo de memória da GPU.

Por esse motivo, ele foi escolhido para integração ao projeto.

A classificação é apresentada como uma **sugestão temática**, e suas pontuações não são interpretadas como probabilidade real de acerto.

---

## Utilização dos Dados no TP5

No TP5, os dados municipais integrados passaram a fornecer o contexto estruturado para um **Assistente ESG com memória conversacional**.

A funcionalidade utiliza principalmente as variáveis:

- `municipio`;
- `percentual_sem_internet`;
- `renda_mediana_per_capita`.

O usuário seleciona uma unidade da federação e a aplicação filtra os municípios correspondentes.

Antes da chamada ao modelo de linguagem, Python e Pandas calculam informações objetivas sobre a seleção realizada.

Entre os fatos calculados estão:

- quantidade de municípios;
- média do percentual de domicílios sem internet;
- mediana da renda per capita;
- município com maior percentual de domicílios sem internet;
- município com menor percentual de domicílios sem internet;
- município com maior renda mediana per capita;
- município com menor renda mediana per capita.

Esses valores são organizados em um contexto textual e fornecidos ao LLM.

O modelo de linguagem não recebe a responsabilidade de calcular esses indicadores. Sua função é interpretar os fatos previamente calculados e produzir respostas em linguagem natural.

---

## Memória Conversacional

A memória conversacional é mantida durante a sessão do usuário por meio do `st.session_state` do Streamlit.

O histórico permite realizar perguntas dependentes de interações anteriores.

Durante o teste com os dados de Rondônia, por exemplo, o usuário perguntou qual município apresentava o maior percentual de domicílios sem internet.

O Assistente ESG identificou **Vale do Anari**, com **25,43%**.

Em seguida, o usuário perguntou apenas:

> E qual é a renda dele?

O sistema manteve o contexto da interação e informou a renda mediana per capita de **R$ 808,00** para o mesmo município.

Para limitar o crescimento do conteúdo enviado à API, apenas as interações mais recentes são utilizadas como janela de memória na chamada ao LLM.

---

## Controle das Respostas do LLM

O prompt utilizado pelo Assistente ESG determina que o modelo deve utilizar exclusivamente os fatos fornecidos pela aplicação.

Entre as restrições definidas estão:

- não inventar municípios;
- não criar indicadores ou valores inexistentes;
- não alterar os resultados calculados em Python;
- não estabelecer relações causais sem suporte nos dados;
- informar quando determinada informação não estiver disponível.

Essa estratégia também foi testada.

Ao ser questionado sobre a população de Vale do Anari, variável que não fazia parte do contexto fornecido ao modelo, o assistente respondeu que o painel não possuía dados sobre essa informação.

Esse comportamento demonstra a utilização do Prompt Engineering para limitar respostas sem sustentação nos dados disponibilizados pela aplicação.

---

## Fluxo dos Dados no Projeto

O fluxo consolidado pode ser representado da seguinte maneira:

`Fontes externas → Coleta → Arquivos processados → Integração → FastAPI → Análise/Modelagem → Streamlit → Usuário`

No caso do Assistente ESG:

`dados_integrados.csv → FastAPI → Pandas → fatos calculados → Prompt + memória → Groq → resposta em linguagem natural`

No caso da análise temática:

`noticias_mcom.csv → FastAPI → modelo local → categoria sugerida → Streamlit`

Essa estrutura permite utilizar diferentes tipos de dados e técnicas dentro do mesmo ciclo de Ciência de Dados.

---

## Relação entre Fontes, Processamento e Resultado

| Fonte | Processamento | Resultado na Aplicação |
|---|---|---|
| API SIDRA — acesso à internet | Coleta, limpeza e padronização | Indicador municipal de limitação de acesso digital |
| API SIDRA — renda | Coleta, limpeza e padronização | Indicador socioeconômico municipal |
| Bases municipais integradas | Junção pelo código IBGE e análises com Pandas | Comparações, métricas, visualizações e contexto do Assistente ESG |
| Notícias do Ministério das Comunicações | Web Scraping e tratamento textual | Página de notícias, análise de termos e dados para modelagem |
| Notícias rotuladas | Avaliação de modelos zero-shot | Escolha do modelo local utilizado pela aplicação |
| Histórico da conversa | Armazenamento temporário em `st.session_state` | Memória conversacional do Assistente ESG |
| Fatos calculados pela aplicação | Estruturação no prompt | Respostas contextualizadas do LLM |

---

## Considerações sobre os Dados

Os dados municipais utilizados são provenientes do Censo Demográfico 2022 e representam o período e as definições das tabelas selecionadas do IBGE.

Portanto, os resultados não devem ser interpretados como medidas em tempo real da situação dos municípios.

A associação entre acesso à internet e renda possui caráter descritivo e comparativo.

A presença de diferenças entre os indicadores não permite concluir, isoladamente, que uma variável seja causa da outra.

As notícias coletadas representam apenas o conteúdo disponível nas páginas e períodos selecionados do Ministério das Comunicações.

O banco de provas utilizado para avaliação do modelo local possui somente 30 exemplos e não representa todas as possibilidades temáticas existentes.

Da mesma forma, o Assistente ESG possui acesso somente aos fatos fornecidos pela aplicação. Perguntas que dependam de outras variáveis ou de fontes externas não podem ser respondidas com base no contexto atual.

---

## Papel dos Dados no Ciclo Completo de Ciência de Dados

A evolução do projeto demonstra a utilização dos dados em diferentes etapas:

1. **Obtenção:** API SIDRA e Web Scraping.
2. **Preparação:** limpeza, conversão de tipos e padronização.
3. **Integração:** associação das bases municipais pelo código IBGE.
4. **Exploração:** filtros, métricas, comparações e visualizações.
5. **Modelagem:** classificação temática de textos com modelo local.
6. **IA generativa:** interpretação dos indicadores com Prompt Engineering e memória conversacional.
7. **Apresentação:** dashboard Streamlit integrado à FastAPI.

Dessa forma, os dados coletados não são utilizados apenas para exibição. Eles percorrem todo o fluxo da aplicação e servem de base tanto para as análises quantitativas quanto para as funcionalidades de Inteligência Artificial.