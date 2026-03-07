---
inclusion: always
---

# Normas de Formatacao - IEEE Access

## FORMATO DO ARTIGO

- **Template:** IEEE Access (LaTeX ou Word)
- **Layout:** Dupla coluna
- **Comprimento:** 8-12 paginas
- **Fonte:** Times New Roman (conforme template IEEE)
- **Idioma corpo:** Portugues
- **Idioma abstract/keywords:** Ingles

## ESTRUTURA OBRIGATORIA IEEE ACCESS

```
Abstract (max 250 palavras)
Keywords (min 5)
I.   INTRODUCTION
II.  RELATED WORK
III. METHODOLOGY
IV.  RESULTS AND DISCUSSION
V.   CONCLUSION
REFERENCES
```

## REGRAS DE CITACAO IEEE

- Citacoes numericas entre colchetes: [1], [2], [3]
- Multiplas citacoes: [1]-[3] ou [1], [4], [7]
- Citacao narrativa: "Villela et al. [1] demonstraram..."
- Ordem das referencias: por ordem de aparicao no texto

## FIGURAS E TABELAS

### Figuras

- Caption abaixo da figura
- Referencia no texto: "Fig. 1", "Fig. 2"
- Resolucao minima: 300 dpi
- Largura: single-column ou double-column conforme necessidade

### Tabelas

- Caption acima da tabela
- Referencia no texto: "Table I", "Table II"
- Numeracao em romanos maiusculos (padrao IEEE)
- Usar booktabs style (sem linhas verticais)

## FIGURAS PLANEJADAS (MINIMO 6)

1. Fig. 1 - Diagrama do framework proposto (fluxo de 4 etapas)
2. Fig. 2 - Distribuicao de RPN por subsistema (boxplot)
3. Fig. 3 - SHAP Summary Plot (importancia global das features)
4. Fig. 4 - SHAP Dependence Plot (Severidade x RPN por subsistema)
5. Fig. 5 - Dendrograma do clustering hierarquico com 3 grupos
6. Fig. 6 - Scatter plot: RPN predito vs. RPN real

## SECOES COM CONTEUDO PENDENTE

- Secao IV (Results): Marcada como placeholder ate gerar resultados experimentais
- Preencher com dados reais apos executar o pipeline Python (XGBoost + SHAP + clustering)
