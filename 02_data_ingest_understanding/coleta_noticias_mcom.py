import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import re


# Páginas mensais de notícias do Ministério das Comunicações
urls_meses = [
    "https://www.gov.br/mcom/pt-br/noticias/2026/novembro",
    "https://www.gov.br/mcom/pt-br/noticias/2026/outubro",
]


headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    )
}


noticias = []


def obter_data_publicacao(link):
    """
    Acessa a página individual da notícia e busca
    a data original de publicação.
    """

    try:
        resposta = requests.get(
            link,
            headers=headers,
            timeout=30
        )

        resposta.raise_for_status()

        soup = BeautifulSoup(
            resposta.text,
            "html.parser"
        )

        bloco_data = soup.find(
            "span",
            class_="documentPublished"
        )

        if bloco_data is None:
            return None

        valor_data = bloco_data.find(
            "span",
            class_="value"
        )

        if valor_data is None:
            return None

        texto_data = valor_data.get_text(
            " ",
            strip=True
        )

        resultado = re.search(
            r"\d{2}/\d{2}/\d{4}",
            texto_data
        )

        if resultado:
            return resultado.group()

        return None

    except requests.RequestException:
        return None


# Percorre cada mês selecionado
for url_base in urls_meses:

    print(
        f"\nColetando mês: {url_base}"
    )

    inicio = 0

    while True:

        # A primeira página não precisa do parâmetro de paginação
        if inicio == 0:
            url_pagina = url_base
        else:
            url_pagina = (
                f"{url_base}?b_start:int={inicio}"
            )

        resposta = requests.get(
            url_pagina,
            headers=headers,
            timeout=30
        )

        resposta.raise_for_status()

        soup = BeautifulSoup(
            resposta.text,
            "html.parser"
        )

        artigos = soup.find_all(
            "article",
            class_="entry"
        )

        # Quando não houver mais notícias, encerra o mês
        if len(artigos) == 0:
            break

        print(
            f"Página iniciada em {inicio}: "
            f"{len(artigos)} notícias"
        )

        for artigo in artigos:

            link_tag = artigo.select_one(
                "span.summary a[href]"
            )

            if link_tag is None:
                continue

            titulo = link_tag.get_text(
                " ",
                strip=True
            )

            link = urljoin(
                url_base,
                link_tag["href"]
            )

            resumo_tag = artigo.select_one(
                "p.description.discreet"
            )

            if resumo_tag is not None:
                resumo = resumo_tag.get_text(
                    " ",
                    strip=True
                )
            else:
                resumo = ""

            # A listagem mostra a última modificação.
            # Por isso, a data de publicação é buscada
            # na página individual da notícia.
            data = obter_data_publicacao(
                link
            )

            if data is None:
                print(
                    "Data de publicação não encontrada:",
                    titulo
                )
                continue

            noticias.append(
                {
                    "titulo": titulo,
                    "data": data,
                    "resumo": resumo,
                    "link": link
                }
            )

        # Cada página do portal possui até 20 notícias
        inicio += 20


# Cria o DataFrame
df_noticias = pd.DataFrame(
    noticias,
    columns=[
        "titulo",
        "data",
        "resumo",
        "link"
    ]
)


if df_noticias.empty:
    raise RuntimeError(
        "Nenhuma notícia foi encontrada. "
        "A estrutura das páginas pode ter sido alterada."
    )


# Evita registros duplicados
df_noticias = df_noticias.drop_duplicates(
    subset=["link"]
)


# Converte a coluna de data
df_noticias["data"] = pd.to_datetime(
    df_noticias["data"],
    format="%d/%m/%Y",
    errors="coerce"
)


df_noticias = df_noticias.dropna(
    subset=["data"]
)


# Ordena da notícia mais recente para a mais antiga
df_noticias = df_noticias.sort_values(
    by="data",
    ascending=False
)


# Retorna a data para o formato usado no projeto
df_noticias["data"] = (
    df_noticias["data"]
    .dt.strftime("%d/%m/%Y")
)


print(
    "\n=== AMOSTRA DAS NOTÍCIAS ==="
)


print(
    df_noticias.head(10).to_string(
        index=False
    )
)


print(
    "\nQuantidade total de notícias coletadas:",
    len(df_noticias)
)


# Define o local de saída
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


# Salva a base atualizada
df_noticias.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"\nArquivo salvo em: {arquivo_saida}"
)