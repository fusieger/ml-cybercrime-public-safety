# Predição Espaço-Temporal de Estelionatos e Fraudes

Projeto acadêmico desenvolvido na disciplina de Planejamento e Gestão de Projetos da Universidade Federal da Fronteira Sul (UFFS).

O projeto investiga a utilização de técnicas de Machine Learning para estimar mensalmente a taxa de ocorrências de estelionato e fraude por 100 mil habitantes nos municípios do Espírito Santo.

## Problema

O crescimento dos registros de estelionato e fraude, especialmente aqueles associados a meios digitais, cria novos desafios para análise e acompanhamento da segurança pública.

Além do número absoluto de ocorrências, é necessário considerar diferenças populacionais entre municípios e a evolução temporal dos registros.

O projeto busca responder à seguinte questão:

> Como técnicas de Machine Learning podem ser utilizadas para estimar mensalmente a taxa de ocorrências de estelionato e fraude nos municípios do Espírito Santo a partir do histórico das ocorrências e da população municipal?

## Objetivo

Desenvolver e avaliar uma abordagem baseada em Machine Learning capaz de identificar padrões espaço-temporais e estimar mensalmente a taxa de ocorrências de estelionato e fraude nos municípios do Espírito Santo, utilizando registros públicos de segurança e dados populacionais.

## Fontes de Dados

O projeto utiliza duas fontes públicas principais:

### SESP/ES

Secretaria de Estado da Segurança Pública e Defesa Social do Espírito Santo.

Base utilizada:

- Estelionato e Fraude;
- registros entre 2023 e 2025;
- granularidade municipal e temporal;
- identificação de ocorrências associadas ao ambiente Web.

### IBGE

Instituto Brasileiro de Geografia e Estatística.

Dados utilizados:

- estimativas anuais de população municipal;
- anos de 2023, 2024 e 2025.

Os dados populacionais são utilizados para calcular taxas mensais por 100 mil habitantes.

## Pipeline de Dados

O fluxo principal do projeto é:

```text
Dados SESP/ES + IBGE
        ↓
Preparação e padronização
        ↓
Grade espaço-temporal
        ↓
Integração populacional
        ↓
Engenharia de características
        ↓
Treinamento dos modelos
        ↓
Avaliação temporal
        ↓
Seleção do Random Forest
        ↓
Exportação dos artefatos
        ↓
Aplicação Streamlit
```

A base processada contém todas as combinações entre os 78 municípios do Espírito Santo e os 36 meses analisados entre 2023 e 2025, totalizando 2.808 observações município-mês.

## Engenharia de Características

Foram utilizadas características temporais construídas apenas com informações anteriores ao período analisado:

- mês do ano;
- população;
- taxa do mês anterior;
- taxa de dois meses anteriores;
- taxa de três meses anteriores;
- média móvel de três meses;
- média móvel de seis meses;
- município.

Essa estratégia evita vazamento de informações futuras durante o treinamento.

## Modelos Avaliados

Foram comparadas três abordagens:

- Baseline de persistência, utilizando a taxa do mês anterior;
- Random Forest Regressor;
- XGBoost Regressor.

Os anos de 2023 e 2024 foram utilizados para treinamento, enquanto 2025 foi reservado integralmente para teste temporal.

## Resultados

| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| Baseline | 23,28 | 32,21 | 0,2735 |
| Random Forest | **20,21** | **27,96** | **0,4527** |
| XGBoost | 21,54 | 29,45 | 0,3930 |

O Random Forest apresentou o melhor desempenho geral e foi selecionado para integração ao MVP.

Os valores previstos representam taxas mensais estimadas por 100 mil habitantes e não devem ser interpretados como probabilidade individual de vitimização.

## MVP

A aplicação interativa foi desenvolvida com Streamlit e publicada no Streamlit Community Cloud.

### Acessar o MVP

https://ml-cybercrime-public-safety-sf6t6tjf3moh4dn7xrn2f3.streamlit.app/

A aplicação possui três áreas principais:

### Visão Geral

Permite visualizar:

