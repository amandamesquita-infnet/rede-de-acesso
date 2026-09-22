import pandas as pd
from pathlib import Path

pasta_dados = Path(__file__).parent / "data"

arquivo_acesso = pasta_dados / "acesso_internet_municipios.csv"
arquivo_renda = pasta_dados / "renda_municipios.csv"

df_acesso = pd.read_csv(
    arquivo_acesso,
    dtype={"codigo_ibge": str}
)

df_renda = pd.read_csv(
    arquivo_renda,
    dtype={"codigo_ibge": str}
)

df_integrado = pd.merge(
    df_acesso,
    df_renda[["codigo_ibge", "renda_mediana_per_capita"]],
    on="codigo_ibge",
    how="inner"
)

print(df_integrado.head(10).to_string(index=False))
print("\nQuantidade de municípios:", len(df_integrado))
print("\nValores ausentes:")
print(df_integrado.isna().sum())

arquivo_saida = pasta_dados / "dados_integrados.csv"

df_integrado.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nArquivo salvo em: {arquivo_saida}")