# Escolha do Modelo Local

## Objetivo

No TP4 do projeto **Rede de Acesso**, foi definida uma tarefa de classificação temática das notícias coletadas do Ministério das Comunicações.

O objetivo é receber um texto relacionado às notícias do projeto e classificá-lo em uma das seguintes categorias:

- `RADIODIFUSAO`
- `CONECTIVIDADE_INFRAESTRUTURA`
- `ENDERECAMENTO_CORREIOS`
- `INCLUSAO_CAPACITACAO_DIGITAL`
- `USO_E_SETOR_DE_TELECOMUNICACOES`
- `GESTAO_POLITICAS_PUBLICAS`

A escolha do modelo foi realizada considerando desempenho no próprio conjunto de dados do projeto, custo computacional local e possibilidade de execução sem dependência de serviços de nuvem.

---

## Ambiente de Teste

Os testes foram realizados localmente no seguinte equipamento:

- **CPU:** Intel Core i5-12450HX
- **Memória RAM:** 31,73 GB
- **GPU:** NVIDIA GeForce RTX 3050 Laptop GPU
- **Memória da GPU:** 6 GB
- **PyTorch:** 2.11.0+cu128
- **CUDA disponível no PyTorch:** sim

A GPU foi reconhecida pelo PyTorch e utilizada durante os testes dos modelos.

---

## Banco de Provas

Para comparar os modelos, foi criado o arquivo:

`03_modeling/banco_de_provas.csv`

O banco contém **30 exemplos reais** retirados das notícias coletadas pelo projeto.

Os exemplos foram rotulados manualmente antes da execução dos modelos.

Foram utilizados cinco exemplos para cada uma das seis categorias, resultando em uma distribuição equilibrada:

| Categoria | Quantidade |
|---|---:|
| RADIODIFUSAO | 5 |
| CONECTIVIDADE_INFRAESTRUTURA | 5 |
| ENDERECAMENTO_CORREIOS | 5 |
| INCLUSAO_CAPACITACAO_DIGITAL | 5 |
| USO_E_SETOR_DE_TELECOMUNICACOES | 5 |
| GESTAO_POLITICAS_PUBLICAS | 5 |
| **Total** | **30** |

O mesmo banco de provas foi utilizado para avaliar os dois modelos candidatos.

---

## Modelos Avaliados

Foram avaliados dois modelos multilíngues voltados à classificação zero-shot.

### Modelo 1

`MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`

O modelo foi executado localmente utilizando a GPU NVIDIA disponível na máquina.

### Modelo 2

`MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli`

Este modelo também foi executado localmente com GPU e submetido exatamente aos mesmos 30 exemplos e às mesmas categorias.

---

## Procedimento de Avaliação

Os dois modelos receberam:

- o mesmo banco de provas;
- as mesmas seis categorias possíveis;
- o mesmo texto de hipótese para classificação zero-shot;
- o mesmo ambiente de hardware.

Foram registrados:

- quantidade de acertos;
- acurácia total;
- desempenho por categoria;
- tempo de carregamento;
- tempo total de inferência;
- tempo médio por notícia;
- pico de memória CUDA utilizado durante a inferência.

O primeiro download dos modelos não foi considerado como tempo normal de carregamento. Após os arquivos estarem disponíveis localmente, os modelos foram executados novamente para obter uma comparação mais justa.

---

## Resultados

| Métrica | Modelo 1 - mDeBERTa | Modelo 2 - MiniLMv2 |
|---|---:|---:|
| Acertos | 8/30 | 14/30 |
| Acurácia | 26,67% | **46,67%** |
| Tempo de carregamento local | 3,67 s | 3,85 s |
| Tempo total de inferência | 7,37 s | **2,04 s** |
| Tempo médio por notícia | 0,25 s | **0,07 s** |
| Pico de memória CUDA | 556,00 MB | **418,71 MB** |

### Resultado por categoria

#### Modelo 1 - mDeBERTa

| Categoria | Acertos |
|---|---:|
| RADIODIFUSAO | 2/5 |
| CONECTIVIDADE_INFRAESTRUTURA | 2/5 |
| ENDERECAMENTO_CORREIOS | 0/5 |
| INCLUSAO_CAPACITACAO_DIGITAL | 0/5 |
| USO_E_SETOR_DE_TELECOMUNICACOES | 0/5 |
| GESTAO_POLITICAS_PUBLICAS | 4/5 |

#### Modelo 2 - MiniLMv2

| Categoria | Acertos |
|---|---:|
| RADIODIFUSAO | 2/5 |
| CONECTIVIDADE_INFRAESTRUTURA | 1/5 |
| ENDERECAMENTO_CORREIOS | 2/5 |
| INCLUSAO_CAPACITACAO_DIGITAL | 3/5 |
| USO_E_SETOR_DE_TELECOMUNICACOES | 3/5 |
| GESTAO_POLITICAS_PUBLICAS | 3/5 |

---

## Modelo Escolhido

O modelo selecionado para integração ao projeto foi:

`MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli`

A escolha foi baseada nos resultados obtidos no banco de provas do próprio projeto.

O MiniLMv2 apresentou:

- maior acurácia geral;
- melhor distribuição de acertos entre as categorias;
- menor tempo de inferência;
- menor consumo de memória da GPU;
- tempo de carregamento semelhante ao modelo maior.

A acurácia de 46,67% ainda demonstra que a classificação possui limitações e que as pontuações produzidas pelo modelo não devem ser interpretadas como garantia de acerto.

Entretanto, entre os candidatos avaliados, o MiniLMv2 apresentou a melhor relação entre desempenho e custo computacional para a tarefa definida.

---

## Compatibilidade com o Ambiente Local

O modelo escolhido funcionou utilizando a NVIDIA GeForce RTX 3050 com 6 GB de VRAM.

Durante o benchmark, o pico de memória CUDA foi de aproximadamente **418,71 MB**, permanecendo abaixo da capacidade disponível na GPU.

O tempo médio de inferência foi de aproximadamente **0,07 segundo por notícia** no banco utilizado.

Esses resultados indicam que o modelo é compatível com os recursos computacionais disponíveis para o projeto.

---

## Execução Local

O modelo será utilizado pela FastAPI a partir de arquivos disponíveis localmente.

A arquitetura prevista é:

`Streamlit → FastAPI → modelo local`

O download do modelo será realizado separadamente da inicialização da API.

Após o download, a aplicação deverá carregar o modelo a partir do armazenamento local, evitando depender de conexão com serviços de nuvem durante a inferência.

O modelo também deverá ser carregado uma única vez durante o ciclo de vida da FastAPI, evitando que os pesos sejam recarregados a cada requisição.

---

## Limitações

O banco de provas contém apenas 30 exemplos.

Embora a distribuição entre categorias seja equilibrada, esse conjunto ainda é pequeno para representar todas as possibilidades existentes nas notícias do Ministério das Comunicações.

Além disso, algumas notícias podem apresentar mais de um tema ao mesmo tempo, enquanto o benchmark utiliza apenas uma categoria esperada para cada texto.

Os resultados devem, portanto, ser interpretados como uma avaliação prática para a escolha do modelo dentro do escopo do TP4, e não como uma avaliação definitiva da capacidade dos modelos.

---

## Plano B

Caso o modelo escolhido não possa ser carregado durante a execução da aplicação, a API deverá permanecer disponível para as demais funcionalidades.

Nesse cenário, somente a funcionalidade de processamento de texto deverá retornar uma resposta de indisponibilidade do modelo.

O modelo `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` permanece registrado como alternativa avaliada, embora tenha apresentado desempenho inferior no banco de provas utilizado.