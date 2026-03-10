# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

This is an **IEEE Access article** written in Markdown (outline phase), to be converted to LaTeX for submission.

**Title:** Automated Risk Priority Number Estimation for CubeSat FMEA Using XGBoost and SHAP Explainability

**Authors:**
1. Heitor Oliveira Goncalves (ORCID: 0000-0002-5866-2213) — heitorhog@gmail.com (corresponding)
2. Celso Pereira — cpereira.eng@gmail.com
3. Jose Cristiano Pereira — josecristiano.pereira@ucp.br

**Affiliation (all):** Center for Engineering and Computing, Catholic University of Petropolis, Petropolis, RJ, Brazil

**Topic:** A framework combining XGBoost, SHAP explainability, and hierarchical clustering to automate and calibrate RPN estimation in CubeSat FMEA analyses. Trained on 63 failure modes from Brazilian nanosatellites (AESP-14, FloripaSat) plus data from 18 literature studies.

## Approved Abstract (Canonical Reference)

This is the single source of truth for the article scope:

> A FMEA ocupa lugar central na engenharia de confiabilidade de nanossatelites. O metodo apresenta limitacao estrutural: subjetividade na atribuicao manual de S, O e D para calculo do RPN. Este trabalho propoe um framework XAI baseado em XGBoost para automatizar e calibrar a estimativa do RPN em missoes CubeSat. O modelo foi treinado sobre 63 modos de falha de nanossatelites brasileiros, complementado por dados de 18 estudos da literatura. O XGBoost alcancou R² superior a 0,98. SHAP foi aplicado para interpretabilidade, revelando que Severidade domina em subsistemas estruturais/deployment e Detectabilidade em comunicacao/ADCS. Agrupamento hierarquico classificou modos de falha em tres grupos de risco.

**Keywords:** FMEA, CubeSat, XGBoost, SHAP, Explainable AI, Risk Priority Number, Machine Learning, Space Systems Reliability

## Article Structure (IEEE Access Format)

```
I.   INTRODUCTION
II.  RELATED WORK
     2.1 Confiabilidade e analise de falhas em CubeSat
     2.2 Machine Learning para estimativa de RPN em FMEA
     2.3 Deteccao de anomalias em telemetria com ML
     2.4 Explainable AI em sistemas criticos
     2.5 Lacuna identificada na literatura
III. METHODOLOGY
     3.1 Visao geral do framework
     3.2 Construcao do dataset
     3.3 Modelo XGBoost e protocolo de validacao
     3.4 Analise de explicabilidade com SHAP
     3.5 Agrupamento hierarquico
IV.  RESULTS AND DISCUSSION
     4.1 Desempenho preditivo do modelo
     4.2 Analise SHAP por subsistema
     4.3 Grupos de risco identificados
     4.4 Discussao critica
V.   CONCLUSION
```

## Article Format Requirements (IEEE Access)

- **Template:** `ieeeaccess.cls` (official IEEE Access journal template, version 2024-04-29)
- **Template location:** `artigo/` folder with all required files (cls, bst, fonts, logos)
- **Document class:** `\documentclass{ieeeaccess}` (NOT conference `IEEEtran`)
- **Length:** 8-12 pages in double-column format
- **Abstract:** 150-250 words, self-contained, no abbreviations/footnotes/references/equations
- **Minimum keywords:** 5, alphabetical order
- **Language:** English (full article for IEEE Access)
- **Figures:** Use `\Figure[t!](topskip=0pt, botskip=0pt, midskip=0pt){file.png}` macro
- **Tables:** Caption above with `\caption{\textbf{Title}}`
- **First paragraph:** Must use `\PARstart{F}{irst}` for drop cap
- **Biographies:** Required at end (`\begin{IEEEbiographynophoto}`)
- **End of document:** Must include `\EOD` before `\end{document}`
- **Figures planned (minimum 6):**
  - Fig. 1: Diagrama do framework (fluxo de 4 etapas)
  - Fig. 2: Distribuicao de RPN por subsistema (boxplot)
  - Fig. 3: SHAP Summary Plot (importancia global)
  - Fig. 4: SHAP Dependence Plot (Severidade x RPN por subsistema)
  - Fig. 5: Dendrograma do clustering hierarquico (3 grupos)
  - Fig. 6: Scatter plot RPN predito vs. RPN real

## Technical Scope

### Framework Components (4 stages)
1. Data collection and structuring (dataset of failure modes)
2. XGBoost model training for RPN prediction
3. SHAP analysis for per-subsystem explainability
4. Hierarchical clustering for actionable risk groups

### Dataset
- **Primary source:** 63 failure modes from AESP-14 and FloripaSat (Brazilian nanosatellites)
- **Secondary source:** Data from 18 literature studies
- **Input features:** S (1-10), O (1-10), D (1-10), subsystem (EPS/ADCS/COM/Thermal/Structure/OBC), mission phase, component type (COTS/space-grade)
- **Output:** RPN = S x O x D

