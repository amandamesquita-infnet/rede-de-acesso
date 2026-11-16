from transformers import pipeline
import torch


MODELO = (
    "MoritzLaurer/"
    "mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
)


CATEGORIAS = [
    "radiodifusão",
    "conectividade e infraestrutura",
    "endereçamento e Correios",
    "inclusão e capacitação digital",
    "uso e setor de telecomunicações",
    "gestão e políticas públicas",
]


# Usa a GPU NVIDIA quando disponível
device = 0 if torch.cuda.is_available() else -1


print(
    "Dispositivo:",
    torch.cuda.get_device_name(0)
    if torch.cuda.is_available()
    else "CPU"
)


print(
    "\nCarregando modelo..."
)


classificador = pipeline(
    "zero-shot-classification",
    model=MODELO,
    device=device
)


texto = (
    "Internet Brasil vence prêmio nacional por ampliar acesso "
    "à internet entre estudantes de baixa renda. "
    "Programa do Ministério das Comunicações foi reconhecido "
    "por iniciativa de combate à exclusão digital."
)


resultado = classificador(
    texto,
    candidate_labels=CATEGORIAS,
    hypothesis_template="Este texto é sobre {}."
)


print(
    "\nCategoria principal:",
    resultado["labels"][0]
)


print(
    "Pontuação:",
    round(
        resultado["scores"][0],
        4
    )
)


print(
    "\nTodas as categorias:"
)


for categoria, pontuacao in zip(
    resultado["labels"],
    resultado["scores"]
):

    print(
        f"- {categoria}: "
        f"{pontuacao:.4f}"
    )