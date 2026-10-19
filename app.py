import streamlit as st


st.set_page_config(
    page_title="Rede de Acesso",
    page_icon="🌐",
    layout="wide"
)


paginas = [
    st.Page(
        "pages/inicio.py",
        title="Início"
    ),
    st.Page(
        "pages/analise_municipal.py",
        title="Análise Municipal"
    ),
    st.Page(
        "pages/noticias.py",
        title="Notícias"
    ),
    st.Page(
        "pages/dados_complementares.py",
        title="Dados Complementares"
    ),
    st.Page(
        "pages/api.py",
        title="API"
    )
]


navegacao = st.navigation(paginas)

navegacao.run()