- número total de ocorrências;
- quantidade de municípios analisados;
- taxa média por 100 mil habitantes;
- proporção de ocorrências associadas ao ambiente Web;
- evolução mensal das ocorrências;
- média móvel de três meses;
- ranking de taxas médias por município.

### Análise por Município

Permite selecionar um município e consultar:

- total de ocorrências;
- taxa média;
- taxa máxima;
- evolução da taxa mensal;
- ocorrências associadas ao ambiente Web;
- média móvel de três meses;
- histórico mensal.

### Predições

Permite selecionar um município e um mês de 2025 e consultar:

- taxa prevista;
- taxa observada;
- diferença absoluta;
- características históricas utilizadas pelo modelo;
- ranking de taxa prevista entre os municípios.

## Sprint 4 — Evolução

Durante a Sprint 4, o MVP foi submetido a uma avaliação exploratória com cinco participantes.

Os participantes avaliaram a aplicação por meio de questões em escala de 1 a 5 e perguntas abertas.

Os principais resultados foram:

| Critério | Média |
|---|---:|
| Clareza da finalidade da aplicação | 4,4 |
| Facilidade para localizar análise por município | 4,8 |
| Clareza da taxa por 100 mil habitantes | 4,0 |
| Clareza entre taxa prevista e observada | 4,2 |
| Contribuição dos gráficos para compreensão | 5,0 |
| Navegação entre as seções | 5,0 |

A avaliação indicou que os principais pontos de melhoria estavam relacionados à explicabilidade dos indicadores e das previsões.

Com base no feedback recebido, foram implementadas as seguintes melhorias:

- inclusão de explicações adicionais para os principais indicadores;
- contextualização do conceito de ocorrência;
- explicação da taxa por 100 mil habitantes;
- explicação das ocorrências associadas ao ambiente Web;
- maior clareza na diferença entre taxa prevista e observada;
- explicação da diferença absoluta;
- inclusão de média móvel de três meses nas visualizações temporais;
- apresentação dos meses por nome na área de predições;
- revisão de textos da interface para reduzir interpretações equivocadas.

A avaliação possui caráter exploratório, pois foi realizada com uma amostra reduzida de cinco participantes selecionados por conveniência.

## Estrutura do Repositório

```text
ml-cybercrime-public-safety/
├── app/
│   └── streamlit_app.py
├── article/
├── data/
│   ├── raw/
│   └── processed/
│       └── modelagem/
│           └── painel_municipal_mensal.csv
├── docs/
├── models/
│   ├── random_forest.joblib
│   └── features_modelo.json
├── notebooks/
├── src/
├── tests/
├── README.md
└── requirements.txt
```

## Artefatos do Modelo

Os principais artefatos utilizados pelo MVP são:

```text
data/processed/modelagem/painel_municipal_mensal.csv
models/random_forest.joblib
models/features_modelo.json
```

O modelo é carregado diretamente pela aplicação Streamlit, evitando a necessidade de novo treinamento a cada execução.

## Tecnologias

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Joblib
- Streamlit
- Google Colab
- GitHub
- Streamlit Community Cloud

## Execução Local

Após clonar o repositório, instale as dependências:

```bash
pip install -r requirements.txt
```

Em seguida, execute:

```bash
streamlit run app/streamlit_app.py
```

## Limitações

Entre as principais limitações do projeto estão:

- série histórica limitada ao período entre 2023 e 2025;
- análise restrita ao estado do Espírito Santo;
- ausência de identificador único das ocorrências;
- utilização de população anual em séries mensais;
- município de registro do boletim não necessariamente corresponde ao local de atuação do autor;
- ausência de variáveis socioeconômicas e outros fatores externos;
- maior dificuldade do modelo para antecipar mudanças abruptas nas taxas;
- validação do MVP realizada com uma amostra reduzida de participantes.

## Repositório e Aplicação

Repositório:

https://github.com/fusieger/ml-cybercrime-public-safety

Aplicação:

https://ml-cybercrime-public-safety-sf6t6tjf3moh4dn7xrn2f3.streamlit.app/

## Autores

Gabriel Henrique Menoncin  
Guilherme Fusieger

Universidade Federal da Fronteira Sul — UFFS  
Campus Chapecó
