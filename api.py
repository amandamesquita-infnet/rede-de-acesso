from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from pathlib import Path


app = FastAPI(
    title="Rede de Acesso API",
    description=(
        "API para consulta de indicadores de acesso à internet "
        "e renda dos municípios brasileiros."
    ),
    version="1.0.0"
)


# Caminho da base integrada
CAMINHO_DADOS = (
    Path(__file__).parent
    / "02_data_ingest_understanding"
    / "data"
    / "dados_integrados.csv"
)


def carregar_dados():
    return pd.read_csv(
        CAMINHO_DADOS,
        dtype={"codigo_ibge": str}
    )


class ConsultaComparacao(BaseModel):
    codigos_ibge: list[str]


@app.get("/")
def inicio():
    return {
        "projeto": "Rede de Acesso",
        "status": "API disponível",
        "documentacao": "/docs"
    }


@app.get("/municipios/{codigo_ibge}")
def consultar_municipio(codigo_ibge: str):

    df = carregar_dados()

    resultado = df[
        df["codigo_ibge"] == codigo_ibge
    ]

    if resultado.empty:
        raise HTTPException(
            status_code=404,
            detail="Município não encontrado."
        )

    municipio = resultado.iloc[0]

    return {
        "codigo_ibge": str(municipio["codigo_ibge"]),
        "municipio": municipio["municipio"],
        "percentual_sem_internet": float(
            municipio["percentual_sem_internet"]
        ),
        "renda_mediana_per_capita": float(
            municipio["renda_mediana_per_capita"]
        )
    }


@app.post("/comparacao")
def comparar_municipios(consulta: ConsultaComparacao):

    df = carregar_dados()

    resultado = df[
        df["codigo_ibge"].isin(
            consulta.codigos_ibge
        )
    ]

    municipios = []

    for _, linha in resultado.iterrows():

        municipios.append(
            {
                "codigo_ibge": str(linha["codigo_ibge"]),
                "municipio": linha["municipio"],
                "percentual_sem_internet": float(
                    linha["percentual_sem_internet"]
                ),
                "renda_mediana_per_capita": float(
                    linha["renda_mediana_per_capita"]
                )
            }
        )

    return {
        "quantidade": len(municipios),
        "municipios": municipios
    }