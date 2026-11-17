from contextlib import asynccontextmanager
import logging
from pathlib import Path
from typing import Literal

import pandas as pd

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)
from fastapi.responses import JSONResponse

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from src.analisador_llm import (
    analisar_texto,
    carregar_analisador,
)


# Configuração do log
logging.basicConfig(
    level=logging.INFO
)

log = logging.getLogger(
    "rede_de_acesso"
)


# Categorias permitidas na análise
Categoria = Literal[
    "RADIODIFUSAO",
    "CONECTIVIDADE_INFRAESTRUTURA",
    "ENDERECAMENTO_CORREIOS",
    "INCLUSAO_CAPACITACAO_DIGITAL",
    "USO_E_SETOR_DE_TELECOMUNICACOES",
    "GESTAO_POLITICAS_PUBLICAS",
]


# Caminho da base integrada
CAMINHO_DADOS = (
    Path(__file__).parent
    / "02_data_ingest_understanding"
    / "data"
    / "dados_integrados.csv"
)


# Caminho da base de notícias
CAMINHO_NOTICIAS = (
    Path(__file__).parent
    / "02_data_ingest_understanding"
    / "data"
    / "noticias_mcom.csv"
)


# Dicionário que guarda o modelo carregado
MOTORES = {}


def carregar_dados():
    return pd.read_csv(
        CAMINHO_DADOS,
        dtype={
            "codigo_ibge": str
        }
    )


@asynccontextmanager
async def lifespan(
    _: FastAPI
):
    try:
        log.info(
            "Carregando modelo local..."
        )

        MOTORES["analise"] = (
            carregar_analisador()
        )

        log.info(
            "Modelo local carregado."
        )

    except (
        OSError,
        ValueError,
        RuntimeError,
    ) as falha:

        MOTORES["analise"] = None

        log.error(
            "Modelo não carregado: %s",
            falha,
        )

    yield

    MOTORES.clear()


app = FastAPI(
    title="Rede de Acesso API",
    description=(
        "API para consulta de indicadores "
        "de acesso à internet, renda, "
        "notícias e análise temática "
        "de textos."
    ),
    version="1.1.0",
    lifespan=lifespan,
)


# -----------------------------
# Modelos de resposta
# -----------------------------

class StatusAPI(BaseModel):
    projeto: str
    status: str
    documentacao: str
    modelo_carregado: bool


class Noticia(BaseModel):
    titulo: str
    data: str
    resumo: str
    link: str


class ListaNoticias(BaseModel):
    quantidade: int
    noticias: list[Noticia]


class Municipio(BaseModel):
    codigo_ibge: str
    municipio: str
    percentual_sem_internet: float
    renda_mediana_per_capita: float


class ListaMunicipios(BaseModel):
    quantidade: int
    municipios: list[Municipio]


class ConsultaComparacao(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    codigos_ibge: list[str] = Field(
        min_length=1
    )


class PedidoAnalise(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    texto: str = Field(
        min_length=10,
        max_length=5000,
    )


class ResultadoAnalise(BaseModel):
    tipo_analise: Literal[
        "classificacao"
    ]

    texto: str

    categoria_sugerida: Categoria

    confianca: float = Field(
        ge=0,
        le=1,
    )

    pontuacoes: dict[
        str,
        float
    ]

    motor: str


# -----------------------------
# Tratamento de erro inesperado
# -----------------------------

@app.exception_handler(Exception)
async def erro_interno(
    _: Request,
    erro: Exception,
):
    log.exception(
        "Erro interno não tratado: %s",
        erro,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": (
                "Ocorreu um erro interno "
                "inesperado."
            ),
            "codigo": "ERRO_INTERNO",
        },
    )


# -----------------------------
# Rotas
# -----------------------------

@app.get(
    "/",
    response_model=StatusAPI,
)
def inicio():
    return {
        "projeto": "Rede de Acesso",
        "status": "API disponível",
        "documentacao": "/docs",
        "modelo_carregado": (
            MOTORES.get(
                "analise"
            )
            is not None
        ),
    }


@app.get(
    "/noticias",
    response_model=ListaNoticias,
)
def listar_noticias():

    df = pd.read_csv(
        CAMINHO_NOTICIAS
    )

    df = df.fillna("")

    noticias = df.to_dict(
        orient="records"
    )

    return {
        "quantidade": len(
            noticias
        ),
        "noticias": noticias,
    }


@app.get(
    "/municipios",
    response_model=ListaMunicipios,
)
def listar_municipios():

    df = carregar_dados()

    municipios = []

    for _, linha in df.iterrows():

        municipios.append(
            {
                "codigo_ibge": str(
                    linha[
                        "codigo_ibge"
                    ]
                ),
                "municipio": (
                    linha[
                        "municipio"
                    ]
                ),
                "percentual_sem_internet":
                    float(
                        linha[
                            "percentual_sem_internet"
                        ]
                    ),
                "renda_mediana_per_capita":
                    float(
                        linha[
                            "renda_mediana_per_capita"
                        ]
                    ),
            }
        )

    return {
        "quantidade": len(
            municipios
        ),
        "municipios": municipios,
    }


@app.get(
    "/municipios/{codigo_ibge}",
    response_model=Municipio,
)
def consultar_municipio(
    codigo_ibge: str
):

    df = carregar_dados()

    resultado = df[
        df["codigo_ibge"]
        == codigo_ibge
    ]

    if resultado.empty:
        raise HTTPException(
            status_code=404,
            detail=(
                "Município não encontrado."
            ),
        )

    municipio = resultado.iloc[0]

    return {
        "codigo_ibge": str(
            municipio[
                "codigo_ibge"
            ]
        ),
        "municipio": (
            municipio[
                "municipio"
            ]
        ),
        "percentual_sem_internet":
            float(
                municipio[
                    "percentual_sem_internet"
                ]
            ),
        "renda_mediana_per_capita":
            float(
                municipio[
                    "renda_mediana_per_capita"
                ]
            ),
    }


@app.post(
    "/comparacao",
    response_model=ListaMunicipios,
)
def comparar_municipios(
    consulta: ConsultaComparacao
):

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
                "codigo_ibge": str(
                    linha[
                        "codigo_ibge"
                    ]
                ),
                "municipio": (
                    linha[
                        "municipio"
                    ]
                ),
                "percentual_sem_internet":
                    float(
                        linha[
                            "percentual_sem_internet"
                        ]
                    ),
                "renda_mediana_per_capita":
                    float(
                        linha[
                            "renda_mediana_per_capita"
                        ]
                    ),
            }
        )

    return {
        "quantidade": len(
            municipios
        ),
        "municipios": municipios,
    }


@app.post(
    "/processar_texto",
    response_model=ResultadoAnalise,
    responses={
        503: {
            "description": (
                "Modelo local indisponível."
            )
        }
    },
)
def processar_texto(
    pedido: PedidoAnalise
):

    analisador = MOTORES.get(
        "analise"
    )

    if analisador is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "O modelo de análise "
                "está indisponível. "
                "As demais rotas da API "
                "continuam funcionando."
            ),
        )

    resultado = analisar_texto(
        analisador,
        pedido.texto,
    )

    return {
        "tipo_analise":
            "classificacao",

        "texto":
            pedido.texto,

        "categoria_sugerida":
            resultado[
                "categoria_sugerida"
            ],

        "confianca":
            resultado[
                "confianca"
            ],

        "pontuacoes":
            resultado[
                "pontuacoes"
            ],

        "motor":
            (
                "multilingual-"
                "MiniLMv2-L6-"
                "mnli-xnli"
            ),
    }