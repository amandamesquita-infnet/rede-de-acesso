import streamlit as st
import pandas as pd
from pathlib import Path


st.set_page_config(
    page_title="Rede de Acesso",
    page_icon="🌐",
    layout="wide"
)


# Cabeçalho
st.title("🌐 Rede de Acesso")
st.caption("Radar de Inclusão Digital e Conectividade nos Municípios Brasileiros")

st.markdown("---")


# Problema de negócio
st.header("Problema de Negócio")

with st.container(border=True):
    st.write(
        """
        O acesso à internet e aos recursos digitais ainda ocorre de forma desigual
        entre os municípios brasileiros. Além da infraestrutura disponível, fatores
        socioeconômicos, como renda, podem estar relacionados a essas diferenças
        de acesso.

        O projeto **Rede de Acesso** busca integrar diferentes indicadores para permitir
        a comparação entre municípios e identificar localidades com maiores
        limitações de acesso digital.
        """
    )

st.info(
    "Quais municípios brasileiros apresentam maiores limitações "
    "de acesso digital e como essa condição se relaciona com "
    "indicadores de renda e infraestrutura de conectividade?"
)

st.markdown("---")


# Objetivo
st.header("Objetivo")

with st.container(border=True):
    st.write(
        """
        Desenvolver uma aplicação interativa em Python com Streamlit que integre
        indicadores de acesso à internet, renda e infraestrutura de conectividade,
        permitindo analisar e comparar a inclusão digital entre municípios brasileiros.
        """
    )

st.markdown("---")


# ODS
st.header("Objetivos de Desenvolvimento Sustentável")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("ODS 9")
        st.write("**Indústria, Inovação e Infraestrutura**")
        st.write(
            """
            Análise das diferenças de acesso à internet e das condições
            de infraestrutura de conectividade entre municípios brasileiros.
            """
        )

with col2:
    with st.container(border=True):
        st.subheader("ODS 10")
        st.write("**Redução das Desigualdades**")
        st.write(
            """
            Análise da relação entre limitações de acesso digital
            e diferenças socioeconômicas entre os municípios.
            """
        )

st.markdown("---")


# Fontes e iniciativas
st.header("Fontes e iniciativas relacionadas")

col_fontes, col_iniciativas = st.columns(2)

with col_fontes:
    with st.container(border=True):
        st.subheader("Fontes de dados")

        st.markdown(
            """
            - [IBGE - SIDRA](https://sidra.ibge.gov.br/)
            - [Anatel](https://www.gov.br/anatel/)
            """
        )

with col_iniciativas:
    with st.container(border=True):
        st.subheader("Iniciativas e referências")

        st.markdown(
            """
            - [Estratégia Brasileira para a Transformação Digital - E-Digital](https://www.gov.br/casacivil/pt-br/acoes-e-programas/e-digital)
            - [Programa Wi-Fi Brasil / GESAC](https://www.gov.br/pt-br/servicos/obter-conexao-de-internet-programa-wi-fi-brasil)
            - [Objetivos de Desenvolvimento Sustentável - ONU Brasil](https://brasil.un.org/pt-br/sdgs)
            """
        )

st.markdown("---")


# Amostra dos dados
st.header("Amostra dos Dados")

arquivo_dados = (
    Path(__file__).parent
    / "02_data_ingest_understanding"
    / "data"
    / "dados_integrados.csv"
)

df_acesso = pd.read_csv(
    arquivo_dados,
    dtype={"codigo_ibge": str}
)

st.write(
    """
    A tabela abaixo apresenta os **10 municípios com maior percentual de
    domicílios particulares permanentes ocupados sem conexão domiciliar
    à internet**, acompanhados pelo rendimento domiciliar mensal mediano
    per capita, com base nos dados do Censo Demográfico 2022.
    """
)

df_exibicao = df_acesso.rename(
    columns={
        "codigo_ibge": "Código IBGE",
        "municipio": "Município",
        "percentual_sem_internet": "Domicílios sem internet (%)",
        "renda_mediana_per_capita": "Renda mediana per capita (R$)"
    }
)

df_amostra = df_exibicao.sort_values(
    by="Domicílios sem internet (%)",
    ascending=False
).head(10)

st.dataframe(
    df_amostra,
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


# Rodapé
st.markdown("---")

st.caption(
    "Rede de Acesso | Projeto de Bloco - Inteligência Artificial Aplicada"
)