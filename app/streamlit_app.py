from pathlib import Path
import json

import joblib
import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ============================================================

st.set_page_config(
    page_title="Predição de Estelionatos e Fraudes",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "modelagem"
    / "painel_municipal_mensal.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "random_forest.joblib"
)

FEATURES_PATH = (
    PROJECT_ROOT
    / "models"
    / "features_modelo.json"
)


# ============================================================
# CARREGAMENTO DOS ARTEFATOS
# ============================================================

@st.cache_data
def carregar_dados():
    df = pd.read_csv(DATA_PATH)

    df["ano"] = pd.to_numeric(
        df["ano"],
        errors="coerce"
    )

    df["mes"] = pd.to_numeric(
        df["mes"],
        errors="coerce"
    )

    df["data"] = pd.to_datetime(
        dict(
            year=df["ano"],
            month=df["mes"],
            day=1
        )
    )

    return df


@st.cache_resource
def carregar_modelo():
    return joblib.load(MODEL_PATH)


@st.cache_data
def carregar_features():
    with open(
        FEATURES_PATH,
        "r",
        encoding="utf-8"
    ) as arquivo:
        return json.load(arquivo)


def validar_artefatos():
    arquivos = {
        "Base processada": DATA_PATH,
        "Modelo Random Forest": MODEL_PATH,
        "Lista de features": FEATURES_PATH
    }

    ausentes = [
        nome
        for nome, caminho in arquivos.items()
        if not caminho.exists()
    ]

    if ausentes:
        st.error(
            "Não foi possível iniciar a aplicação. "
            "Os seguintes artefatos não foram encontrados: "
            + ", ".join(ausentes)
        )
        st.stop()


validar_artefatos()

df = carregar_dados()
modelo = carregar_modelo()
features_modelo = carregar_features()


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def preparar_entrada_modelo(linha):
    """
    Reconstrói uma única observação exatamente com as colunas
    utilizadas durante o treinamento do Random Forest.
    """

    entrada = pd.DataFrame(
        0.0,
        index=[0],
        columns=features_modelo
    )

    # Features numéricas utilizadas no notebook
    colunas_numericas = [
        "mes",
        "populacao",
        "taxa_lag_1",
        "taxa_lag_2",
        "taxa_lag_3",
        "media_movel_3m",
        "media_movel_6m"
    ]

    for coluna in colunas_numericas:
        if coluna in entrada.columns:
            entrada.loc[0, coluna] = linha[coluna]

    # O notebook usa pd.get_dummies(..., drop_first=True).
    # Para municípios diferentes da categoria removida, haverá
    # uma feature no formato municipio_NOME_DO_MUNICIPIO.
    coluna_municipio = f"municipio_{linha['municipio']}"

    if coluna_municipio in entrada.columns:
        entrada.loc[0, coluna_municipio] = 1.0

    return entrada


def prever_linha(linha):
    entrada = preparar_entrada_modelo(linha)
    previsao = modelo.predict(entrada)[0]
    return float(previsao)


def formatar_numero(valor, casas=2):
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ============================================================
# CABEÇALHO
# ============================================================

st.title(
    "Predição Espaço-Temporal de Estelionatos e Fraudes"
)

st.caption(
    "Estudo de caso com dados dos municípios do Espírito Santo "
    "entre 2023 e 2025."
)

st.info(
    "O modelo estima a taxa mensal de ocorrências por 100 mil "
    "habitantes. As previsões não devem ser interpretadas como "
    "evidência de uma causa criminal específica."
)


# ============================================================
# NAVEGAÇÃO
# ============================================================

aba_geral, aba_municipio, aba_predicoes = st.tabs(
    [
        "Visão Geral",
        "Análise por Município",
        "Predições"
    ]
)


# ============================================================
# ABA 1 - VISÃO GERAL
# ============================================================

