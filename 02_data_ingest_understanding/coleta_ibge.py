import requests
import pandas as pd
from pathlib import Path

url = (
    "https://apisidra.ibge.gov.br/values/"
    "t/9936/"
    "n6/all/"
    "v/1000381/"
    "p/2022/"
    "c2072/all"
)

resposta = requests.get(url, timeout=30)
resposta.raise_for_status()

dados = resposta.json()

df = pd.DataFrame(dados[1:]).rename(columns=dados[0])

df_sem_internet = df[
    df["Existência de conexão domiciliar à Internet"] == "Não"
].copy()

df_sem_internet = df_sem_internet[
    [
        "Município (Código)",
        "Município",
        "Valor"
    ]
]

df_sem_internet = df_sem_internet.rename(
    columns={
        "Município (Código)": "codigo_ibge",
        "Município": "municipio",
        "Valor": "percentual_sem_internet"
    }
)

df_sem_internet["percentual_sem_internet"] = pd.to_numeric(
    df_sem_internet["percentual_sem_internet"]
)

print(df_sem_internet.head(10).to_string(index=False))
print("\nQuantidade de municípios:", len(df_sem_internet))

pasta_dados = Path(__file__).parent / "data"
pasta_dados.mkdir(exist_ok=True)

arquivo_saida = pasta_dados / "acesso_internet_municipios.csv"

df_sem_internet.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nArquivo salvo em: {arquivo_saida}")
