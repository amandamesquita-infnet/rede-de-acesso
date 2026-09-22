import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import re


# Página de notícias do Ministério das Comunicações
url = "https://www.gov.br/mcom/pt-br/assuntos/noticias"

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


# Interpreta o HTML
soup = BeautifulSoup(
    resposta.text,
    "html.parser"
)


noticias = []


# Procura os títulos das notícias
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

    link = urljoin(
        url,
        link_tag["href"]
    )

    if not titulo:
        continue


    # Procura a data e o resumo no bloco
    # que contém a notícia
    bloco = titulo_tag

    data = None
    resumo = None

    for _ in range(6):

        bloco = bloco.parent

        if bloco is None:
            break

        texto_bloco = bloco.get_text(
            " ",
            strip=True
        )

        resultado = re.search(
            r"(\d{2}/\d{2}/\d{4})\s*-\s*(.+)",
            texto_bloco
        )

        if resultado:

            data = resultado.group(1)

            resumo = resultado.group(2).strip()

            break


    if data is not None:

        noticias.append(
            {
                "titulo": titulo,
                "data": data,
                "resumo": resumo,
                "link": link
            }
        )


# Cria o DataFrame já definindo as colunas
df_noticias = pd.DataFrame(
    noticias,
    columns=[
        "titulo",
        "data",
        "resumo",
        "link"
    ]
)


# Interrompe com uma mensagem clara se nada for encontrado
if df_noticias.empty:

    raise RuntimeError(
        "Nenhuma notícia foi encontrada. "
        "A estrutura da página pode ter sido alterada."
    )


# Remove registros duplicados
df_noticias = df_noticias.drop_duplicates(
    subset=["link"]
)


# Converte a data
df_noticias["data"] = pd.to_datetime(
    df_noticias["data"],
    format="%d/%m/%Y",
    errors="coerce"
)


# Ordena das mais recentes para as mais antigas
df_noticias = df_noticias.sort_values(
    by="data",
    ascending=False
)


# Formata novamente para o CSV
df_noticias["data"] = (
    df_noticias["data"]
    .dt.strftime("%d/%m/%Y")
)


# Exibe uma amostra
print(
    df_noticias.head(10).to_string(
        index=False
    )
)

print(
    "\nQuantidade de notícias coletadas:",
    len(df_noticias)
)


# Pasta de saída
pasta_dados = (
    Path(__file__).parent
    / "data"
)

pasta_dados.mkdir(
    exist_ok=True
)


arquivo_saida = (
    pasta_dados
    / "noticias_mcom.csv"
)


# Salva o arquivo
df_noticias.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"\nArquivo salvo em: {arquivo_saida}"
)