with aba_geral:

    total_ocorrencias = int(
        df["total_ocorrencias"].sum()
    )

    total_municipios = int(
        df["municipio"].nunique()
    )

    taxa_media = float(
        df["taxa_100k_total"].mean()
    )

    proporcao_web = (
        df["ocorrencias_web"].sum()
        / df["total_ocorrencias"].sum()
        * 100
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Ocorrências",
        f"{total_ocorrencias:,}".replace(",", ".")
    )

    col2.metric(
        "Municípios",
        total_municipios
    )

    col3.metric(
        "Taxa média / 100 mil",
        formatar_numero(taxa_media)
    )

    col4.metric(
        "Ocorrências Web",
        f"{formatar_numero(proporcao_web)}%"
    )

    st.subheader(
        "Evolução mensal das ocorrências"
    )

    evolucao = (
        df.groupby("data", as_index=False)
        .agg(
            total_ocorrencias=(
                "total_ocorrencias",
                "sum"
            )
        )
        .set_index("data")
    )

    st.line_chart(
        evolucao["total_ocorrencias"],
        x_label="Mês",
        y_label="Ocorrências"
    )

    st.subheader(
        "Taxa média por município"
    )

    ranking_historico = (
        df.groupby(
            "municipio",
            as_index=False
        )
        .agg(
            taxa_media=(
                "taxa_100k_total",
                "mean"
            )
        )
        .sort_values(
            "taxa_media",
            ascending=False
        )
        .head(10)
    )

    st.bar_chart(
        ranking_historico.set_index(
            "municipio"
        )["taxa_media"],
        x_label="Município",
        y_label="Taxa média / 100 mil"
    )


# ============================================================
# ABA 2 - ANÁLISE POR MUNICÍPIO
# ============================================================

