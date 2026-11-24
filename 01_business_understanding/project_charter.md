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

### Configuração da API

O endereço utilizado pela aplicação Streamlit para acessar a FastAPI é centralizado no arquivo `config.py`.

Por padrão, a API é executada localmente em:

`http://127.0.0.1:8000`

A configuração também permite utilizar a variável de ambiente `REDE_API_URL`, evitando que o endereço da API fique repetido em diferentes arquivos do projeto.

Essa organização facilita alterações futuras no ambiente de execução e reduz o acoplamento entre a interface e a camada responsável pela disponibilização dos dados.

---

## Atualizações para o TP4

### Aplicação de modelo local

No TP4, o projeto passou a incorporar uma etapa de modelagem utilizando um modelo de linguagem natural executado localmente.

A funcionalidade implementada realiza classificação temática zero-shot de textos relacionados ao contexto de conectividade e inclusão digital.

Antes da escolha do modelo definitivo, foram avaliados dois modelos multilíngues utilizando um banco de provas composto por 30 notícias reais coletadas pelo próprio projeto:

- `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`;
- `MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli`.

Os modelos foram comparados utilizando o mesmo conjunto de textos e as mesmas categorias. Foram considerados a acurácia obtida no banco de provas, o tempo de inferência e o consumo de memória da GPU.

O modelo selecionado foi:

`MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli`

A escolha foi baseada no melhor equilíbrio entre desempenho no banco de provas e custo computacional na máquina utilizada para desenvolvimento.

A classificação produzida pelo modelo é apresentada na aplicação como uma sugestão temática, e não como uma classificação definitiva, considerando as limitações observadas durante a avaliação.

### Evolução da arquitetura

O modelo é carregado pela FastAPI e utilizado por meio do endpoint responsável pelo processamento de textos.

O Streamlit não carrega diretamente os pesos do modelo. A interface envia o texto à API e apresenta a resposta retornada pelo serviço.

A arquitetura pode ser representada de forma simplificada como:

`Streamlit → cliente_api.py → FastAPI → modelo local → resultado`

Essa separação mantém a interface desacoplada da camada de modelagem e permite que as demais funcionalidades da API continuem disponíveis mesmo quando o modelo local não pode ser carregado.

---

## Atualizações para o TP5

### Evolução do problema de negócio

O problema central do projeto permanece:

> Quais municípios brasileiros apresentam maiores limitações de acesso digital e como essa condição se relaciona com indicadores de renda?

No TP5, a solução foi ampliada para permitir que os resultados quantitativos sejam explorados também por meio de linguagem natural.

A nova funcionalidade não substitui as análises e visualizações existentes. Seu objetivo é facilitar a interpretação dos indicadores e permitir que o usuário realize perguntas sucessivas sobre os dados, preservando o contexto da conversa.

### Assistente ESG com memória conversacional

Foi incorporado ao dashboard um **Assistente ESG com memória conversacional**, utilizando um modelo de linguagem acessado pela API da Groq.

A memória da conversa é mantida durante a sessão do usuário por meio do `st.session_state` do Streamlit.

Essa implementação permite que o sistema compreenda perguntas dependentes de interações anteriores. Por exemplo, após identificar um município em uma primeira pergunta, o usuário pode realizar uma nova consulta utilizando expressões como “dele” ou “desse município”, sem precisar repetir o nome da localidade.

Para evitar o crescimento indefinido do contexto enviado ao modelo, é utilizada uma janela com as interações mais recentes.

### Uso dos dados do projeto

Os valores utilizados pelo Assistente ESG não são calculados pelo modelo de linguagem.

A aplicação utiliza Python e Pandas para calcular previamente informações como:

- média do percentual de domicílios sem internet na unidade da federação selecionada;
- mediana da renda per capita;
- município com maior e menor percentual de domicílios sem internet;
- município com maior e menor renda mediana per capita.

Os resultados calculados são transformados em um contexto estruturado e enviados ao modelo de linguagem.

Dessa forma, a IA é utilizada principalmente para interpretar os fatos, manter o contexto conversacional e apresentar os resultados em linguagem natural.

Essa abordagem reduz o risco de delegar ao LLM operações determinísticas que podem ser executadas diretamente pelo código da aplicação.

### Prompt Engineering

O Assistente ESG utiliza um prompt de sistema criado especificamente para o contexto do projeto.

As principais instruções definidas no prompt são:

- responder em português;
- utilizar exclusivamente os fatos fornecidos pela aplicação;
- não inventar municípios, indicadores ou valores;
- não recalcular ou alterar os valores obtidos pelo código Python;
- evitar interpretações causais que não possam ser sustentadas pelos dados;
- informar explicitamente quando a informação solicitada não estiver disponível;
- relacionar os resultados aos ODS quando isso for pertinente.

