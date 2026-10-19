# Project Charter

## Nome do Projeto

Rede de Acesso

### Subtítulo

Radar de Inclusão Digital e Conectividade nos Municípios Brasileiros

---

## Problema de Negócio

O acesso à internet e aos recursos digitais ainda ocorre de forma desigual entre os municípios brasileiros. Enquanto algumas localidades apresentam maior acesso, outras possuem limitações que podem dificultar o uso de informações, serviços públicos, oportunidades educacionais e profissionais disponíveis em meios digitais.

Além disso, fatores socioeconômicos, como a renda, podem estar relacionados a essas diferenças. Os dados necessários para observar esse cenário encontram-se distribuídos em diferentes fontes, o que dificulta a comparação entre os municípios.

O projeto **Rede de Acesso** busca reunir e organizar essas informações em uma aplicação interativa, permitindo comparar municípios brasileiros a partir de indicadores de acesso à internet e renda.

A análise é orientada pela seguinte questão:

**Quais municípios brasileiros apresentam maiores limitações de acesso digital e como essa condição se relaciona com indicadores de renda?**

---

## Objetivo Geral

Desenvolver uma aplicação interativa em Python com Streamlit que integre indicadores de acesso à internet e renda, permitindo explorar e comparar as condições de inclusão digital entre municípios brasileiros.

A aplicação também busca complementar essa análise com informações relacionadas à conectividade coletadas por Web Scraping e permitir que o usuário acrescente novos dados por meio do upload de arquivos CSV.

---

## Escopo

O projeto Rede de Acesso contempla:

- coleta de dados públicos relacionados ao acesso domiciliar à internet;
- coleta de indicadores socioeconômicos relacionados à renda;
- integração das bases utilizando o código IBGE dos municípios;
- comparação dos indicadores entre municípios e unidades da federação;
- desenvolvimento de filtros interativos para exploração dos dados;
- coleta de notícias por Web Scraping utilizando Beautiful Soup;
- análise textual das notícias por meio de nuvem de palavras e frequência de termos;
- upload de arquivos CSV com informações complementares;
- integração dos dados enviados pelo usuário à base principal;
- download dos dados filtrados e processados;
- desenvolvimento da aplicação em Streamlit;
- utilização de Git e GitHub para controle de versão do projeto;
- organização da aplicação em múltiplas páginas com navegação entre funcionalidades;
- desenvolvimento de uma API com FastAPI para disponibilização dos dados processados;
- integração entre a aplicação Streamlit e a API desenvolvida.

O projeto possui caráter descritivo e comparativo. Nesta etapa, não busca estabelecer relações de causa e efeito entre renda e acesso à internet.

Novos indicadores de infraestrutura e qualidade da conectividade poderão ser incorporados em etapas futuras.

---

## Público-Alvo

O público-alvo principal da aplicação é formado por analistas e gestores públicos envolvidos em áreas como inclusão digital, desenvolvimento social e conectividade.

A aplicação pode auxiliar na comparação de indicadores entre municípios e na identificação de localidades que apresentam maiores limitações de acesso digital.

---

## Stakeholders

- Gestores públicos;
- analistas de políticas públicas;
- órgãos relacionados à inclusão digital e telecomunicações;
- organizações ligadas ao desenvolvimento social;
- populações dos municípios analisados.

---

## Metas e Indicadores de Sucesso

| Meta | Indicador de Sucesso |
|---|---|
| Integrar dados públicos relacionados à inclusão digital | Base consolidada com dados dos municípios brasileiros |
| Analisar diferenças de acesso digital | Presença de indicador municipal de domicílios sem conexão à internet |
| Incorporar uma dimensão socioeconômica | Presença de indicador de renda mediana per capita |
| Possibilitar análise territorial | Filtros por unidade da federação e município |
| Disponibilizar os resultados de forma interativa | Aplicação funcional desenvolvida em Streamlit |
| Incorporar uma nova fonte de dados | Coleta de notícias por Web Scraping com Beautiful Soup |
| Apresentar informações obtidas no Web Scraping | Tabela de notícias, nuvem de palavras e frequência de termos |
| Permitir a entrada de novos dados | Upload de arquivo CSV com validação e integração pelo código IBGE |
| Permitir a saída dos dados processados | Download dos dados filtrados em formato CSV |
| Manter o histórico de desenvolvimento | Projeto versionado com Git e disponibilizado no GitHub |
| Organizar as funcionalidades da aplicação | Navegação entre múltiplas páginas no Streamlit |
| Disponibilizar os dados processados por API | API FastAPI funcional com endpoints GET e POST |
| Integrar a aplicação à API | Consultas à FastAPI realizadas diretamente pela aplicação Streamlit |

---

## ODS

### ODS 9 - Indústria, Inovação e Infraestrutura

O projeto está principalmente relacionado ao ODS 9 por analisar diferenças no acesso à internet entre municípios brasileiros. A conectividade digital depende da existência e do desenvolvimento de infraestrutura tecnológica, e identificar localidades com maiores limitações de acesso pode contribuir para compreender onde essas diferenças são mais significativas.

### ODS 10 - Redução das Desigualdades

O projeto também se relaciona ao ODS 10 por comparar o acesso à internet com indicadores de renda. Diferenças no acesso às tecnologias digitais podem estar associadas a desigualdades no acesso a informações, serviços e oportunidades.

## Atualizações para o TP3

### Reavaliação do problema de negócio

O problema de negócio permanece:

> Quais municípios brasileiros apresentam maiores limitações de acesso digital e como essa condição se relaciona com indicadores de renda?

A inclusão de novas tecnologias no TP3 não altera o problema central do projeto. As mudanças feitas ampliam a forma de acesso e organização das informações do projeto, permitindo que os dados processados também sejam consultados por meio de uma API.

### Evolução da aplicação

Nesta etapa, a aplicação foi reorganizada em várias páginas utilizando os recursos `st.navigation` e `st.Page` do Streamlit.

As funcionalidades foram distribuídas entre páginas específicas para:

- apresentação do projeto;
- análise dos indicadores municipais;
- exploração das notícias coletadas;
- upload e download de dados complementares;
- integração com a API do projeto.

Também desenvolvemos uma API com FastAPI para disponibilizar os indicadores processados de forma estruturada. A API possui endpoints para consulta individual de municípios e comparação entre municípios e foi integrada à aplicação Streamlit.

### Avaliação do uso de Selenium

Analisamos a necessidade de utilização do Selenium para a coleta de dados. Mas, as fontes atualmente utilizadas pelo projeto não exigem interação dinâmica com páginas web. Os indicadores do IBGE são obtidos por meio de API, enquanto as notícias do Ministério das Comunicações podem ser coletadas diretamente do HTML da página utilizando Requests e Beautiful Soup.

Por esse motivo, o Selenium não foi usado nesta etapa. Com isso, tentamos manter o processo de coleta mais simples e reduzir dependências e fragilidade desnecessárias, utilizando cada tecnologia de acordo com a característica da fonte de dados.

### Preparação para uso futuro de LLM

Em uma etapa futura, pretendo integrar um modelo de linguagem ao projeto para gerar resumos interpretativos dos indicadores de um município selecionado. O modelo poderá usar informações como percentual de domicílios sem acesso à internet, renda mediana per capita e comparação com os indicadores da respectiva unidade da federação para produzir uma síntese textual dos dados.

A geração deverá seguir descritiva, evitando atribuir relações causais que não possam ser demonstradas pelos dados disponíveis.