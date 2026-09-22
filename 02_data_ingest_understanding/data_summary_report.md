# Data Summary Report

## Visão Geral

Este documento apresenta um resumo inicial das fontes de dados previstas para o projeto Rede de Acesso, incluindo sua origem, principais variáveis e finalidade dentro da análise de inclusão digital e conectividade nos municípios brasileiros.

## Fontes de Dados

| Fonte | Conjunto de Dados | Abrangência | Uso no Projeto |
|---|---|---|---|
| IBGE - Censo Demográfico 2022 / SIDRA | Tabela 9936 - Domicílios particulares permanentes ocupados por existência de conexão domiciliar à Internet | Municípios brasileiros | Identificar a proporção de domicílios com e sem conexão domiciliar à internet |
| IBGE - Censo Demográfico 2022 / SIDRA | Tabela 10295 - Rendimento domiciliar mensal per capita médio e mediano | Municípios brasileiros | Representar a dimensão socioeconômica da análise |
| Anatel | Índice Brasileiro de Conectividade (IBC) | Municípios brasileiros | Analisar o estágio de desenvolvimento da infraestrutura e dos serviços de conectividade |

## Tipos de Dados

Os dados previstos para o projeto são predominantemente estruturados e tabulares, compostos por variáveis numéricas, categóricas e identificadoras.

| Tipo de dado | Exemplos no projeto | Finalidade |
|---|---|---|
| Identificador | Código IBGE do município | Permitir a integração entre diferentes bases de dados |
| Categórico | Nome do município e unidade da federação | Identificar e agrupar os municípios analisados |
| Numérico | Percentual ou quantidade de domicílios com acesso à internet | Medir o nível de acesso digital |
| Numérico | Rendimento domiciliar per capita | Representar a dimensão socioeconômica |
| Numérico | Indicador de infraestrutura/conectividade da Anatel | Representar as condições de infraestrutura digital |

## Finalidade dos Dados

Os dados serão usados de maneira integrada para permitir a comparação das condições de inclusão digital entre os municípios brasileiros.

- Os dados de acesso domiciliar à internet serão usados como principal indicador das limitações de acesso digital.
- Os dados de renda permitirão analisar a relação entre condições socioeconômicas e acesso à internet.
- Os indicadores da Anatel serão empregados para representar as condições de infraestrutura e disponibilidade de conectividade nos municípios.
- A integração das bases pelo código IBGE do município permitirá comparar os indicadores territorialmente e identificar localidades que possam demandar maior atenção em iniciativas de inclusão digital.

## Resumo da Coleta Inicial

Foram realizadas duas coletas iniciais por meio da API SIDRA do IBGE, utilizando dados do Censo Demográfico 2022.

### Acesso à Internet

A primeira coleta utilizou a Tabela 9936 para obter o percentual de domicílios particulares permanentes ocupados sem conexão domiciliar à internet.

Após o tratamento dos dados, a base resultante apresenta:

- 5.570 municípios;
- código IBGE do município;
- nome do município;
- percentual de domicílios sem conexão domiciliar à internet.

### Renda

A segunda coleta utilizou a Tabela 10295 para obter o rendimento nominal mediano mensal domiciliar per capita.

Após o tratamento dos dados, a base resultante apresenta:

- 5.570 municípios;
- código IBGE do município;
- nome do município;
- rendimento mediano domiciliar per capita.

### Integração Inicial

As duas bases foram integradas utilizando o código IBGE do município como chave. A integração resultou em uma base consolidada com 5.570 municípios e sem valores ausentes nas variáveis utilizadas nesta etapa.


## Observações Iniciais

As fontes selecionadas apresentam diferentes estruturas e formas de disponibilização, o que exigirá uma etapa de padronização antes da integração dos dados.

Essa integração entre as bases deverá utilizar preferencialmente o código IBGE do município como a chave de identificação, evitando inconsistências relacionadas à grafia dos nomes dos municípios.

Também será necessário verificar a compatibilidade temporal entre os indicadores utilizados, uma vez que as bases podem apresentar anos de referência diferentes.

Nesta etapa inicial, o projeto não pretende estabelecer relações de causalidade entre renda, infraestrutura e acesso digital, mas identificar padrões, diferenças territoriais e possíveis associações entre estes indicadores.