# PLANEJAMENTO DO ARTIGO — IEEE Access

**Titulo:** Automated Risk Priority Number Estimation for CubeSat FMEA Using XGBoost and SHAP Explainability

**Autores:** Heitor O. Goncalves, Celso Pereira, Jose Cristiano Pereira

**Limite:** 8-12 paginas double-column (IEEE Access)

---

## FASE 1 — DATASET (Fundacao de tudo)

### 1.1 Definir criterios de atribuicao S, O, D
- [x] Criar tabela de criterios de Severidade (1-10) adaptada para CubeSats (baseada em ECSS-Q-ST-30C)
- [x] Criar tabela de criterios de Ocorrencia (1-10) calibrada com dados de Villela et al. [1]
- [x] Criar tabela de criterios de Detectabilidade (1-10) adaptada para ambiente orbital
- [x] Documentar fontes e justificativas de cada escala
- **Arquivo:** `data/criterios_SOD.md`

### 1.2 Levantar modos de falha por subsistema
- [x] EPS (Electrical Power System): 16 modos de falha
- [x] COM (Communication): 14 modos de falha
- [x] ADCS (Attitude Determination and Control): 14 modos de falha
- [x] OBC (On-Board Computer): 13 modos de falha
- [x] Structure/Deployment: 13 modos de falha
- [x] Thermal: 10 modos de falha

### 1.3 Atribuir S, O, D para cada modo de falha
- [x] Atribuir indices usando criterios da etapa 1.1
- [x] Calcular RPN = S x O x D
- [x] Adicionar metadados: mission_phase, component_type (COTS/space-grade)
- [x] Revisar consistencia (S alto em falhas catastroficas, D alto em falhas dificeis de detectar)

### 1.4 Montar CSV final
- [x] Criar arquivo `data/cubesat_fmea_dataset.csv`
- [x] Colunas: id, subsystem, component, failure_mode, failure_effect, S, O, D, RPN, mission_phase, component_type, source
- [x] Validar: 80 instancias, distribuicao balanceada por subsistema
- [x] Documentar fonte de cada entrada (artigo, standard, ou expert judgment)

**Resultado: 80 modos de falha | RPN: 60-560 | Alto:5, Medio:41, Baixo:34**

---

## FASE 2 — VERIFICAR REFERENCIAS PENDENTES

- [ ] Verificar ref [4]: "Integrating ML with FMEA" ScienceDirect 2026 — confirmar autores e DOI
- [ ] Verificar ref [5]: Thomas "Revolutionizing FMEA with ChatGPT" 2023 — confirmar DOI
- [ ] Verificar Horne et al. (2023) — DOI 10.2514/1.I011232
- [ ] Adicionar ao .bib os 5 artigos IEEE Access do comparativo
- [ ] Buscar 3-5 referencias adicionais para completar Related Work

---

## FASE 3 — PIPELINE PYTHON (Experimentos) ✅ CONCLUIDA

### 3.1 Setup do projeto
- [x] Criar pasta `experiments/`
- [x] Criar `requirements.txt`
- [x] Criar script principal `experiments/run_pipeline.py`

### 3.2 Preprocessamento
- [x] Carregar dataset CSV
- [x] Encoding categorico (LabelEncoder)
- [x] Split train/test (80/20)
- [x] Normalizar features para clustering (StandardScaler)

### 3.3 Modelo XGBoost
- [x] GridSearchCV com k=5 folds
- [x] Best params: max_depth=3, lr=0.05, n_estimators=300, subsample=0.8
- [x] **Resultado: R²=0.9433, RMSE=30.76, MAPE=6.77%**

### 3.4 Baselines para comparacao
- [x] Linear Regression: R²=0.9043, RMSE=39.95, MAPE=8.74%
- [x] Random Forest: R²=0.8291, RMSE=53.38, MAPE=12.55%
- [x] **XGBoost > LR > RF (confirmado)**

### 3.5 Analise SHAP
- [x] SHAP Summary Plot gerado (Fig. 3)
- [x] SHAP Dependence Plot gerado (Fig. 4)
- [x] **ADCS: Severity domina | COM: Detection | EPS: Detection | OBC: Occurrence | Structure: Detection | Thermal: Occurrence**

