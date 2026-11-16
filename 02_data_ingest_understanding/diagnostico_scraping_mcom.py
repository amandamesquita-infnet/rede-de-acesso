import requests
from bs4 import BeautifulSoup


# Página de notícias do Ministério das Comunicações
url = "https://www.gov.br/mcom/pt-br/noticias/ultimas-noticias"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    )
}


# Faz a requisição
resposta = requests.get(
    url,
    headers=headers,
    timeout=30
)

resposta.raise_for_status()


# Analisa o HTML recebido
soup = BeautifulSoup(
    resposta.text,
    "html.parser"
)


# Procura títulos de notícias no próprio HTML
titulos = []

for titulo_tag in soup.find_all("h2"):

    link_tag = titulo_tag.find(
        "a",
        href=True
    )

    if link_tag is None:
        continue

    titulo = link_tag.get_text(
        " ",
        strip=True
    )

    if titulo:
        titulos.append(titulo)


# Evidências do diagnóstico
print("=== DIAGNÓSTICO DA PÁGINA DO MCOM ===")

print(
    "Status HTTP:",
    resposta.status_code
)

print(
    "Tamanho do HTML recebido:",
    len(resposta.text),
    "caracteres"
)

print(
    "Quantidade de títulos encontrados no HTML:",
    len(titulos)
)


if titulos:

    print(
        "\nExemplo de título encontrado diretamente no HTML:"
    )

    print(
        titulos[0]
    )

    print(
        "\nConclusão: o conteúdo necessário para a coleta "
        "já está presente no HTML retornado pelo servidor."
    )

    print(
        "Portanto, requests + BeautifulSoup são suficientes "
        "e não há necessidade de Selenium para esta fonte."
    )

else:

    print(
        "\nNenhum título foi encontrado diretamente no HTML."
    )

    print(
        "A página deve ser investigada para verificar "
        "se o conteúdo depende de JavaScript."
    )