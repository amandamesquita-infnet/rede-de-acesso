import pandas as pd
import requests
import streamlit as st

from src.cliente_api import processar_texto


st.title("Análise Temática com Modelo Local")

st.write(
    """
    Esta página utiliza um modelo de linguagem executado
    localmente para classificar textos relacionados ao projeto
    Rede de Acesso.
    """
)


st.info(
    "A classificação é uma sugestão produzida pelo modelo. "
    "As pontuações não representam probabilidade de acerto."
)


texto = st.text_area(
    "Digite o texto para análise:",
    height=180,
    placeholder=(
        "Exemplo: O Ministério das Comunicações "
        "ampliou o acesso à internet..."
    )
)


if st.button(
    "Analisar texto",
    type="primary"
):

    try:

        resultado = processar_texto(
            texto
        )

    except ValueError as erro:

        st.warning(
            str(erro)
        )

        st.stop()

    except RuntimeError as erro:

        st.error(
            str(erro)
        )

        st.stop()

    except requests.exceptions.Timeout:

        st.error(
            "A análise demorou mais do que o esperado. "
            "Tente novamente."
        )

        st.stop()

    except requests.exceptions.RequestException:

        st.error(
            "Não foi possível conectar à API. "
            "Verifique se a FastAPI está em execução."
        )

        st.stop()


    nomes_categorias = {
        "RADIODIFUSAO":
            "Radiodifusão",

        "CONECTIVIDADE_INFRAESTRUTURA":
            "Conectividade e infraestrutura",

        "ENDERECAMENTO_CORREIOS":
            "Endereçamento e Correios",

        "INCLUSAO_CAPACITACAO_DIGITAL":
            "Inclusão e capacitação digital",

        "USO_E_SETOR_DE_TELECOMUNICACOES":
            "Uso e setor de telecomunicações",

        "GESTAO_POLITICAS_PUBLICAS":
            "Gestão e políticas públicas",
    }


    categoria = resultado[
        "categoria_sugerida"
    ]

    pontuacao = resultado[
        "confianca"
    ]


    st.markdown("---")

    st.subheader(
        "Resultado da análise"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Categoria sugerida",
            nomes_categorias.get(
                categoria,
                categoria
            )
        )


    with col2:

        st.metric(
            "Pontuação do modelo",
            f"{pontuacao:.2%}"
        )


    st.caption(
        "A pontuação indica o grau de preferência "
        "do modelo entre as categorias apresentadas. "
        "Ela não deve ser interpretada como "
        "probabilidade real de acerto."
    )


    st.markdown("---")

    st.subheader(
        "Pontuação por categoria"
    )


    dados_pontuacoes = []


    for codigo, valor in (
        resultado[
            "pontuacoes"
        ].items()
    ):

        dados_pontuacoes.append(
            {
                "Categoria":
                    nomes_categorias.get(
                        codigo,
                        codigo
                    ),

                "Pontuação":
                    valor,
            }
        )


    df_pontuacoes = pd.DataFrame(
        dados_pontuacoes
    )


    df_pontuacoes = (
        df_pontuacoes
        .sort_values(
            "Pontuação",
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )


    st.dataframe(
        df_pontuacoes,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Categoria":
                st.column_config.TextColumn(
                    "Categoria"
                ),

            "Pontuação":
                st.column_config.ProgressColumn(
                    "Pontuação",
                    min_value=0.0,
                    max_value=1.0,
                    format="%.2f"
                ),
        }
    )


    st.caption(
        "Modelo utilizado: "
        + resultado["motor"]
    )