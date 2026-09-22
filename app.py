import streamlit as st
import pandas as pd
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter

@st.cache_data
def carregar_dados(caminho):
    return pd.read_csv(
        caminho,
        dtype={"codigo_ibge": str}
    )

@st.cache_data
def carregar_noticias(caminho):
    return pd.read_csv(caminho)

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


# Dados municipais
arquivo_dados = (
    Path(__file__).parent
    / "02_data_ingest_understanding"
    / "data"
    / "dados_integrados.csv"
)

df_acesso = carregar_dados(arquivo_dados)


# Separa a UF do nome do município
df_acesso["uf"] = df_acesso["municipio"].str.extract(
    r" - ([A-Z]{2})$"
)

df_acesso["municipio_nome"] = df_acesso["municipio"].str.replace(
    r" - [A-Z]{2}$",
    "",
    regex=True
)


# Filtros
st.sidebar.header("Filtros")

ufs = sorted(
    df_acesso["uf"]
    .dropna()
    .unique()
)

# Guarda a UF selecionada durante a sessão
if "uf_selecionada" not in st.session_state:
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


# Mantém um município válido quando a UF é alterada
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

# Upload de dados complementares
st.sidebar.markdown("---")
st.sidebar.subheader("Dados complementares")

arquivo_upload = st.sidebar.file_uploader(
    "Adicionar arquivo CSV",
    type=["csv"]
)

if arquivo_upload is not None:

    try:
        df_upload = pd.read_csv(
            arquivo_upload,
            dtype={"codigo_ibge": str}
        )

        if df_upload.empty:
            st.sidebar.error(
                "O arquivo enviado está vazio."
            )

        elif "codigo_ibge" not in df_upload.columns:
            st.sidebar.error(
                "O arquivo deve conter a coluna 'codigo_ibge'."
            )

        elif len(df_upload.columns) == 1:
            st.sidebar.error(
                "O arquivo deve conter pelo menos uma coluna "
                "adicional além de 'codigo_ibge'."
            )

        else:
            st.session_state["dados_upload"] = df_upload

            st.sidebar.success(
                f"Arquivo carregado: {len(df_upload)} registros."
            )

    except Exception as erro:
        st.sidebar.error(
            f"Não foi possível ler o arquivo: {erro}"
        )

# Integra os dados enviados pelo usuário
if "dados_upload" in st.session_state:

    df_acesso = df_acesso.merge(
        st.session_state["dados_upload"],
        on="codigo_ibge",
        how="left"
    )

# Atualiza os dados da UF após a integração
df_uf = df_acesso[
    df_acesso["uf"] == uf_selecionada
].copy()


# Download dos dados filtrados e processados
csv_download = df_uf.to_csv(
    index=False
).encode("utf-8-sig")

st.sidebar.download_button(
    label="Baixar dados da UF selecionada",
    data=csv_download,
    file_name=f"dados_{uf_selecionada}.csv",
    mime="text/csv"
)

# Dados do município selecionado
dados_municipio = df_uf[
    df_uf["municipio_nome"] == municipio_selecionado
].iloc[0]


st.markdown("---")

st.header("Exploração Interativa")

st.write(
    """
    Utilize os filtros na barra lateral para selecionar uma unidade
    da federação e um município. Os indicadores abaixo permitem comparar
    a situação do município selecionado com os valores do seu estado.
    """
)


# Indicadores do município e da UF
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


# Tabela da UF selecionada
st.subheader(
    f"Municípios de {uf_selecionada}"
)

st.write(
    """
    A tabela apresenta os municípios da UF selecionada,
    ordenados pelo percentual de domicílios sem conexão
    domiciliar à internet.
    """
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
st.header("Panorama Nacional")

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
    df_amostra[
        [
            "Código IBGE",
            "Município",
            "Domicílios sem internet (%)",
            "Renda mediana per capita (R$)"
        ]
    ],
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

# Notícias coletadas por Web Scraping
st.markdown("---")

st.header("Conectividade em Destaque")

st.write(
    """
    Esta seção apresenta informações coletadas da página de notícias
    do Ministério das Comunicações por meio de Web Scraping com
    Beautiful Soup. A coleta é realizada separadamente da aplicação
    e armazenada em arquivo CSV.
    """
)


arquivo_noticias = (
    Path(__file__).parent
    / "02_data_ingest_understanding"
    / "data"
    / "noticias_mcom.csv"
)

df_noticias = carregar_noticias(
    arquivo_noticias
)


# Estatísticas básicas
total_noticias = len(df_noticias)

df_noticias["data"] = pd.to_datetime(
    df_noticias["data"],
    format="%d/%m/%Y",
    errors="coerce"
)

data_mais_recente = df_noticias["data"].max()

if pd.notna(data_mais_recente):
    data_mais_recente = data_mais_recente.strftime("%d/%m/%Y")
else:
    data_mais_recente = "Não disponível"


col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Notícias coletadas",
        total_noticias
    )

with col2:
    st.metric(
        "Notícia mais recente",
        data_mais_recente
    )


# Prepara tabela para exibição
df_noticias_exibicao = df_noticias.copy()

df_noticias_exibicao["data"] = (
    df_noticias_exibicao["data"]
    .dt.strftime("%d/%m/%Y")
)

df_noticias_exibicao = df_noticias_exibicao.rename(
    columns={
        "titulo": "Título",
        "data": "Data",
        "resumo": "Resumo",
        "link": "Link"
    }
)


st.subheader("Notícias coletadas")

st.dataframe(
    df_noticias_exibicao,
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

# Nuvem de palavras
st.subheader("Palavras em destaque")

st.write(
    """
    A nuvem abaixo representa os termos mais recorrentes nos títulos
    e resumos das notícias coletadas. Quanto maior a palavra,
    maior sua frequência no conjunto de textos.
    """
)


# Junta títulos e resumos em um único texto
texto_noticias = " ".join(
    (
        df_noticias["titulo"].fillna("")
        + " "
        + df_noticias["resumo"].fillna("")
    )
)


# Palavras comuns que não contribuem para a análise
stopwords_pt = {
    "a", "ao", "aos", "as", "com", "como", "da", "das",
    "de", "do", "dos", "e", "em", "entre", "é", "mais",
    "na", "nas", "no", "nos", "o", "os", "ou", "para",
    "pela", "pelas", "pelo", "pelos", "por", "que",
    "se", "sem", "sobre", "um", "uma", "uns", "umas"
}


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

# Frequência das palavras
st.subheader("Termos mais frequentes")

st.write(
    """
    O gráfico apresenta os termos que aparecem com maior frequência
    nos títulos e resumos das notícias coletadas, desconsiderando
    palavras comuns da língua portuguesa.
    """
)


# Separa as palavras do texto
palavras = re.findall(
    r"\b[a-záàâãéêíóôõúç]+\b",
    texto_noticias.lower()
)


# Remove palavras comuns e termos muito curtos
palavras_filtradas = [
    palavra
    for palavra in palavras
    if palavra not in stopwords_pt
    and len(palavra) > 2
]


# Conta a frequência
frequencia = Counter(
    palavras_filtradas
)


# Seleciona os 15 termos mais frequentes
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

# Rodapé
st.markdown("---")

st.caption(
    "Rede de Acesso | Projeto de Bloco - Inteligência Artificial Aplicada"
)