import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import re


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


    # O resumo aparece logo após o título
    resumo_tag = titulo_tag.find_next("p")

    if resumo_tag is not None:
        resumo = resumo_tag.get_text(
            " ",
            strip=True
        )
    else:
        resumo = ""


    # Procura a data depois do título
    data = None

    elemento = titulo_tag

    for _ in range(15):

        elemento = elemento.find_next()

        if elemento is None:
            break

        # Interrompe se chegar ao próximo título
        if elemento.name == "h2":
            break

        texto_elemento = elemento.get_text(
            " ",
            strip=True
        )

        resultado = re.search(
            r"publicado\s+(\d{2}/\d{2}/\d{4})",
            texto_elemento,
            flags=re.IGNORECASE
        )

        if resultado:

            data = resultado.group(1)

            break


    # Só adiciona a notícia quando encontra a data
    if data is not None:

        noticias.append(
            {
                "titulo": titulo,
                "data": data,
                "resumo": resumo,
                "link": link
            }
        )


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


# Remove registros sem data válida
df_noticias = df_noticias.dropna(
    subset=["data"]
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