with aba_municipio:

    municipios = sorted(
        df["municipio"]
        .dropna()
        .unique()
        .tolist()
    )

    municipio_selecionado = st.selectbox(
        "Selecione o município",
        municipios,
        key="municipio_analise"
    )

    df_municipio = (
        df[
            df["municipio"]
            == municipio_selecionado
        ]
        .sort_values("data")
        .copy()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total de ocorrências",
        f"{int(df_municipio['total_ocorrencias'].sum()):,}".replace(",", ".")
    )

    col2.metric(
        "Taxa média / 100 mil",
        formatar_numero(
            df_municipio[
                "taxa_100k_total"
            ].mean()
        )
    )

    col3.metric(
        "Taxa máxima / 100 mil",
        formatar_numero(
            df_municipio[
                "taxa_100k_total"
            ].max()
        )
    )

    st.subheader(
        "Evolução da taxa por 100 mil habitantes"
    )

    grafico_taxas = (
        df_municipio[
            [
                "data",
                "taxa_100k_total",
                "taxa_100k_web"
            ]
        ]
        .set_index("data")
        .rename(
            columns={
                "taxa_100k_total": "Taxa total",
                "taxa_100k_web": "Taxa Web"
            }
        )
    )

    st.line_chart(
        grafico_taxas,
        x_label="Mês",
        y_label="Taxa / 100 mil"
    )

    st.subheader(
        "Histórico mensal"
    )

    tabela_municipio = df_municipio[
        [
            "ano",
            "mes",
            "total_ocorrencias",
            "ocorrencias_web",
            "populacao",
            "taxa_100k_total",
            "taxa_100k_web"
        ]
    ].copy()

    tabela_municipio = tabela_municipio.rename(
        columns={
            "ano": "Ano",
            "mes": "Mês",
            "total_ocorrencias": "Ocorrências",
            "ocorrencias_web": "Ocorrências Web",
            "populacao": "População",
            "taxa_100k_total": "Taxa / 100 mil",
            "taxa_100k_web": "Taxa Web / 100 mil"
        }
    )

    st.dataframe(
        tabela_municipio,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ABA 3 - PREDIÇÕES
# ============================================================

with aba_predicoes:

    st.write(
        "Nesta etapa, o modelo Random Forest é aplicado aos registros "
        "de 2025 utilizando exatamente as mesmas features temporais "
        "empregadas no treinamento."
    )

    df_2025 = (
        df[
            df["ano"] == 2025
        ]
        .dropna(
            subset=[
                "taxa_lag_3",
                "media_movel_6m"
            ]
        )
        .copy()
    )

    municipios_2025 = sorted(
        df_2025["municipio"]
        .unique()
        .tolist()
    )

    col_filtro1, col_filtro2 = st.columns(2)

    municipio_predicao = col_filtro1.selectbox(
        "Município",
        municipios_2025,
        key="municipio_predicao"
    )

    meses_disponiveis = sorted(
        df_2025[
            df_2025["municipio"]
            == municipio_predicao
        ]["mes"]
        .unique()
        .tolist()
    )

    mes_predicao = col_filtro2.selectbox(
        "Mês de 2025",
        meses_disponiveis,
        key="mes_predicao"
    )

    linha = (
        df_2025[
            (
                df_2025["municipio"]
                == municipio_predicao
            )
            & (
                df_2025["mes"]
                == mes_predicao
            )
        ]
        .iloc[0]
    )

    taxa_prevista = prever_linha(linha)
    taxa_observada = float(
        linha["taxa_100k_total"]
    )

    diferenca = (
        taxa_observada
        - taxa_prevista
    )

    diferenca_absoluta = abs(
        diferenca
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Taxa prevista / 100 mil",
        formatar_numero(
            taxa_prevista
        )
    )

    col2.metric(
        "Taxa observada / 100 mil",
        formatar_numero(
            taxa_observada
        )
    )

    col3.metric(
        "Diferença absoluta",
        formatar_numero(
            diferenca_absoluta
        )
    )

    if diferenca > 0:
        st.warning(
            "A taxa observada ficou acima da previsão do modelo "
            f"em {formatar_numero(diferenca)} pontos por 100 mil habitantes."
        )
    elif diferenca < 0:
        st.success(
            "A taxa observada ficou abaixo da previsão do modelo "
            f"em {formatar_numero(abs(diferenca))} pontos por 100 mil habitantes."
        )
    else:
        st.success(
            "A taxa observada coincidiu com a previsão do modelo."
        )

    st.subheader(
        "Histórico utilizado na previsão"
    )

    historico = pd.DataFrame(
        {
            "Característica": [
                "Taxa do mês anterior",
                "Taxa de 2 meses anteriores",
                "Taxa de 3 meses anteriores",
                "Média móvel de 3 meses",
                "Média móvel de 6 meses"
            ],
            "Valor": [
                linha["taxa_lag_1"],
                linha["taxa_lag_2"],
                linha["taxa_lag_3"],
                linha["media_movel_3m"],
                linha["media_movel_6m"]
            ]
        }
    )

    historico["Valor"] = (
        historico["Valor"]
        .round(2)
    )

    st.dataframe(
        historico,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "Ranking de taxa prevista em 2025"
    )

    @st.cache_data
    def gerar_previsoes_2025(
        dados_2025
    ):
        previsoes = []

        for _, registro in dados_2025.iterrows():
            previsoes.append(
                prever_linha(registro)
            )

        resultado = dados_2025[
            [
                "municipio",
                "mes",
                "taxa_100k_total"
            ]
        ].copy()

        resultado["taxa_prevista"] = previsoes

        return resultado


    resultados_2025 = gerar_previsoes_2025(
        df_2025
    )

    ranking_previsto = (
        resultados_2025
        .groupby(
            "municipio",
            as_index=False
        )
        .agg(
            taxa_prevista=(
                "taxa_prevista",
                "mean"
            )
        )
        .sort_values(
            "taxa_prevista",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        ranking_previsto.rename(
            columns={
                "municipio": "Município",
                "taxa_prevista": "Taxa média prevista / 100 mil"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        ranking_previsto.set_index(
            "municipio"
        )["taxa_prevista"],
        x_label="Município",
        y_label="Taxa prevista / 100 mil"
    )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "Projeto acadêmico desenvolvido na Universidade Federal da "
    "Fronteira Sul (UFFS). Os resultados possuem finalidade "
    "exploratória e acadêmica."
)
