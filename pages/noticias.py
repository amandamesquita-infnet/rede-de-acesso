import streamlit as st
import pandas as pd
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter


@st.cache_data
def carregar_noticias(caminho):
    return pd.read_csv(caminho)


st.title("Notícias e Conectividade")

st.write(
    """
    Esta página apresenta informações coletadas da página de notícias
    do Ministério das Comunicações por meio de Web Scraping com
    Beautiful Soup.
    """
)


# Caminho do arquivo gerado pelo scraping
arquivo_noticias = (
    Path(__file__).parent.parent
    / "02_data_ingest_understanding"
    / "data"
    / "noticias_mcom.csv"
)

df_noticias = carregar_noticias(
    arquivo_noticias
)


# Tratamento da data
df_noticias["data"] = pd.to_datetime(
    df_noticias["data"],
    format="%d/%m/%Y",
    errors="coerce"
)


# Indicadores
total_noticias = len(df_noticias)
data_mais_recente = df_noticias["data"].max()

if pd.notna(data_mais_recente):
    data_mais_recente_formatada = data_mais_recente.strftime(
        "%d/%m/%Y"
    )
else:
    data_mais_recente_formatada = "Não disponível"


col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Notícias coletadas",
        total_noticias
    )

with col2:
    st.metric(
        "Notícia mais recente",
        data_mais_recente_formatada
    )


st.markdown("---")


# Tabela de notícias
st.subheader("Notícias coletadas")

df_exibicao = df_noticias.copy()

df_exibicao["data"] = (
    df_exibicao["data"]
    .dt.strftime("%d/%m/%Y")
)

df_exibicao = df_exibicao.rename(
    columns={
        "titulo": "Título",
        "data": "Data",
        "resumo": "Resumo",
        "link": "Link"
    }
)

st.dataframe(
    df_exibicao,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Título": st.column_config.TextColumn(
            "Título"
        ),
        "Data": st.column_config.TextColumn(
            "Data"
        ),
        "Resumo": st.column_config.TextColumn(
            "Resumo"
        ),
        "Link": st.column_config.LinkColumn(
            "Acessar notícia",
            display_text="Abrir"
        )
    }
)


st.markdown("---")


# Texto para análise
texto_noticias = " ".join(
    (
        df_noticias["titulo"].fillna("")
        + " "
        + df_noticias["resumo"].fillna("")
    )
)


stopwords_pt = {
    "a", "ao", "aos", "as", "com", "como", "da", "das",
    "de", "do", "dos", "e", "em", "entre", "é", "mais",
    "na", "nas", "no", "nos", "o", "os", "ou", "para",
    "pela", "pelas", "pelo", "pelos", "por", "que",
    "se", "sem", "sobre", "um", "uma", "uns", "umas"
}


# Nuvem de palavras
st.subheader("Palavras em destaque")

nuvem = WordCloud(
    width=1200,
    height=500,
    background_color="white",
    stopwords=stopwords_pt,
    collocations=False
).generate(texto_noticias)


fig, ax = plt.subplots(
    figsize=(12, 5)
)

ax.imshow(
    nuvem,
    interpolation="bilinear"
)

ax.axis("off")

st.pyplot(fig)

plt.close(fig)


st.markdown("---")


# Frequência
st.subheader("Termos mais frequentes")

palavras = re.findall(
    r"\b[a-záàâãéêíóôõúç]+\b",
    texto_noticias.lower()
)

palavras_filtradas = [
    palavra
    for palavra in palavras
    if palavra not in stopwords_pt
    and len(palavra) > 2
]

frequencia = Counter(
    palavras_filtradas
)

df_frequencia = pd.DataFrame(
    frequencia.most_common(15),
    columns=[
        "Termo",
        "Frequência"
    ]
)

st.bar_chart(
    df_frequencia,
    x="Termo",
    y="Frequência"
)