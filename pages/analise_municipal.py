import streamlit as st
import pandas as pd
from pathlib import Path


@st.cache_data
def carregar_dados(caminho):
    return pd.read_csv(
        caminho,
        dtype={"codigo_ibge": str}
    )


st.title("Análise Municipal")

st.write(
    """
    Explore os indicadores de acesso à internet e renda dos municípios
    brasileiros. Utilize os filtros para selecionar uma unidade da federação
    e um município.
    """
)


# Caminho da base integrada
arquivo_dados = (
    Path(__file__).parent.parent
    / "02_data_ingest_understanding"
    / "data"
    / "dados_integrados.csv"
)

df_acesso = carregar_dados(arquivo_dados)


# Separa UF e nome do município
df_acesso["uf"] = df_acesso["municipio"].str.extract(
    r" - ([A-Z]{2})$"
)

df_acesso["municipio_nome"] = df_acesso["municipio"].str.replace(
    r" - [A-Z]{2}$",
    "",
    regex=True
)


# Integra dados complementares caso tenham sido enviados
if "dados_upload" in st.session_state:

    df_acesso = df_acesso.merge(
        st.session_state["dados_upload"],
        on="codigo_ibge",
        how="left"
    )


# Filtros
st.sidebar.markdown("---")
st.sidebar.subheader("Filtros da Análise")

ufs = sorted(
    df_acesso["uf"]
    .dropna()
    .unique()
)


if (
    "uf_selecionada" not in st.session_state
    or st.session_state["uf_selecionada"] not in ufs
):
    st.session_state["uf_selecionada"] = ufs[0]


uf_selecionada = st.sidebar.selectbox(
    "Selecione uma UF",
    ufs,
    key="uf_selecionada"
)


df_uf = df_acesso[
    df_acesso["uf"] == uf_selecionada
].copy()


municipios = sorted(
    df_uf["municipio_nome"]
    .dropna()
    .unique()
)


if (
    "municipio_selecionado" not in st.session_state
    or st.session_state["municipio_selecionado"] not in municipios
):
    st.session_state["municipio_selecionado"] = municipios[0]


municipio_selecionado = st.sidebar.selectbox(
    "Selecione um município",
    municipios,
    key="municipio_selecionado"
)


# Município selecionado
dados_municipio = df_uf[
    df_uf["municipio_nome"] == municipio_selecionado
].iloc[0]


st.subheader(
    f"{municipio_selecionado} - {uf_selecionada}"
)


# Comparações com a UF
media_sem_internet_uf = (
    df_uf["percentual_sem_internet"].mean()
)

mediana_renda_uf = (
    df_uf["renda_mediana_per_capita"].median()
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Domicílios sem internet",
        f"{dados_municipio['percentual_sem_internet']:.2f}%"
    )

with col2:
    st.metric(
        f"Média em {uf_selecionada}",
        f"{media_sem_internet_uf:.2f}%"
    )

with col3:
    st.metric(
        "Renda mediana per capita",
        f"R$ {dados_municipio['renda_mediana_per_capita']:.2f}"
    )

with col4:
    st.metric(
        f"Mediana em {uf_selecionada}",
        f"R$ {mediana_renda_uf:.2f}"
    )


st.markdown("---")


# Municípios da UF
st.subheader(
    f"Municípios de {uf_selecionada}"
)

df_uf_exibicao = (
    df_uf[
        [
            "codigo_ibge",
            "municipio_nome",
            "percentual_sem_internet",
            "renda_mediana_per_capita"
        ]
    ]
    .sort_values(
        by="percentual_sem_internet",
        ascending=False
    )
    .rename(
        columns={
            "codigo_ibge": "Código IBGE",
            "municipio_nome": "Município",
            "percentual_sem_internet": "Domicílios sem internet (%)",
            "renda_mediana_per_capita": "Renda mediana per capita (R$)"
        }
    )
)

st.dataframe(
    df_uf_exibicao,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Código IBGE": st.column_config.TextColumn(
            "Código IBGE"
        ),
        "Município": st.column_config.TextColumn(
            "Município"
        ),
        "Domicílios sem internet (%)": st.column_config.NumberColumn(
            "Domicílios sem internet (%)",
            format="%.2f%%"
        ),
        "Renda mediana per capita (R$)": st.column_config.NumberColumn(
            "Renda mediana per capita (R$)",
            format="R$ %.2f"
        )
    }
)


st.markdown("---")


# Panorama nacional
st.subheader("Panorama Nacional")

st.write(
    """
    Municípios com os maiores percentuais de domicílios
    sem conexão domiciliar à internet.
    """
)

df_nacional = (
    df_acesso[
        [
            "codigo_ibge",
            "municipio",
            "percentual_sem_internet",
            "renda_mediana_per_capita"
        ]
    ]
    .sort_values(
        by="percentual_sem_internet",
        ascending=False
    )
    .head(10)
    .rename(
        columns={
            "codigo_ibge": "Código IBGE",
            "municipio": "Município",
            "percentual_sem_internet": "Domicílios sem internet (%)",
            "renda_mediana_per_capita": "Renda mediana per capita (R$)"
        }
    )
)

st.dataframe(
    df_nacional,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Domicílios sem internet (%)": st.column_config.NumberColumn(
            "Domicílios sem internet (%)",
            format="%.2f%%"
        ),
        "Renda mediana per capita (R$)": st.column_config.NumberColumn(
            "Renda mediana per capita (R$)",
            format="R$ %.2f"
        )
    }
)