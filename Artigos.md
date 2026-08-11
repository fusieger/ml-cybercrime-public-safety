
### 3.3 *(Extra)* Crime Forecasting: A Spatio-temporal Analysis with Deep Learning Models (arXiv, CNN-LSTM)
* **Pré-print / Artigo Completo:** [Acessar no arXiv](https://arxiv.org/abs/2502.07465)
* **Resumo Metodológico:** Apresenta arquiteturas híbridas de *Deep Learning* que combinam **Redes Neurais Convolucionais (CNN)** para captura de características espaciais e **Redes de Memória de Longo e Curto Prazo (LSTM)** para dinâmicas temporais.
* **Principais Destaques:**
  * **Arquitetura CNN-LSTM:** A camada CNN interpreta a grade territorial da cidade como uma "imagem" de intensidade criminal, enquanto a LSTM processa a sequência evolutiva ao longo do tempo.
  * **Estado da Arte (SOTA):** Supera modelos tradicionais (como ARIMA, KDE e Random Forest isolado) em cenários de alta densidade urbana com múltiplas variáveis contextuais (clima, eventos de massa, pontos de interesse de transporte).

---

## 4. Síntese Comparativa das Tecnologias e Algoritmos

| Classe Metodológica | Algoritmos Típicos | Aplicação Principal na Segurança Pública | Pontos Fortes | Limitações |
| :--- | :--- | :--- | :--- | :--- |
| **Estatística Espacial** | KDE, SEPP (ETAS) | Mapeamento de manchas de calor (*Hotspots*); policiamento ostensivo imediato. | Baixo custo computacional; alta interpretabilidade visual. | Dificuldade em capturar relações lineares/não-lineares complexas com variáveis externas. |
| **ML Supervisionado** | Random Forest, XGBoost, LightGBM | Predição em grades espaciais; pontuação de risco operacional por bairro/zona. | Interpretabilidade (*Feature Importance*); robustez com dados tabulares operacionais. | Requer engenharia de atributos (*Feature Engineering*) manual e bem estruturada. |
| **Deep Learning (Espaço-Temporal)** | CNN-LSTM, GNN (Graph Neural Networks) | Predição fina de séries temporais espaciais; integração do grafo viário urbano. | Alta acurácia em grandes centros urbanos; captura dinâmicas complexas de transbordo. | Exige grande volume de dados históricos; menor explicabilidade (efeito "caixa preta"). |
| **Processamento de Linguagem Natural (NLP)** | TF-IDF, BERTimbau, Transformers em PT-BR | Triagem de BOs de estelionato; agrupamento de narrativas criminais por *modus operandi*. | Identificação de quadrilhas e crimes cometidos com a mesma técnica textual ou bancária. | Sensível a erros ortográficos, abreviações policiais e variações regionais na redação. |

---

## 5. Recomendações Práticas para Aplicação em Segurança Pública

1. **Governança de Dados e Georreferenciamento:**
   * Priorizar a qualidade do georreferenciamento de chamados (190) e registros (BOs) antes de aplicar arquiteturas de *Deep Learning*. Dados imprecisos geram *hotspots* distorcidos.
2. **Uso Híbrido de Métodos (KDE + ML):**
   * Em operações diárias de batalhão, mapas visuais baseados em KDE ou Random Forest (como demonstrado no **Predspot**) oferecem retorno imediato e maior aceitação pela tropa do que sistemas puramente baseados em caixas pretas.
3. **Triagem de Estelionato via NLP (Inquérito Policial Inteligente):**
   * Empregar pipelines de NLP adaptados ao português brasileiro (como modelos baseados no *BERTimbau*) para extrair entidades automáticas de BOs eletrônicos (chaves Pix, telefones, links fraudulentos e padrões de narrativa de golpe), conectando inquéritos dispersos entre delegacias.

---
*Documento compilado como material de referência acadêmica, técnica e operacional em Criminologia Computacional e Inteligência Artificial na Segurança Pública.*
