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

Para cada notícia são