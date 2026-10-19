import streamlit as st
import pandas as pd
from pathlib import Path


@st.cache_data
def carregar_dados(caminho):
    return pd.read_csv(
        caminho,
        dtype={"codigo_ibge": str}
    )


st.title("Dados Complementares")

st.write(
    """
    Nesta página é possível enviar um arquivo CSV com informações
    adicionais sobre os municípios brasileiros.

    Para que os dados possam ser integrados à base principal,
    o arquivo deve conter obrigatoriamente a coluna `codigo_ibge`.
    """
)


# Base principal
arquivo_dados = (
    Path(__file__).parent.parent
    / "02_data_ingest_understanding"
    / "data"
    / "dados_integrados.csv"
)

df_acesso = carregar_dados(
    arquivo_dados
)


# Upload
st.subheader("Upload de arquivo CSV")

arquivo_upload = st.file_uploader(
    "Selecione um arquivo CSV",
    type=["csv"]
)


if arquivo_upload is not None:

    try:
        df_upload = pd.read_csv(
            arquivo_upload,
            dtype={"codigo_ibge": str}
        )

        if df_upload.empty:

            st.error(
                "O arquivo enviado está vazio."
            )

        elif "codigo_ibge" not in df_upload.columns:

            st.error(
                "O arquivo deve conter a coluna 'codigo_ibge'."
            )

        elif len(df_upload.columns) == 1:

            st.error(
                "O arquivo deve conter pelo menos uma coluna "
                "adicional além de 'codigo_ibge'."
            )

        else:

            st.session_state["dados_upload"] = df_upload

            st.success(
                f"Arquivo carregado com sucesso: "
                f"{len(df_upload)} registros."
            )

    except Exception as erro:

        st.error(
            f"Não foi possível ler o arquivo: {erro}"
        )


# Exibe dados carregados
if "dados_upload" in st.session_state:

    st.markdown("---")

    st.subheader("Dados enviados")

    st.dataframe(
        st.session_state["dados_upload"],
        use_container_width=True,
        hide_index=True
    )


    # Integra com a base principal
    df_integrado = df_acesso.merge(
        st.session_state["dados_upload"],
        on="codigo_ibge",
        how="left"
    )


    st.subheader("Dados integrados")

    st.write(
        """
        Os dados enviados foram associados à base principal
        utilizando o código IBGE do município.
        """
    )

    st.dataframe(
        df_integrado.head(20),
        use_container_width=True,
        hide_index=True
    )


    # Filtro para download
    df_integrado["uf"] = (
        df_integrado["municipio"]
        .str.extract(r" - ([A-Z]{2})$")
    )

    ufs = sorted(
        df_integrado["uf"]
        .dropna()
        .unique()
    )

    uf_download = st.selectbox(
        "Selecione uma UF para download",
        ufs
    )

    df_download = df_integrado[
        df_integrado["uf"] == uf_download
    ].copy()


    csv_download = df_download.to_csv(
        index=False
    ).encode("utf-8-sig")


    st.download_button(
        label="Baixar dados da UF selecionada",
        data=csv_download,
        file_name=f"dados_{uf_download}.csv",
        mime="text/csv"
    )