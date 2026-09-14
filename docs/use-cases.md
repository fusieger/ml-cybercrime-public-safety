UC01 — Consultar evolução das ocorrências

Ator: Analista de segurança pública
Objetivo: acompanhar a evolução mensal de estelionatos e fraudes em um município.
Pré-condição: dados processados e disponíveis.
Fluxo principal: o usuário seleciona um município; o sistema recupera os dados históricos; calcula ou consulta a taxa por 100 mil habitantes; apresenta série temporal e indicadores.
Resultado esperado: visualização da evolução das ocorrências e taxas.

UC02 — Consultar previsão mensal

Ator: Analista de segurança pública
Objetivo: consultar a taxa prevista de ocorrências para o próximo mês.
Pré-condição: modelo treinado e dados históricos disponíveis.
Fluxo principal: o usuário seleciona o município e período; o sistema utiliza as características históricas; executa o modelo; apresenta a previsão.
Resultado esperado: taxa prevista para o mês seguinte.

UC03 — Comparar previsão com valor observado

Ator: Analista ou pesquisador
Objetivo: avaliar o desempenho da previsão.
Pré-condição: existir previsão e valor real para o período.
Fluxo principal: o sistema recupera previsão e valor observado; calcula a diferença; apresenta erro e métricas associadas.
Resultado esperado: identificação da qualidade da previsão e de possíveis desvios.

UC04 — Consultar ranking de municípios

Ator: Analista de segurança pública
Objetivo: identificar os municípios com maior taxa prevista.
Fluxo principal: o usuário seleciona o mês; o sistema recupera as previsões de todos os municípios; ordena os resultados; apresenta o ranking.
Resultado esperado: lista ordenada dos municípios segundo a taxa prevista.