A estratégia foi validada durante os testes da aplicação.

Em uma interação com os dados de Rondônia, o assistente identificou **Vale do Anari** como o município com maior percentual de domicílios sem internet no contexto apresentado.

Em seguida, ao receber apenas a pergunta **“E qual é a renda dele?”**, o sistema preservou o contexto da conversa e respondeu com a renda correspondente ao mesmo município.

Em outro teste, ao ser questionado sobre a população de Vale do Anari, informação não fornecida ao modelo, o assistente informou que o painel não possuía esse dado, em vez de produzir um valor não sustentado pelo contexto.

### Segurança da chave da API

A chave utilizada para acesso à API da Groq é armazenada localmente no arquivo `.env`.

O arquivo está incluído no `.gitignore` e não é enviado ao repositório público.

A aplicação acessa a chave por meio da variável de ambiente `GROQ_API_KEY`.

Essa estrutura permite manter a credencial separada do código-fonte.

### Ciclo completo de Ciência de Dados

Com as funcionalidades incorporadas ao longo do projeto, o fluxo do **Rede de Acesso** pode ser representado da seguinte forma:

`Coleta → Tratamento → Integração → Análise → Modelagem/IA → Interpretação → Visualização e interação`

O ciclo contempla:

1. **Coleta:** obtenção de indicadores municipais por meio da API SIDRA do IBGE e coleta de notícias por Web Scraping.
2. **Tratamento:** limpeza, padronização e preparação das bases.
3. **Integração:** associação dos dados municipais por meio do código IBGE.
4. **Análise:** cálculo e comparação dos indicadores de acesso à internet e renda.
5. **Modelagem:** aplicação de modelo local para classificação temática de textos.
6. **IA generativa:** utilização de LLM com Prompt Engineering e memória conversacional.
7. **Apresentação:** disponibilização dos resultados por meio de dashboard interativo em Streamlit, FastAPI, visualizações e Assistente ESG.

### Relação com ESG e ODS

A solução está associada à dimensão social de ESG ao permitir identificar e explorar diferenças territoriais de acesso digital e renda.

A inclusão digital pode influenciar a capacidade de acesso a informações, educação, serviços e oportunidades disponibilizadas por meios digitais.

O projeto se relaciona principalmente aos seguintes Objetivos de Desenvolvimento Sustentável:

- **ODS 4 — Educação de Qualidade:** a conectividade pode ser relevante para o acesso a conteúdos, plataformas e recursos educacionais digitais;
- **ODS 9 — Indústria, Inovação e Infraestrutura:** a análise aborda diretamente a disponibilidade de conectividade digital como componente da infraestrutura tecnológica;
- **ODS 10 — Redução das Desigualdades:** a comparação entre acesso à internet e renda permite observar diferenças socioeconômicas e territoriais entre os municípios.

O projeto mantém caráter descritivo e comparativo. Os resultados não são utilizados para estabelecer relações causais entre renda, conectividade ou outros fatores.

### Contribuição para o problema de negócio

A solução final reúne em uma única aplicação dados públicos, análises quantitativas, informações textuais, modelo local e uma interface conversacional.

Para analistas e gestores, o dashboard permite identificar localidades com maiores limitações de acesso digital, comparar indicadores socioeconômicos e explorar os resultados por meio de perguntas em linguagem natural.

A inclusão do Assistente ESG busca reduzir a barreira entre o dado estruturado e sua interpretação, sem substituir os indicadores originais nem os cálculos realizados pela aplicação.

---

## Metas e Indicadores de Sucesso Atualizados para o TP5

| Meta | Indicador de Sucesso |
|---|---|
| Demonstrar o ciclo completo de Ciência de Dados | Fluxo documentado da coleta à apresentação dos resultados |
| Utilizar dados reais no processo analítico | Indicadores municipais obtidos da API SIDRA e notícias coletadas por Web Scraping |
| Incorporar IA ao dashboard | Modelo local e Assistente ESG disponíveis na aplicação Streamlit |
| Implementar memória conversacional | Perguntas sucessivas preservam o contexto da interação |
| Aplicar Prompt Engineering | Prompt restringe respostas aos fatos disponibilizados pela aplicação |
| Reduzir respostas sem sustentação nos dados | Assistente informa quando determinada informação não está disponível |
| Manter cálculos determinísticos fora do LLM | Indicadores e comparações calculados previamente com Python e Pandas |
| Relacionar a solução a ESG e ODS | Resultados interpretados no contexto de inclusão digital e ODS 4, 9 e 10 |
| Manter uma experiência de uso simples | Navegação multipágina, filtros, indicadores e interface de chat integrados ao dashboard |
| Preservar a segurança das credenciais | Chave da Groq armazenada em `.env` e excluída do versionamento |