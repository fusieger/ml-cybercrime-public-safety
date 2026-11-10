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

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "modelagem" / "painel_municipal_mensal.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "random_forest.joblib"
FEATURES_PATH = PROJECT_ROOT / "models" / "features_modelo.json"


# ============================================================
# CONSTANTES DE INTERFACE
# ============================================================

NOMES_MESES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}


# ============================================================
# CARREGAMENTO DOS ARTEFATOS
# ============================================================

@st.cache_data
def carregar_dados():
    df = pd.read_csv(DATA_PATH)

    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    df["mes"] = pd.to_numeric(df["mes"], errors="coerce")

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
    with open(FEATURES_PATH, "r", encoding="utf-8") as arquivo:
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
    entrada = pd.DataFrame(
        0.0,
        index=[0],
        columns=features_modelo
    )

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

    coluna_municipio = f"municipio_{linha['municipio']}"

    if coluna_municipio in entrada.columns:
        entrada.loc[0, coluna_municipio] = 1.0

    return entrada


def prever_linha(linha):
    entrada = preparar_entrada_modelo(linha)
    previsao = modelo.predict(entrada)[0]
    return float(previsao)


def formatar_numero(valor, casas=2):
    return (
        f"{valor:,.{casas}f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def nome_mes(numero):
    return NOMES_MESES.get(int(numero), str(numero))


# ============================================================
# CABEÇALHO
# ============================================================

st.title("Predição Espaço-Temporal de Estelionatos e Fraudes")

st.caption(
    "Estudo de caso com dados dos municípios do Espírito Santo "
    "entre 2023 e 2025."
)

st.info(
    "A aplicação analisa registros públicos de estelionato e fraude "
    "e estima a taxa mensal de ocorrências por 100 mil habitantes. "
    "As previsões têm finalidade acadêmica e exploratória e não "
    "representam probabilidade individual de vitimização nem "
    "evidência de uma causa criminal específica."
)

with st.expander("Como interpretar os principais indicadores?"):
    st.markdown(
        """
        **Ocorrência:** corresponde a um registro presente na base pública
        de Estelionato e Fraude da SESP/ES utilizada neste projeto.

        **Taxa por 100 mil habitantes:** normaliza o número de ocorrências
        pela população do município, permitindo comparar municípios de
        tamanhos diferentes.

        **Ocorrências Web:** registros cuja classificação de local está
        associada ao ambiente Web na base analisada.

        **Taxa prevista:** valor estimado pelo modelo Random Forest a partir
        do histórico recente do município e das demais características usadas
        no treinamento.

        **Taxa observada:** valor efetivamente calculado a partir das
        ocorrências registradas no período.

        **Diferença absoluta:** distância entre a taxa prevista e a taxa
        observada, sem considerar se o modelo estimou acima ou abaixo do valor
        real.

        **Média móvel de 3 meses:** média das taxas dos três meses anteriores.
        Ela ajuda a visualizar a tendência da série, suavizando oscilações
        mensais, mas não substitui os valores observados.
        """
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

    st.subheader("Indicadores gerais")

    st.caption(
        "Os indicadores abaixo resumem o conjunto completo analisado "
        "entre 2023 e 2025."
    )

    total_ocorrencias = int(df["total_ocorrencias"].sum())
    total_municipios = int(df["municipio"].nunique())
    taxa_media = float(df["taxa_100k_total"].mean())

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

    st.caption(
        "A taxa média permite comparar a intensidade relativa dos registros, "
        "enquanto 'Ocorrências Web' indica a proporção de registros classificados "
        "como associados ao ambiente Web."
    )

    st.subheader("Evolução mensal das ocorrências")

    evolucao = (
        df.groupby("data", as_index=False)
        .agg(total_ocorrencias=("total_ocorrencias", "sum"))
        .sort_values("data")
    )

    evolucao["media_movel_3m"] = (
        evolucao["total_ocorrencias"]
        .rolling(window=3, min_periods=3)
        .mean()
    )

    grafico_evolucao = (
        evolucao[
            [
                "data",
                "total_ocorrencias",
                "media_movel_3m"
            ]
        ]
        .set_index("data")
        .rename(
            columns={
                "total_ocorrencias": "Ocorrências mensais",
                "media_movel_3m": "Média móvel de 3 meses"
            }
        )
    )

    st.line_chart(
        grafico_evolucao,
        x_label="Mês",
        y_label="Ocorrências"
    )

    st.caption(
        "A média móvel de 3 meses suaviza oscilações pontuais e facilita "
        "a identificação da tendência geral da série."
    )

    st.subheader("Taxa média por município")

    ranking_historico = (
        df.groupby("municipio", as_index=False)
        .agg(taxa_media=("taxa_100k_total", "mean"))
        .sort_values("taxa_media", ascending=False)
        .head(10)
    )

    st.bar_chart(
        ranking_historico.set_index("municipio")["taxa_media"],
        x_label="Município",
        y_label="Taxa média / 100 mil"
    )

    st.caption(
        "O ranking utiliza taxas normalizadas por população. "
        "Taxas elevadas não significam, isoladamente, maior risco individual."
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
        df[df["municipio"] == municipio_selecionado]
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
        formatar_numero(df_municipio["taxa_100k_total"].mean())
    )

    col3.metric(
        "Taxa máxima / 100 mil",
        formatar_numero(df_municipio["taxa_100k_total"].max())
    )

    st.caption(
        "A taxa por 100 mil habitantes relaciona o número de ocorrências "
        "à população do município, permitindo comparação entre localidades."
    )

    st.subheader("Evolução da taxa por 100 mil habitantes")

    df_municipio["media_movel_visual_3m"] = (
        df_municipio["taxa_100k_total"]
        .rolling(window=3, min_periods=3)
        .mean()
    )

    grafico_taxas = (
        df_municipio[
            [
                "data",
                "taxa_100k_total",
                "taxa_100k_web",
                "media_movel_visual_3m"
            ]
        ]
        .set_index("data")
        .rename(
            columns={
                "taxa_100k_total": "Taxa total",
                "taxa_100k_web": "Taxa Web",
                "media_movel_visual_3m": "Média móvel 3 meses"
            }
        )
    )

    st.line_chart(
        grafico_taxas,
        x_label="Mês",
        y_label="Taxa / 100 mil"
    )

    st.caption(
        "A linha de média móvel de 3 meses ajuda a visualizar a tendência "
        "sem ocultar os valores mensais observados."
    )

    st.subheader("Histórico mensal")

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

    tabela_municipio["mes"] = tabela_municipio["mes"].map(NOMES_MESES)

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
        "O modelo Random Forest é aplicado aos registros de 2025 utilizando "
        "as mesmas características temporais empregadas durante o treinamento."
    )

    st.info(
        "A taxa prevista é uma estimativa do modelo. A taxa observada é o "
        "valor calculado a partir dos registros efetivamente presentes na base "
        "para aquele município e mês. A diferença entre elas representa o erro "
        "da estimativa naquele período."
    )

    df_2025 = (
        df[df["ano"] == 2025]
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
            df_2025["municipio"] == municipio_predicao
        ]["mes"]
        .unique()
        .tolist()
    )

    mes_predicao = col_filtro2.selectbox(
        "Mês de 2025",
        meses_disponiveis,
        format_func=nome_mes,
        key="mes_predicao"
    )

    linha = (
        df_2025[
            (df_2025["municipio"] == municipio_predicao)
            & (df_2025["mes"] == mes_predicao)
        ]
        .iloc[0]
    )

    taxa_prevista = prever_linha(linha)
    taxa_observada = float(linha["taxa_100k_total"])

    diferenca = taxa_observada - taxa_prevista
    diferenca_absoluta = abs(diferenca)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Taxa prevista / 100 mil",
        formatar_numero(taxa_prevista)
    )

    col2.metric(
        "Taxa observada / 100 mil",
        formatar_numero(taxa_observada)
    )

    col3.metric(
        "Diferença absoluta",
        formatar_numero(diferenca_absoluta)
    )

    if diferenca > 0:
        st.warning(
            "Neste período, a taxa observada ficou "
            f"{formatar_numero(diferenca)} pontos por 100 mil habitantes "
            "acima da estimativa do modelo. Isso indica um desvio entre "
            "o comportamento observado e o padrão histórico aprendido, "
            "sem estabelecer sua causa."
        )
    elif diferenca < 0:
        st.success(
            "Neste período, a taxa observada ficou "
            f"{formatar_numero(abs(diferenca))} pontos por 100 mil habitantes "
            "abaixo da estimativa do modelo."
        )
    else:
        st.success(
            "Neste período, a taxa observada coincidiu com a previsão do modelo."
        )

    st.subheader("Histórico utilizado na previsão")

    st.caption(
        "Estas características representam o comportamento recente do município "
        "antes do mês analisado. O valor do próprio mês não é utilizado para "
        "construir os lags ou as médias móveis."
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

    historico["Valor"] = historico["Valor"].round(2)

    st.dataframe(
        historico,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Ranking de taxa prevista em 2025")

    @st.cache_data
    def gerar_previsoes_2025(dados_2025):
        previsoes = []

        for _, registro in dados_2025.iterrows():
            previsoes.append(prever_linha(registro))

        resultado = dados_2025[
            [
                "municipio",
                "mes",
                "taxa_100k_total"
            ]
        ].copy()

        resultado["taxa_prevista"] = previsoes

        return resultado

    resultados_2025 = gerar_previsoes_2025(df_2025)

    ranking_previsto = (
        resultados_2025
        .groupby("municipio", as_index=False)
        .agg(taxa_prevista=("taxa_prevista", "mean"))
        .sort_values("taxa_prevista", ascending=False)
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
        ranking_previsto.set_index("municipio")["taxa_prevista"],
        x_label="Município",
        y_label="Taxa prevista / 100 mil"
    )

    st.caption(
        "O ranking compara taxas previstas normalizadas por população. "
        "Ele não representa probabilidade individual de sofrer fraude."
    )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "Projeto acadêmico desenvolvido na Universidade Federal da "
    "Fronteira Sul (UFFS). Dados públicos da SESP/ES e do IBGE. "
    "Os resultados possuem finalidade exploratória e acadêmica."
)