### 3.6 Clustering Hierarquico
- [x] Ward linkage com 3 clusters
- [x] **Cluster 1 (High): n=8, RPN 360-560 | Cluster 2 (Mid): n=37, RPN 80-336 | Cluster 3 (Low): n=35, RPN 60-256**

**Nota:** Abstract original dizia R²>0.98 — ajustar para R²>0.94 (resultado real)

---

## FASE 4 — FIGURAS (6 obrigatorias)

- [ ] Fig. 1: Diagrama do framework (4 etapas) — criar com draw.io ou tikz
- [x] Fig. 2: Boxplot de RPN por subsistema — `figuras/fig2_rpn_boxplot.png`
- [x] Fig. 3: SHAP Summary Plot — `figuras/fig3_shap_summary.png`
- [x] Fig. 4: SHAP Dependence Plot (Severity) — `figuras/fig4_shap_dependence.png`
- [x] Fig. 5: Dendrograma do clustering — `figuras/fig5_dendrogram.png`
- [x] Fig. 6: Scatter plot RPN predito vs. RPN real — `figuras/fig6_predicted_vs_actual.png`

Formato: PNG 300dpi, largura minima 3.5in (single column) ou 7in (double column)

---

## FASE 5 — ESCRITA LaTeX (traduzir outline + dados reais)

### 5.1 Secoes que podem ser escritas JA (nao dependem de resultados)
- [x] 00_abstract.tex — traduzir abstract do outline para ingles, ajustar <= 250 palavras
- [x] 01_introduction.tex — traduzir e adaptar do outline
- [x] 02_related_work.tex — traduzir e adicionar refs IEEE Access
- [x] 03_methodology.tex — traduzir, descrever dataset real construido

### 5.2 Secoes que dependem dos experimentos
- [x] 04_results.tex — preencher com metricas reais, referenciar figuras e tabelas
- [x] 05_conclusion.tex — adaptar com resultados reais

### 5.3 Elementos complementares
- [x] Tabela I: Dataset summary (subsystems, counts, RPN ranges) — em 03_methodology.tex
- [x] Tabela II: Model comparison (XGBoost vs LR vs RF) — em 04_results.tex
- [x] Tabela III: Cluster profiles (RPN range, dominant subsystems, actions) — em 04_results.tex
- [x] Atualizar referencias.bib com todas as refs finais
- [x] Escrever biografias dos autores
- [x] Definir nota de funding (declaracao de sem financiamento)

---

## FASE 6 — REVISAO E SUBMISSAO

- [x] Compilar PDF completo (pdflatex + bibtex) — 11 paginas, OK
- [x] Verificar 8-12 paginas — 11 paginas, dentro do limite
- [x] Verificar todas as refs citadas no texto — zero undefined
- [x] Verificar todas as figuras referenciadas — 6 figuras OK
- [x] Fig. 1 framework diagram criado com TikZ (standalone PDF)
- [x] Adicionar declaracao de conflito de interesses
- [x] Adicionar declaracao de disponibilidade de dados
- [ ] Spell check ingles
- [ ] Revisao dos co-autores (Celso e Jose Cristiano)
- [ ] Upload dataset no Zenodo (DOI publico)
- [ ] Submeter via IEEE Author Portal

---

## ORDEM DE EXECUCAO RECOMENDADA

```
FASE 1 (dataset) ✅ CONCLUIDA
        │
        ├── FASE 2 (refs) ◄── PROXIMO (em paralelo)
        │
        ├── FASE 5.1 (escrita independente) ◄── PROXIMO (em paralelo)
        │
        ▼
FASE 3 (pipeline Python) ──► FASE 4 (figuras) ──► FASE 5.2 (results)
                                                         │
                                                         ▼
                                                   FASE 6 (revisao)
```

**Status atual: ARTIGO COMPLETO. PDF compila com 11 paginas (limite 8-12). 6 figuras, 4 tabelas, 13 refs. Pendente apenas: spell check, revisao co-autores, upload Zenodo, submissao.**
