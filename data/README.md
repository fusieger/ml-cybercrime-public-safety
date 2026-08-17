# Dados

Este diretório contém os conjuntos de dados utilizados no projeto "Predição Espaço-Temporal de Estelionatos e Fraudes Digitais utilizando Machine Learning".

## Estrutura

- `raw/`: dados originais obtidos das fontes oficiais, sem alterações.
- `processed/`: dados resultantes das etapas de limpeza, integração
  e transformação.

---

## IBGE — Estimativas da População

**Instituição:** Instituto Brasileiro de Geografia e Estatística (IBGE)

**Fonte:** Estimativas da População

**Página oficial:**
https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html
https://www.ibge.gov.br/estatisticas/sociais/populacao/37734-relacao-da-populacao-dos-municipios-para-publicacao-no-tcu.html
https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html

**Granularidade espacial:** Município

**Granularidade temporal:** Anual

**Utilização prevista:**
Os dados populacionais serão utilizados para normalização das ocorrências criminais, incluindo o cálculo da taxa de estelionatos por 100 mil habitantes.

### Arquivos coletados

| Ano | Arquivo | Fonte |
|---|---|---|
| 2018 | estimativa_populacao_2018.xls | Estimativa IBGE |
| 2019 | estimativa_populacao_2019.xls | Estimativa IBGE |
| 2020 | estimativa_populacao_2020.xls | Estimativa IBGE |
| 2021 | estimativa_populacao_2021.xls | Estimativa IBGE |
| 2022 | populacao_censo_2022.xlsx | Censo Demográfico 2022 |
| 2023 | populacao_tcu_2023.xlsx | População dos Municípios / TCU |
| 2024 | estimativa_populacao_2024.xlsx | Estimativa IBGE |
| 2025 | estimativa_populacao_2025.xlsx | Estimativa IBGE |

### Observações

Os arquivos presentes em `raw/` correspondem aos dados originais obtidos das fontes oficiais e não devem ser modificados diretamente.

Os anos de 2022 e 2023 possuem fonte/metodologia distinta das estimativas populacionais anuais tradicionais e serão analisados e documentados durante a etapa de preparação dos dados.
