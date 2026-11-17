from pathlib import Path

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)


MODELO_HUGGINGFACE = (
    "MoritzLaurer/"
    "multilingual-MiniLMv2-L6-mnli-xnli"
)


PASTA_MODELO = (
    Path(__file__).parent.parent
    / "modelos"
    / "minilm_multilingual"
)


def baixar_modelo():
    print(
        "Baixando tokenizer..."
    )

    tokenizer = AutoTokenizer.from_pretrained(
        MODELO_HUGGINGFACE
    )


    print(
        "Baixando modelo..."
    )

    modelo = (
        AutoModelForSequenceClassification
        .from_pretrained(
            MODELO_HUGGINGFACE
        )
    )


    PASTA_MODELO.mkdir(
        parents=True,
        exist_ok=True
    )


    tokenizer.save_pretrained(
        PASTA_MODELO
    )


    modelo.save_pretrained(
        PASTA_MODELO
    )


    print(
        "\nModelo salvo com sucesso em:"
    )

    print(
        PASTA_MODELO
    )


if __name__ == "__main__":
    baixar_modelo()