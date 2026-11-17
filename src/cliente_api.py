import requests

from config import API_URL


def consultar_municipio(codigo_ibge):
    resposta = requests.get(
        f"{API_URL}/municipios/{codigo_ibge}",
        timeout=10
    )

    resposta.raise_for_status()

    return resposta.json()


def comparar_municipios(codigos_ibge):
    resposta = requests.post(
        f"{API_URL}/comparacao",
        json={
            "codigos_ibge": codigos_ibge
        },
        timeout=10
    )

    resposta.raise_for_status()

    return resposta.json()


def verificar_status_api():
    resposta = requests.get(
        f"{API_URL}/",
        timeout=5
    )

    resposta.raise_for_status()

    return resposta.json()


def listar_municipios():
    resposta = requests.get(
        f"{API_URL}/municipios",
        timeout=10
    )

    resposta.raise_for_status()

    return resposta.json()


def listar_noticias():
    resposta = requests.get(
        f"{API_URL}/noticias",
        timeout=10
    )

    resposta.raise_for_status()

    return resposta.json()


def processar_texto(texto):
    resposta = requests.post(
        f"{API_URL}/processar_texto",
        json={
            "texto": texto
        },
        timeout=30
    )

    if resposta.status_code == 422:
        raise ValueError(
            "O texto enviado não atende "
            "aos critérios da análise."
        )

    if resposta.status_code == 503:
        detalhe = resposta.json().get(
            "detail",
            "O modelo está indisponível."
        )

        raise RuntimeError(
            detalhe
        )

    resposta.raise_for_status()

    return resposta.json()