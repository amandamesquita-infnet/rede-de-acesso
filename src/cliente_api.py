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