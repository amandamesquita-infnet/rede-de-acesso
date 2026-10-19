import streamlit as st
import requests


st.title("Integração com a API")

st.write(
    """
    Esta página demonstra a integração da aplicação Streamlit
    com a API desenvolvida em FastAPI para o projeto Rede de Acesso.
    """
)

API_URL = "http://127.0.0.1:8000"


# Status da API
st.subheader("Status da API")

if st.button("Verificar conexão"):

    try:
        resposta = requests.get(
            f"{API_URL}/",
            timeout=5
        )

        if resposta.status_code == 200:
            st.success("API conectada com sucesso.")
            st.json(resposta.json())

        else:
            st.error(
                f"Erro na API: {resposta.status_code}"
            )

    except requests.exceptions.RequestException:
        st.error(
            "Não foi possível conectar à API. "
            "Verifique se o servidor FastAPI está em execução."
        )


st.markdown("---")


# GET
st.subheader("Consulta de Município")

st.write(
    """
    O endpoint GET permite consultar os indicadores de um
    município a partir de seu código IBGE.
    """
)

codigo_ibge = st.text_input(
    "Código IBGE",
    value="3304557"
)

if st.button("Consultar município"):

    try:
        resposta = requests.get(
            f"{API_URL}/municipios/{codigo_ibge}",
            timeout=5
        )

        if resposta.status_code == 200:

            dados = resposta.json()

            st.success(
                f"Município encontrado: {dados['municipio']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Domicílios sem internet",
                    f"{dados['percentual_sem_internet']:.2f}%"
                )

            with col2:
                st.metric(
                    "Renda mediana per capita",
                    f"R$ {dados['renda_mediana_per_capita']:.2f}"
                )

            st.json(dados)

        elif resposta.status_code == 404:
            st.warning("Município não encontrado.")

        else:
            st.error(
                f"Erro na consulta: {resposta.status_code}"
            )

    except requests.exceptions.RequestException:
        st.error(
            "Não foi possível conectar à API."
        )


st.markdown("---")


# POST
st.subheader("Comparação de Municípios")

st.write(
    """
    O endpoint POST recebe códigos IBGE e retorna os indicadores
    dos municípios solicitados para comparação.
    """
)

col1, col2 = st.columns(2)

with col1:
    codigo_1 = st.text_input(
        "Primeiro código IBGE",
        value="3304557"
    )

with col2:
    codigo_2 = st.text_input(
        "Segundo código IBGE",
        value="3550308"
    )


if st.button("Comparar municípios"):

    try:
        resposta = requests.post(
            f"{API_URL}/comparacao",
            json={
                "codigos_ibge": [
                    codigo_1,
                    codigo_2
                ]
            },
            timeout=5
        )

        if resposta.status_code == 200:

            dados = resposta.json()

            st.success(
                f"{dados['quantidade']} municípios retornados."
            )

            st.dataframe(
                dados["municipios"],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.error(
                f"Erro na consulta: {resposta.status_code}"
            )

    except requests.exceptions.RequestException:
        st.error(
            "Não foi possível conectar à API."
        )