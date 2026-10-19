import streamlit as st


st.title("🌐 Rede de Acesso")
st.caption(
    "Radar de Inclusão Digital e Conectividade nos Municípios Brasileiros"
)

st.markdown("---")


# Problema de negócio
st.header("Problema de Negócio")

with st.container(border=True):
    st.write(
        """
        O acesso à internet e aos recursos digitais ainda ocorre de forma
        desigual entre os municípios brasileiros. Enquanto algumas localidades
        apresentam maior acesso, outras possuem limitações que podem dificultar
        o uso de informações, serviços públicos, oportunidades educacionais e
        profissionais disponíveis em meios digitais.

        Além disso, fatores socioeconômicos, como a renda, podem estar
        relacionados a essas diferenças.
        """
    )

st.info(
    "Quais municípios brasileiros apresentam maiores limitações "
    "de acesso digital e como essa condição se relaciona com "
    "indicadores de renda?"
)

st.markdown("---")


# Objetivo
st.header("Objetivo")

with st.container(border=True):
    st.write(
        """
        Desenvolver uma aplicação interativa em Python com Streamlit que
        integre indicadores de acesso à internet e renda, permitindo explorar
        e comparar as condições de inclusão digital entre municípios
        brasileiros.

        A aplicação também utiliza informações coletadas por Web Scraping
        e permite a inclusão de dados complementares por meio de arquivos CSV.
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
            O projeto analisa diferenças no acesso à internet entre
            municípios brasileiros e sua relação com a conectividade digital.
            """
        )

with col2:
    with st.container(border=True):
        st.subheader("ODS 10")
        st.write("**Redução das Desigualdades**")
        st.write(
            """
            O projeto compara indicadores de acesso digital e renda,
            permitindo observar diferenças socioeconômicas entre municípios.
            """
        )

st.markdown("---")


# Fontes
st.header("Fontes de Dados")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Dados Estruturados")
        st.markdown(
            """
            - **IBGE - SIDRA**
            - Censo Demográfico 2022
            - Acesso domiciliar à internet
            - Rendimento domiciliar mediano per capita
            """
        )

with col2:
    with st.container(border=True):
        st.subheader("Dados Textuais")
        st.markdown(
            """
            - **Ministério das Comunicações**
            - Notícias coletadas por Web Scraping
            - Títulos, datas, resumos e links
            """
        )


st.markdown("---")

st.caption(
    "Rede de Acesso | Projeto de Bloco - Inteligência Artificial Aplicada"
)