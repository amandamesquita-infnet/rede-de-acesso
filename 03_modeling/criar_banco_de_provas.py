import pandas as pd
from pathlib import Path


# Base completa de notícias coletadas
caminho_noticias = (
    Path(__file__).parent.parent
    / "02_data_ingest_understanding"
    / "data"
    / "noticias_mcom.csv"
)


df_noticias = pd.read_csv(
    caminho_noticias
)


# Classificação manual utilizada como resposta esperada
# para o banco de provas do TP4.
rotulos = {
    # Radiodifusão
    47: "RADIODIFUSAO",
    74: "RADIODIFUSAO",
    59: "RADIODIFUSAO",
    73: "RADIODIFUSAO",
    56: "RADIODIFUSAO",

    # Conectividade e infraestrutura
    30: "CONECTIVIDADE_INFRAESTRUTURA",
    85: "CONECTIVIDADE_INFRAESTRUTURA",
    20: "CONECTIVIDADE_INFRAESTRUTURA",
    82: "CONECTIVIDADE_INFRAESTRUTURA",
    38: "CONECTIVIDADE_INFRAESTRUTURA",

    # Endereçamento e Correios
    41: "ENDERECAMENTO_CORREIOS",
    28: "ENDERECAMENTO_CORREIOS",
    21: "ENDERECAMENTO_CORREIOS",
    39: "ENDERECAMENTO_CORREIOS",
    29: "ENDERECAMENTO_CORREIOS",

    # Inclusão e capacitação digital
    34: "INCLUSAO_CAPACITACAO_DIGITAL",
    88: "INCLUSAO_CAPACITACAO_DIGITAL",
    16: "INCLUSAO_CAPACITACAO_DIGITAL",
    0: "INCLUSAO_CAPACITACAO_DIGITAL",
    45: "INCLUSAO_CAPACITACAO_DIGITAL",

    # Uso e setor de telecomunicações
    86: "USO_E_SETOR_DE_TELECOMUNICACOES",
    87: "USO_E_SETOR_DE_TELECOMUNICACOES",
    2: "USO_E_SETOR_DE_TELECOMUNICACOES",
    77: "USO_E_SETOR_DE_TELECOMUNICACOES",
    79: "USO_E_SETOR_DE_TELECOMUNICACOES",

    # Gestão e políticas públicas
    50: "GESTAO_POLITICAS_PUBLICAS",
    9: "GESTAO_POLITICAS_PUBLICAS",
    52: "GESTAO_POLITICAS_PUBLICAS",
    40: "GESTAO_POLITICAS_PUBLICAS",
    43: "GESTAO_POLITICAS_PUBLICAS",
}


# 30 exemplos:
# 6 categorias com 5 exemplos em cada categoria.
indices_amostra = [
    47,
    74,
    59,
    73,
    56,

    30,
    85,
    20,
    82,
    38,

    41,
    28,
    21,
    39,
    29,

    34,
    88,
    16,
    0,
    45,

    86,
    87,
    2,
    77,
    79,

    50,
    9,
    52,
    40,
    43,
]


banco = df_noticias.loc[
    indices_amostra,
    [
        "titulo",
        "resumo",
    ]
].copy()


# Mantém o índice original da notícia para permitir
# a reprodução da amostra posteriormente.
banco.insert(
    0,
    "indice_original",
    indices_amostra
)


banco["categoria_esperada"] = [
    rotulos[indice]
    for indice in indices_amostra
]


# Texto que será enviado aos modelos durante o benchmark
banco["texto"] = (
    banco["titulo"].fillna("")
    + ". "
    + banco["resumo"].fillna("")
)


arquivo_saida = (
    Path(__file__).parent
    / "banco_de_provas.csv"
)


banco.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)


print(
    "Banco de provas criado com sucesso."
)


print(
    "Quantidade de exemplos:",
    len(banco)
)


print(
    "\nDistribuição das categorias:"
)


print(
    banco["categoria_esperada"].value_counts()
)