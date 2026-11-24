import os

import pandas as pd
import requests
import streamlit as st

from dotenv import load_dotenv
from src.cliente_api import listar_municipios


# Carrega a chave da Groq do arquivo .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = (
    "https://api.groq.com/openai/v1/chat/completions"
)

MODELO_GROQ = "openai/gpt-oss-20b"


st.title("Assistente ESG")

st.write(
    """
    Converse com o assistente sobre os indicadores de inclusão
    digital e renda dos municípios brasileiros.

    Os cálculos são realizados com os dados do projeto em Python.
    O modelo de linguagem é utilizado para interpretar os resultados
    e manter o contexto da conversa.
    """
)


# Verifica se a chave foi configurada
if not GROQ_API_KEY:
    st.error(
        "A chave GROQ_API_KEY não foi encontrada. "
        "Verifique o arquivo .env."
    )
    st.stop()


# Consulta os dados pela FastAPI
try:
    dados_api = listar_municipios()

except requests.exceptions.RequestException:
    st.error(
        "Não foi possível conectar à API. "
        "Verifique se a FastAPI está em execução."
    )
    st.stop()


df = pd.DataFrame(
    dados_api["municipios"]
)


# Separa UF e nome do município
df["uf"] = df["municipio"].str.extract(
    r" - ([A-Z]{2})$"
)

df["municipio_nome"] = df["municipio"].str.replace(
    r" - [A-Z]{2}$",
    "",
    regex=True
)


# Seleção da UF
ufs = sorted(
    df["uf"]
    .dropna()
    .unique()
)


uf_selecionada = st.selectbox(
    "Selecione uma UF para o contexto da análise",
    ufs
)


df_uf = df[
    df["uf"] == uf_selecionada
].copy()


# Cálculos feitos em Python
media_sem_internet = (
    df_uf["percentual_sem_internet"].mean()
)

mediana_renda = (
    df_uf["renda_mediana_per_capita"].median()
)


maior_sem_internet = df_uf.loc[
    df_uf["percentual_sem_internet"].idxmax()
]


menor_sem_internet = df_uf.loc[
    df_uf["percentual_sem_internet"].idxmin()
]


maior_renda = df_uf.loc[
    df_uf["renda_mediana_per_capita"].idxmax()
]


menor_renda = df_uf.loc[
    df_uf["renda_mediana_per_capita"].idxmin()
]


# Contexto calculado que será enviado ao LLM
contexto_dados = f"""
UF analisada: {uf_selecionada}

Quantidade de municípios na base:
{len(df_uf)}

Média de domicílios sem internet na UF:
{media_sem_internet:.2f}%

Mediana da renda per capita na UF:
R$ {mediana_renda:.2f}

Município com maior percentual de domicílios sem internet:
{maior_sem_internet["municipio_nome"]}
Percentual: {maior_sem_internet["percentual_sem_internet"]:.2f}%
Renda mediana per capita:
R$ {maior_sem_internet["renda_mediana_per_capita"]:.2f}

Município com menor percentual de domicílios sem internet:
{menor_sem_internet["municipio_nome"]}
Percentual: {menor_sem_internet["percentual_sem_internet"]:.2f}%
Renda mediana per capita:
R$ {menor_sem_internet["renda_mediana_per_capita"]:.2f}

Município com maior renda mediana per capita:
{maior_renda["municipio_nome"]}
Renda: R$ {maior_renda["renda_mediana_per_capita"]:.2f}
Percentual sem internet:
{maior_renda["percentual_sem_internet"]:.2f}%

Município com menor renda mediana per capita:
{menor_renda["municipio_nome"]}
Renda: R$ {menor_renda["renda_mediana_per_capita"]:.2f}
Percentual sem internet:
{menor_renda["percentual_sem_internet"]:.2f}%
"""


# Exibe alguns indicadores calculados
col1, col2 = st.columns(2)

with col1:
    st.metric(
        f"Média sem internet em {uf_selecionada}",
        f"{media_sem_internet:.2f}%"
    )

with col2:
    st.metric(
        f"Mediana de renda em {uf_selecionada}",
        f"R$ {mediana_renda:.2f}"
    )


st.caption(
    "Os valores acima e os fatos utilizados pelo assistente "
    "são calculados diretamente pela aplicação."
)


st.markdown("---")


# Cria a memória da conversa
if "mensagens_esg" not in st.session_state:
    st.session_state["mensagens_esg"] = []


# Se a UF mudar, inicia um novo contexto
if "uf_chat_esg" not in st.session_state:
    st.session_state["uf_chat_esg"] = uf_selecionada


if st.session_state["uf_chat_esg"] != uf_selecionada:
    st.session_state["mensagens_esg"] = []
    st.session_state["uf_chat_esg"] = uf_selecionada


# Botão para apagar a memória
if st.button("Limpar conversa"):
    st.session_state["mensagens_esg"] = []
    st.rerun()


# Exibe o histórico
for mensagem in st.session_state["mensagens_esg"]:

    with st.chat_message(
        mensagem["role"]
    ):
        st.markdown(
            mensagem["content"]
        )


# Campo para nova pergunta
pergunta = st.chat_input(
    "Faça uma pergunta sobre os indicadores..."
)


if pergunta:

    # Guarda a pergunta na memória
    st.session_state["mensagens_esg"].append(
        {
            "role": "user",
            "content": pergunta
        }
    )


    with st.chat_message("user"):
        st.markdown(pergunta)


    prompt_sistema = f"""
Você é o Assistente ESG do projeto Rede de Acesso.

Responda em português utilizando exclusivamente os fatos
fornecidos pela aplicação e o histórico recente da conversa.

Os cálculos estatísticos já foram realizados em Python.
Não recalcule nem altere os valores apresentados.

Não invente municípios, indicadores ou valores.

Não atribua causas às diferenças observadas quando os dados
não permitirem essa conclusão.

Quando for pertinente, relacione os resultados aos Objetivos
de Desenvolvimento Sustentável, especialmente ao ODS 9
(Indústria, Inovação e Infraestrutura) e ao ODS 10
(Redução das Desigualdades).

Se a pergunta exigir uma informação que não esteja nos fatos
fornecidos, informe claramente que o painel não possui dados
suficientes para responder.

FATOS CALCULADOS PELA APLICAÇÃO:

{contexto_dados}
"""


    # Janela de memória:
    # últimas 4 interações = até 8 mensagens
    historico_recente = (
        st.session_state["mensagens_esg"][-8:]
    )


    mensagens_api = [
        {
            "role": "system",
            "content": prompt_sistema
        }
    ] + historico_recente


    try:

        resposta = requests.post(
            GROQ_URL,
            headers={
                "Authorization": (
                    f"Bearer {GROQ_API_KEY}"
                ),
                "Content-Type": "application/json"
            },
            json={
                "model": MODELO_GROQ,
                "messages": mensagens_api,
                "temperature": 0.2,
                "max_completion_tokens": 400
            },
            timeout=30
        )


        resposta.raise_for_status()


        dados_resposta = resposta.json()


        texto_resposta = (
            dados_resposta[
                "choices"
            ][0][
                "message"
            ][
                "content"
            ]
        )


    except requests.exceptions.RequestException as erro:

        texto_resposta = (
            "Não foi possível consultar o modelo de linguagem. "
            "Verifique a conexão e a configuração da API."
        )

        print(
            "ERRO GROQ:",
            erro
        )


    # Guarda a resposta na memória
    st.session_state["mensagens_esg"].append(
        {
            "role": "assistant",
            "content": texto_resposta
        }
    )


    with st.chat_message("assistant"):
        st.markdown(
            texto_resposta
        )