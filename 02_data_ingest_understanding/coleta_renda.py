import requests
import pandas as pd
from pathlib import Path

url = (
    "https://apisidra.ibge.gov.br/values/"
    "t/10295/"
    "n6/all/"
    "v/13534/"
    "p/2022"
)

resposta = requests.get(url, timeout=30)
resposta.raise_for_status()

dados = resposta.json()

df = pd.DataFrame(dados[1:]).rename(columns=dados[0])

df_renda = df[
    [
        "Município (Código)",
        "Município",
        "Valor"
    ]
].copy()

df_renda = df_renda.rename(
    columns={
        "Município (Código)": "codigo_ibge",
        "Município": "municipio",
        "Valor": "renda_mediana_per_capita"
    }
)

df_renda["renda_mediana_per_capita"] = pd.to_numeric(
    df_renda["renda_mediana_per_capita"]
)

print(df_renda.head(10).to_string(index=False))
print("\nQuantidade de municípios:", len(df_renda))

pasta_dados = Path(__file__).parent / "data"
pasta_dados.mkdir(exist_ok=True)

arquivo_saida = pasta_dados / "renda_municipios.csv"

df_renda.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nArquivo salvo em: {arquivo_saida}")