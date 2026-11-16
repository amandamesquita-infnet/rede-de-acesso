import requests

from config import API_URL

def consultar_municipio(codigo_ibge):
    resposta = requests.get(
        f"{API_URL}/municipios/{codigo_ibge}",
        timeout=10
    )

    resposta.raise_for_status()

    return resposta.json()