### Model Details
- **Algorithm:** XGBoost (gradient boosting)
- **Hyperparameter tuning:** GridSearchCV, k=5 stratified cross-validation
- **Metrics:** R², RMSE, MAPE
- **Baselines:** Linear regression, Random Forest
- **Target performance:** R² > 0.98, MAPE < 3%

### Explainability
- **SHAP Summary Plot:** Global feature importance
- **SHAP Dependence Plot:** Severity x RPN by subsystem
- **Key findings:** Severity dominates in structural/deployment; Detectability dominates in COM/ADCS

### Clustering
- **Method:** Hierarchical agglomerative (Ward linkage)
- **Features:** Normalized [S, O, D, RPN]
- **Clusters:** 3 risk groups (high >400 RPN, intermediate 200-400, low <200)

## Verified References

| # | Reference | Status | DOI |
|---|-----------|--------|-----|
| [1] | Villela et al. "Towards the thousandth CubeSat" 2019 | Confirmed | 10.1155/2019/5063145 |
| [2] | Bouwmeester et al. "Improving CubeSat reliability" 2022 | Confirmed | 10.1016/j.ress.2021.108288 |
| [3] | Al-Refaie et al. "Enhancing FMEA Using Auto ML" 2020 | Confirmed | 10.3390/pr8020224 |
| [4] | "Integrating ML with FMEA" ScienceDirect 2026 | Verify authors | 10.1016/S2590-1230(26)00171-4 |
| [5] | Thomas "Revolutionizing FMEA with ChatGPT" 2023 | Verify | 10.1007/s11668-023-01659-y |
| [6] | Cespedes et al. "ML for Anomaly Detection in CubeSat Solar Panels" 2022 | Confirmed | 10.3390/app12178634 |
| [7] | Ruszczak et al. "OPS-SAT benchmark" 2025 | Confirmed | 10.1038/s41597-025-05035-3 |

## Strict Content Rules

### Zero Invention Policy
- **NEVER** invent data, statistics, or references
- **NEVER** fabricate DOIs or bibliography entries
- **NEVER** add methodologies not in the approved scope
- **NEVER** expand beyond the XGBoost-SHAP-CubeSat framework
- If data is not available, mark as placeholder: *(to be filled with experimental results)*

### Scope Boundaries
1. **Problem:** Subjectivity in manual RPN assignment for CubeSat FMEA
2. **Solution:** XGBoost + SHAP + hierarchical clustering
3. **Domain:** CubeSat/nanosatellite missions (Brazilian focus)
4. **Validation:** Comparison with expert-based conventional FMEA
5. **Contribution:** Reproducible XAI framework for space systems reliability

## Terminology Consistency

- "Risk Priority Number (RPN)" - always define on first use
- "FMEA" - "Failure Mode and Effects Analysis (FMEA)" on first use
- "XGBoost" - no expansion needed (proper name)
- "SHAP" - "SHapley Additive Explanations (SHAP)" on first use
- "XAI" - "Inteligencia Artificial Explicavel (XAI)" on first use
- "CubeSat" - capitalized, no hyphen
- "nanossatelite" - Portuguese, lowercase
- Subsystems: EPS, ADCS, COM, OBC, Thermal, Structure
- Indices: Severidade (S), Ocorrencia (O), Detectabilidade (D)

## Writing Style

- **Tone:** Formal, objective, scientific
- **Voice:** Impersonal ("the model achieved", "it is proposed")
- **No superlatives:** Avoid "best", "revolutionary". Use "results indicate", "demonstrated"
- **Claims require citations:** Every factual claim needs a reference
- **Language:** English throughout (IEEE Access standard)

## Repository Structure

```
artigo/
├── main.tex                    # Main document (\documentclass{ieeeaccess})
├── ieeeaccess.cls              # IEEE Access class file
├── IEEEtran.cls                # Base IEEE class
├── IEEEtran.bst                # Bibliography style
├── spotcolor.sty               # Required style file
├── referencias.bib             # BibTeX references
├── t1-formata*, t1-times*, ... # Required font files
├── secoes/
│   ├── 00_abstract.tex
│   ├── 01_introduction.tex
│   ├── 02_related_work.tex
│   ├── 03_methodology.tex
│   ├── 04_results.tex
│   └── 05_conclusion.tex
└── figuras/
    ├── logo.png, notaglinelogo.png, bullet.png  # IEEE Access logos
    └── (article figures to be added)
```

## Build Commands

```bash
cd "g:/ArtigoComCelso/artigo"

# Full compilation (citations + cross-references)
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

# Quick compilation (no bibliography update)
pdflatex main.tex
```

## Current Status

- LaTeX structure created with IEEE Access template (ieeeaccess.cls)
- Outline v2 complete with verified references
- All sections have TODO placeholders
- Sections IV (Results) pending experimental data
- Next steps: write article content, implement Python pipeline, generate results

## Submission Checklist

- [ ] IEEE Access template applied
- [ ] 8-12 pages double-column
- [ ] Abstract <= 250 words
- [ ] Min 5 keywords
- [ ] Min 6 figures
- [ ] All references verified
- [ ] Conflict of interest statement
- [ ] Data availability statement (Zenodo)
