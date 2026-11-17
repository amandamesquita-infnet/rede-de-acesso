from pathlib import Path

import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
)


PASTA_MODELO = (
    Path(__file__).parent.parent
    / "modelos"
    / "minilm_multilingual"
)


CATEGORIAS = [
    "radiodifusão",
    "conectividade e infraestrutura",
    "endereçamento e Correios",
    "inclusão e capacitação digital",
    "uso e setor de telecomunicações",
    "gestão e políticas públicas",
]


MAPA_CATEGORIAS = {
    "radiodifusão":
        "RADIODIFUSAO",

    "conectividade e infraestrutura":
        "CONECTIVIDADE_INFRAESTRUTURA",

    "endereçamento e Correios":
        "ENDERECAMENTO_CORREIOS",

    "inclusão e capacitação digital":
        "INCLUSAO_CAPACITACAO_DIGITAL",

    "uso e setor de telecomunicações":
        "USO_E_SETOR_DE_TELECOMUNICACOES",

    "gestão e políticas públicas":
        "GESTAO_POLITICAS_PUBLICAS",
}


def carregar_analisador():
    if not PASTA_MODELO.exists():
        raise FileNotFoundError(
            "Modelo local não encontrado."
        )


    tokenizer = AutoTokenizer.from_pretrained(
        PASTA_MODELO,
        local_files_only=True,
    )


    modelo = (
        AutoModelForSequenceClassification
        .from_pretrained(
            PASTA_MODELO,
            local_files_only=True,
        )
    )


    dispositivo = (
        0
        if torch.cuda.is_available()
        else -1
    )


    analisador = pipeline(
        "zero-shot-classification",
        model=modelo,
        tokenizer=tokenizer,
        device=dispositivo,
    )


    return analisador


def analisar_texto(
    analisador,
    texto,
):
    resultado = analisador(
        texto,
        CATEGORIAS,
        hypothesis_template=(
            "Este texto é sobre {}."
        ),
    )


    categoria_principal = (
        resultado["labels"][0]
    )


    categoria_codigo = (
        MAPA_CATEGORIAS[
            categoria_principal
        ]
    )


    confianca = float(
        resultado["scores"][0]
    )


    pontuacoes = {}


    for categoria, pontuacao in zip(
        resultado["labels"],
        resultado["scores"],
    ):
        codigo = MAPA_CATEGORIAS[
            categoria
        ]

        pontuacoes[codigo] = float(
            pontuacao
        )


    return {
        "categoria_sugerida":
            categoria_codigo,

        "confianca":
            confianca,

        "pontuacoes":
            pontuacoes,
    }