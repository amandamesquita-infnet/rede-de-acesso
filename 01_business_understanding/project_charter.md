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
- coleta de notícias por Web Scraping utilizando Requests e Beautiful Soup;
- análise textual das notícias por meio de nuvem de palavras e frequência de termos;
- upload de arquivos CSV com informações complementares;
- integração dos dados enviados pelo usuário à base principal;
- download dos dados filtrados e processados;
- desenvolvimento da aplicação em Streamlit;
- utilização de Git e GitHub para controle de versão do projeto;
- organização da aplicação em múltiplas páginas com navegação entre funcionalidades;
- desenvolvimento de uma API com FastAPI para disponibilização dos dados processados;
- integração entre a aplicação Streamlit e a API desenvolvida;
- centralização das requisições HTTP realizadas pelo Streamlit;
- tratamento da indisponibilidade temporária da API.

O projeto possui caráter descritivo e comparativo. Nesta etapa, não busca estabelecer relações de causa e efeito entre renda e acesso à internet.

Novos indicadores de infraestrutura e qualidade da conectividade poderão ser incorporados em etapas futuras.

---

## Público-Alvo

O público-alvo principal da aplicação é formado por analistas e gestores públicos envolvidos em áreas como inclusão digital, desenvolvimento social e conectividade.

A aplicação pode auxiliar na comparação de indicadores entre municípios e na identificação de localidades que apresentam maiores limitações de acesso digital.

---

## Stakeholders

- gestores públicos;
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
| Incorporar uma nova fonte de dados | Coleta de notícias por Web Scraping com Requests e Beautiful Soup |
| Ampliar a coleta textual | Coleta de notícias de outubro e novembro de 2026 com tratamento de paginação |
| Apresentar informações obtidas no Web Scraping | Tabela de notícias, nuvem de palavras e frequência de termos |
| Permitir a entrada de novos dados | Upload de arquivo CSV com validação e integração pelo código IBGE |
| Permitir a saída dos dados processados | Download dos dados filtrados em formato CSV |
| Manter o histórico de desenvolvimento | Projeto versionado com Git e disponibilizado no GitHub |
| Organizar as funcionalidades da aplicação | Navegação entre múltiplas páginas no Streamlit |
| Disponibilizar os dados processados por API | API FastAPI funcional com endpoints GET e POST |
| Integrar a aplicação à API | Consultas à FastAPI realizadas diretamente pela aplicação Streamlit |
| Reduzir acoplamento entre interface e dados | Chamadas HTTP centralizadas em `src/cliente_api.py` |
| Melhorar a robustez da interface | Mensagem amigável quando a FastAPI está indisponível |

---

## ODS

### ODS 9 - Indústria, Inovação e Infraestrutura

O projeto está principalmente relacionado ao ODS 9 por analisar diferenças no acesso à internet entre municípios brasileiros. A conectividade digital depende da existência e do desenvolvimento de infraestrutura tecnológica, e identificar localidades com maiores limitações de acesso pode contribuir para compreender onde essas diferenças são mais significativas.

### ODS 10 - Redução das Desigualdades

O projeto também se relaciona ao ODS 10 por comparar o acesso à internet com indicadores de renda. Diferenças no acesso às tecnologias digitais podem estar associadas a desigualdades no acesso a informações, serviços e oportunidades.

---

## Atualizações para o TP3

### Reavaliação do problema de negócio

O problema de negócio permanece:

> Quais municípios brasileiros apresentam maiores limitações de acesso digital e como essa condição se relaciona com indicadores de renda?

A inclusão das novas tecnologias no TP3 não altera o problema central do projeto. As mudanças realizadas ampliam a forma de organização, disponibilização e consumo das informações, mantendo o foco nos indicadores de inclusão digital e renda.

### Evolução da aplicação

Nesta etapa, a aplicação foi reorganizada em várias páginas utilizando os recursos `st.navigation` e `st.Page` do Streamlit.

As funcionalidades foram distribuídas entre páginas específicas para:

- apresentação do projeto;
- análise dos indicadores municipais;
- exploração das notícias coletadas;
- upload e download de dados complementares;
- integração e testes da API.

Também foi desenvolvida uma API com FastAPI para disponibilizar os dados processados de forma estruturada.

A API possui endpoints para:

- verificar o funcionamento do serviço;
- listar os municípios disponíveis;
- consultar um município por código IBGE;
- disponibilizar as notícias coletadas;
- comparar municípios por meio de uma requisição POST.

A interface Streamlit passou a consumir esses dados pela FastAPI, reduzindo o acesso direto das páginas aos arquivos internos do projeto.

As chamadas HTTP foram centralizadas no arquivo:

`src/cliente_api.py`

A estrutura adotada pode ser representada de forma simplificada como:

`Streamlit → cliente_api.py → FastAPI → dados processados`

### Configuração da API