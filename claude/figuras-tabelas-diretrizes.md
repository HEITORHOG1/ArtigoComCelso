---
inclusion: always
---

# Diretrizes para Figuras e Tabelas do Artigo IEEE

## FIGURAS OBRIGATORIAS

### Fig. 1 - Framework Proposto
- **Tipo:** Diagrama de fluxo (4 etapas)
- **Conteudo:** Dataset -> XGBoost Training -> SHAP Analysis -> Hierarchical Clustering
- **Secao:** III.A (Visao geral do framework)

### Fig. 2 - Distribuicao de RPN por Subsistema
- **Tipo:** Boxplot ou histograma
- **Conteudo:** RPN distribuido por EPS, ADCS, COM, Thermal, Structure, OBC
- **Secao:** IV.1 (Desempenho preditivo)

### Fig. 3 - SHAP Summary Plot
- **Tipo:** Beeswarm plot (gerado pelo SHAP)
- **Conteudo:** Importancia global de S, O, D, subsistema, fase, tipo componente
- **Secao:** IV.2 (Analise SHAP)

### Fig. 4 - SHAP Dependence Plot
- **Tipo:** Scatter com coloracao por subsistema
- **Conteudo:** Severidade vs. SHAP value, colorido por subsistema
- **Secao:** IV.2 (Analise SHAP)

### Fig. 5 - Dendrograma
- **Tipo:** Dendrograma hierarquico
- **Conteudo:** 3 clusters com corte visual, Ward linkage
- **Secao:** IV.3 (Grupos de risco)

### Fig. 6 - RPN Predito vs. Real
- **Tipo:** Scatter plot com linha de identidade
- **Conteudo:** Valores preditos pelo XGBoost vs. valores reais, R² anotado
- **Secao:** IV.1 (Desempenho preditivo)

## TABELAS SUGERIDAS

### Table I - Dataset Summary
- Features, escalas, descricao

### Table II - Model Performance Comparison
- XGBoost vs. Linear Regression vs. Random Forest (R², RMSE, MAPE)

### Table III - Cluster Profiles
- Grupo A/B/C: RPN range, subsistemas predominantes, acoes recomendadas

## REGRAS GERAIS

- Sempre referenciar figuras/tabelas no texto ANTES de apresenta-las
- Figuras geradas pelo pipeline Python (matplotlib/seaborn/shap)
- Qualidade minima 300 dpi para submissao
- Figuras devem ser autoexplicativas com legends claras
