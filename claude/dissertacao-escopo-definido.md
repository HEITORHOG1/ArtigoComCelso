---
inclusion: always
---

# Escopo Definido do Artigo - Sem Invencoes

## TITULO DO ARTIGO

**Titulo:** Automated Risk Priority Number Estimation for CubeSat FMEA Using XGBoost and SHAP Explainability

**Formato:** IEEE Access (8-12 paginas, dupla coluna)

## ESCOPO RESTRITO APROVADO

1. **Problema:** Subjetividade na atribuicao manual de S, O e D no FMEA de CubeSats
2. **Solucao:** Framework XAI com XGBoost + SHAP + clustering hierarquico
3. **Dominio:** Missoes CubeSat/nanossatelites (foco brasileiro: AESP-14, FloripaSat)
4. **Validacao:** Comparacao com FMEA convencional por especialistas
5. **Contribuicao:** Framework XAI reprodutivel para engenharia de confiabilidade espacial

## CONTRIBUICOES DO ARTIGO (5)

1. Framework XAI completo e reprodutivel para automacao do RPN em FMEA de CubeSats
2. Dataset estruturado com 63 modos de falha de missoes brasileiras + 18 estudos da literatura
3. Analise SHAP identificando drivers dominantes de risco por subsistema
4. Agrupamento hierarquico em 3 classes de risco para priorizacao de acoes corretivas
5. Comparacao quantitativa framework proposto vs. avaliacao convencional por especialistas

## ELEMENTOS TECNICOS DEFINIDOS

- **Modelo:** XGBoost (gradient boosting para dados tabulares)
- **Explicabilidade:** SHAP (SHapley Additive Explanations)
- **Clustering:** Hierarquico aglomerativo (Ward linkage)
- **Dataset:** 63 modos de falha, features: S, O, D, subsistema, fase de missao, tipo de componente
- **Metricas:** R², RMSE, MAPE
- **Baselines:** Regressao linear, Random Forest

## SUBSISTEMAS COBERTOS

- EPS (Electrical Power System)
- ADCS (Attitude Determination and Control System)
- COM (Communication)
- Thermal
- Structure/Deployment
- OBC (On-Board Computer)

## REGRAS FUNDAMENTAIS - ZERO INVENCAO

- **NUNCA** inventar dados, estatisticas ou referencias
- **NUNCA** fabricar DOIs ou entradas bibliograficas
- **NUNCA** adicionar metodologias fora do escopo (ex: redes neurais, LSTMs como metodo principal)
- **NUNCA** expandir alem do framework XGBoost-SHAP-CubeSat
- **NUNCA** inventar resultados experimentais
- Dados pendentes devem ser marcados como *(a ser preenchido com resultados experimentais)*

## VERIFICACAO DE CONSISTENCIA

Antes de produzir qualquer conteudo, verificar:

- [ ] Esta alinhado com o abstract aprovado?
- [ ] Mantem o escopo XGBoost + SHAP + CubeSat?
- [ ] Nao inventa dados ou estudos?
- [ ] Usa terminologia consistente?
- [ ] Respeita o formato IEEE Access?
- [ ] Referencias sao verificadas?
