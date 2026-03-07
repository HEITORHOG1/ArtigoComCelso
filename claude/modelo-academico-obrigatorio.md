---
inclusion: always

---
# Estrutura Logica do Artigo IEEE

## FLUXO ARGUMENTATIVO

```
Problema (subjetividade do FMEA manual)
  -> Lacuna (nenhum trabalho combina XGBoost+SHAP+CubeSat)
    -> Proposta (framework XAI de 4 etapas)
      -> Validacao (R²>0.98, comparacao com baseline)
        -> Contribuicao (reprodutibilidade, interpretabilidade)
```

## CONEXAO ENTRE SECOES

- Introduction: define o problema e lista 5 contribuicoes
- Related Work: posiciona o trabalho e identifica a lacuna
- Methodology: descreve as 4 etapas do framework
- Results: apresenta evidencias quantitativas e qualitativas
- Conclusion: sintetiza e aponta trabalhos futuros

## ARGUMENTOS-CHAVE POR SECAO

### Introduction

- 25-30% dos CubeSats inaugurais falham
- FMEA e padrao (ECSS-Q-ST-30C, NASA) mas tem limitacao na subjetividade
- ML (XGBoost) + XAI (SHAP) podem superar essa limitacao
- Lacuna: nenhum trabalho aplica isso a CubeSats brasileiros

### Related Work

- Villela et al.: base quantitativa de falhas em CubeSats
- Bouwmeester et al.: testes vs. redundancia
- Al-Refaie et al.: AutoML para FMEA
- Framework XGBoost+SHAP em manufatura (ref [4])
- Gap: inexistente para dominio espacial

### Methodology

- Dataset: 63 modos de falha + 18 estudos
- XGBoost: GridSearchCV, k=5, metricas R²/RMSE/MAPE
- SHAP: summary plot + dependence plot
- Clustering: Ward, 3 grupos

### Results

- XGBoost R²>0.98, MAPE<3%
- SHAP: Severidade domina em estrutura/deployment, Detectabilidade em COM
- 3 clusters: alto (>400), medio (200-400), baixo (<200)
- Variancia inter-avaliadores reduzida

### Conclusion

- Framework validado com alta fidelidade preditiva
- SHAP oferece granularidade por subsistema
- Limitacao: dataset pequeno (63 instancias)
- Futuro: OPSSAT-AD, LSTM/Transformers, mais missoes
