# Data Summary Report

## Visão Geral

Este documento apresenta as principais fontes de dados utilizadas no projeto **Rede de Acesso**, explicando a origem dos dados, as principais variáveis e como cada fonte é utilizada na aplicação.

Nesta etapa, o projeto utiliza dados do Censo Demográfico 2022, obtidos por meio da API SIDRA do IBGE, além de notícias coletadas da página do Ministério das Comunicações por meio de Web Scraping.

A aplicação também permite que o usuário envie um arquivo CSV com informações complementares sobre os municípios.


## Fontes de Dados

| Fonte | Conjunto de Dados | Abrangência | Forma de Obtenção | Uso no Projeto |
|---|---|---|---|---|
| IBGE - Censo Demográfico 2022 / SIDRA | Tabela 9936 - Domicílios particulares permanentes ocupados por existência de conexão domiciliar à Internet | 5.570 municípios brasileiros | API SIDRA | Identificar o percentual de domicílios sem conexão domiciliar à internet |
| IBGE - Censo Demográfico 2022 / SIDRA | Tabela 10295 - Rendimento domiciliar mensal per capita médio e mediano | 5.570 municípios brasileiros | API SIDRA | Representar a dimensão socioeconômica da análise |
| Ministério das Comunicações | Página de notícias do Ministério das Comunicações | Notícias relacionadas a telecomunicações, internet e conectividade | Web Scraping com Beautiful Soup | Acrescentar informações textuais ao projeto e analisar os termos mais frequentes nas notícias |
| Arquivo enviado pelo usuário | CSV com dados complementares | Depende do arquivo enviado | Upload pelo Streamlit | Permitir que novas informações sejam associadas aos municípios da base principal |


## Tipos de Dados

O projeto trabalha com dados estruturados, como os dados municipais do IBGE, e também com dados textuais obtidos pelas notícias.

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


## Finalidade dos Dados

Os dados do IBGE são utilizados para comparar as condições de acesso à internet e renda entre os municípios brasileiros.

O percentual de domicílios sem conexão domiciliar à internet é utilizado como o principal indicador de limitação de acesso digital. A renda mediana domiciliar per capita permite acrescentar uma dimensão socioeconômica à comparação entre os municípios.

As duas bases são integradas pelo código IBGE do município.

As notícias coletadas por Web Scraping complementam os dados numéricos do projeto. A partir dos títulos e resumos das notícias, a aplicação apresenta uma nuvem de palavras e os termos mais frequentes encontrados na coleta.

Além disso, o usuário pode enviar um arquivo CSV com novas informações. Para que essas informações sejam integradas à base principal, o arquivo deve conter a coluna `codigo_ibge`.


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

`dados_integrados.csv`

A base integrada contém os 5.570 municípios brasileiros e não apresenta valores ausentes nas variáveis utilizadas no projeto.


## Coleta por Web Scraping

No TP2, também foi adicionada uma coleta de dados por Web Scraping.

A coleta é realizada na página de notícias do **Ministério das Comunicações**, utilizando as bibliotecas `requests` e `BeautifulSoup`.

O processo é executado pelo arquivo:

`coleta_noticias_mcom.py`

Para cada notícia são coletados:

- título;
- data;
- resumo;
- link.

Na coleta realizada para o projeto, foram obtidas **30 notícias**.

O resultado é salvo no arquivo:

`noticias_mcom.csv`

A coleta é executada separadamente do Streamlit. Dessa forma, o site não precisa ser acessado novamente toda vez que o usuário interage com a aplicação. O aplicativo apenas lê o arquivo CSV gerado anteriormente.


## Uso das Notícias na Aplicação

As notícias coletadas são apresentadas em uma seção específica do aplicativo.

A aplicação mostra:

- quantidade de notícias coletadas;
- data da notícia mais recente;
- tabela com título, data, resumo e link;
- nuvem de palavras;
- gráfico com os termos mais frequentes.

Para a análise textual, palavras muito comuns da língua portuguesa são retiradas para que os termos mais relevantes apareçam com maior destaque.


## Dados Complementares Enviados pelo Usuário

A aplicação também permite que o usuário envie um arquivo CSV com informações adicionais sobre os municípios.

O arquivo precisa conter obrigatoriamente a coluna:

`codigo_ibge`

Antes de utilizar os dados, a aplicação verifica se:

- o arquivo pode ser lido;
- o arquivo possui registros;
- a coluna `codigo_ibge` está presente;
- existe pelo menos uma coluna adicional.

Quando o arquivo é válido, as novas informações são associadas à base principal por meio do código IBGE.

Os dados enviados são mantidos no `st.session_state` durante a sessão do usuário.

Também é possível baixar um novo arquivo CSV com os dados da unidade da federação selecionada, incluindo as informações complementares quando elas tiverem sido adicionadas pelo usuário.


## Tratamento dos Dados

O código IBGE é mantido como texto para preservar sua função como identificador e facilitar a integração entre as bases.

A unidade da federação é extraída do campo de município e utilizada nos filtros da aplicação.

Na coleta das notícias, possíveis registros duplicados são removidos utilizando o link como referência. As datas também são tratadas antes da ordenação e exibição.

O script de Web Scraping também verifica se alguma notícia foi encontrada antes de gerar o arquivo final.


## Limitações

Os dados de acesso à internet e renda utilizados no projeto são referentes ao Censo Demográfico 2022.

As notícias representam o conteúdo disponível na página do Ministério das Comunicações no momento da coleta. Caso a estrutura da página seja alterada, o código de Web Scraping também poderá precisar de ajustes.

Os arquivos enviados pelos usuários podem ter diferentes tipos de informação. Por isso, a aplicação realiza apenas validações básicas e utiliza o código IBGE como chave para integração.

O projeto tem caráter descritivo e comparativo. Portanto, as relações observadas entre renda e acesso à internet não são tratadas como relações de causa e efeito.


## Expansões Futuras

Uma possível expansão do projeto é acrescentar dados da **Anatel** relacionados à infraestrutura e à qualidade da conectividade nos municípios.

Esses indicadores poderiam complementar os dados de acesso à internet e renda já utilizados.

Os dados da Anatel ainda não foram integrados nesta etapa do projeto.