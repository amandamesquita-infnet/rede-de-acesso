import time
from pathlib import Path

import pandas as pd
import torch
from transformers import pipeline


MODELO = (
    "MoritzLaurer/"
    "mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
)


CATEGORIAS = {
    "RADIODIFUSAO": "radiodifusão",
    "CONECTIVIDADE_INFRAESTRUTURA": (
        "conectividade e infraestrutura"
    ),
    "ENDERECAMENTO_CORREIOS": (
        "endereçamento e Correios"
    ),
    "INCLUSAO_CAPACITACAO_DIGITAL": (
        "inclusão e capacitação digital"
    ),
    "USO_E_SETOR_DE_TELECOMUNICACOES": (
        "uso e setor de telecomunicações"
    ),
    "GESTAO_POLITICAS_PUBLICAS": (
        "gestão e políticas públicas"
    ),
}


# Caminho do banco de provas
arquivo_banco = (
    Path(__file__).parent
    / "banco_de_provas.csv"
)


banco = pd.read_csv(
    arquivo_banco
)


# GPU quando disponível
device = (
    0
    if torch.cuda.is_available()
    else -1
)


print(
    "Modelo:",
    MODELO
)


print(
    "Dispositivo:",
    torch.cuda.get_device_name(0)
    if torch.cuda.is_available()
    else "CPU"
)


# Mede o tempo de carregamento
inicio_carregamento = time.perf_counter()


classificador = pipeline(
    "zero-shot-classification",
    model=MODELO,
    device=device
)


tempo_carregamento = (
    time.perf_counter()
    - inicio_carregamento
)


print(
    f"\nTempo de carregamento: "
    f"{tempo_carregamento:.2f} segundos"
)


# Reinicia a medição de memória da GPU
if torch.cuda.is_available():
    torch.cuda.reset_peak_memory_stats()


resultados = []


inicio_inferencia = time.perf_counter()


for numero, (_, linha) in enumerate(
    banco.iterrows(),
    start=1
):

    resultado = classificador(
        linha["texto"],
        candidate_labels=list(
            CATEGORIAS.values()
        ),
        hypothesis_template=(
            "Este texto é sobre {}."
        )
    )


    categoria_modelo_texto = (
        resultado["labels"][0]
    )


    categoria_modelo = next(
        codigo
        for codigo, descricao
        in CATEGORIAS.items()
        if descricao == categoria_modelo_texto
    )


    pontuacao = (
        resultado["scores"][0]
    )


    acertou = (
        categoria_modelo
        == linha["categoria_esperada"]
    )


    resultados.append(
        {
            "indice_original": (
                linha["indice_original"]
            ),
            "categoria_esperada": (
                linha["categoria_esperada"]
            ),
            "categoria_modelo": (
                categoria_modelo
            ),
            "pontuacao": (
                round(
                    pontuacao,
                    4
                )
            ),
            "acertou": acertou,
        }
    )


    print(
        f"{numero:02d}/30 - "
        f"Esperado: "
        f"{linha['categoria_esperada']} | "
        f"Modelo: "
        f"{categoria_modelo} | "
        f"{'ACERTOU' if acertou else 'ERROU'}"
    )


tempo_inferencia = (
    time.perf_counter()
    - inicio_inferencia
)


df_resultados = pd.DataFrame(
    resultados
)


quantidade_acertos = (
    df_resultados["acertou"].sum()
)


acuracia = (
    quantidade_acertos
    / len(df_resultados)
)


tempo_medio = (
    tempo_inferencia
    / len(df_resultados)
)


print(
    "\n=== RESULTADO MODELO 1 ==="
)


print(
    "Acertos:",
    f"{quantidade_acertos}/"
    f"{len(df_resultados)}"
)


print(
    "Acurácia:",
    f"{acuracia:.2%}"
)


print(
    "Tempo total de inferência:",
    f"{tempo_inferencia:.2f} segundos"
)


print(
    "Tempo médio por notícia:",
    f"{tempo_medio:.2f} segundos"
)


if torch.cuda.is_available():

    memoria_pico_mb = (
        torch.cuda.max_memory_allocated()
        / 1024
        / 1024
    )

    print(
        "Pico de memória CUDA durante "
        "a inferência:",
        f"{memoria_pico_mb:.2f} MB"
    )


# Resultado por categoria
print(
    "\nAcurácia por categoria:"
)


for categoria in CATEGORIAS:

    subset = df_resultados[
        df_resultados[
            "categoria_esperada"
        ] == categoria
    ]

    acertos_categoria = (
        subset["acertou"].sum()
    )

    print(
        f"- {categoria}: "
        f"{acertos_categoria}/"
        f"{len(subset)}"
    )


# Salva os resultados
arquivo_saida = (
    Path(__file__).parent
    / "resultado_modelo_1.csv"
)


df_resultados.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"\nResultados salvos em: "
    f"{arquivo_saida}"
)