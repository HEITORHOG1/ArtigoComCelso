# Artigos de Referencia da IEEE Access - Comparativo

## Objetivo

5 artigos publicados na IEEE Access relevantes ao nosso tema (FMEA + ML + CubeSat + XAI).
Servem como benchmark de estrutura, abordagem e qualidade para nosso artigo.

---

## Artigo 1: AMWRPN - Ambiguity Measure Weighted RPN Model for FMEA

- **Titulo:** AMWRPN: Ambiguity Measure Weighted Risk Priority Number Model for Failure Mode and Effects Analysis
- **Journal:** IEEE Access
- **URL:** https://ieeexplore.ieee.org/document/8358690/
- **Ano:** 2018
- **Tema:** Propoe modelo AMWRPN que pondera fatores de risco (S, O, D) usando medida de ambiguidade baseada em Dempster-Shafer evidence theory. Constroi peso exponencial de cada fator de risco conforme certeza das avaliacoes dos especialistas.
- **Relevancia para nos:**
  - Aborda diretamente o problema da subjetividade no RPN tradicional (mesmo problema que atacamos)
  - Usa abordagem matematica/estatistica, nao ML - nosso artigo oferece alternativa baseada em dados
  - Boa referencia para a secao Related Work sobre limitacoes do RPN classico

---

## Artigo 2: A New Geometric Mean FMEA Method Based on Information Quality

- **Titulo:** A New Geometric Mean FMEA Method Based on Information Quality
- **Journal:** IEEE Access
- **URL:** https://ieeexplore.ieee.org/document/8761847/
- **Ano:** 2019
- **Tema:** Propoe metodo de media geometrica para FMEA usando distribuicao fuzzy para capturar opiniao de especialistas. Calcula RPN com base na qualidade da informacao ao combinar multiplas distribuicoes de probabilidade.
- **Relevancia para nos:**
  - Outro artigo que tenta resolver a subjetividade do RPN, desta vez via fuzzy + media geometrica
  - Nao usa ML nem explainability - nosso framework e mais moderno e interpretavel
  - Referencia para mostrar evolucao das abordagens de melhoria do RPN

---

## Artigo 3: FMEA Approach Based on Avoidance of Aggregation Discrepancy

- **Titulo:** Failure Mode and Effect Analysis (FMEA) Approach Based on Avoidance of Aggregation Discrepancy
- **Journal:** IEEE Access
- **URL:** https://ieeexplore.ieee.org/document/10075671/
- **Ano:** 2023
- **Tema:** Identifica problema de discrepancia de agregacao no FMEA em grupo (decisao multicriterio). Propoe metodo AADFMEA baseado em otimizacao multi-objetivo para melhorar precisao da avaliacao coletiva usando escala qualitativa de 10 pontos.
- **Relevancia para nos:**
  - Artigo recente na IEEE Access sobre melhoria do FMEA
  - Foca no problema de grupo (multiplos avaliadores), nos focamos na automacao via ML
  - Mostra que IEEE Access continua publicando artigos sobre FMEA melhorado

---

## Artigo 4: Fault Analysis and Mitigation Techniques of the I2C Bus for Nanosatellite Missions

- **Titulo:** Fault Analysis and Mitigation Techniques of the I2C Bus for Nanosatellite Missions
- **Journal:** IEEE Access
- **URL:** https://ieeexplore.ieee.org/document/10082916/
- **DOI:** 10.1109/ACCESS.2023.3262410
- **Ano:** 2023
- **Tema:** Analise detalhada de falhas do barramento I2C em missoes de nanossatelites. Identifica riscos ao sucesso de missao e propoe tecnicas de mitigacao. Destaca que falhas do I2C podem ser catastroficas para CubeSats.
- **Relevancia para nos:**
  - Artigo da IEEE Access especificamente sobre falhas em nanosatelites/CubeSats
  - Foca em analise de falha de componente especifico (I2C), nos fazemos FMEA sistematico
  - Valida que IEEE Access publica trabalhos sobre confiabilidade de CubeSats
  - Pode ser citado na secao de CubeSat reliability

---

## Artigo 5: Explainable AI Framework Using XGBoost With SHAP and LIME

- **Titulo:** Explainable AI Framework Using XGBoost With SHAP and LIME for Multi-Scale Household Energy Forecasting
- **Journal:** IEEE Access
- **URL:** https://ieeexplore.ieee.org/document/11141411/
- **Ano:** 2025
- **Tema:** Framework de XAI usando XGBoost com SHAP e LIME para previsao de consumo de energia. Demonstra como SHAP revela importancia de features globais e locais, e como XGBoost combinado com explicabilidade melhora confianca nos modelos.
- **Relevancia para nos:**
  - Usa exatamente a mesma stack tecnica: XGBoost + SHAP
  - Artigo recente e aceito na IEEE Access - valida que a combinacao XGBoost+SHAP e publicavel
  - Dominio diferente (energia), mas framework analogo - nos aplicamos ao dominio espacial/FMEA
  - Referencia forte para a secao de XAI e para justificar escolha do XGBoost+SHAP

---

## Tabela Comparativa: Artigos IEEE Access vs. Nosso Artigo

| Aspecto | Art.1 AMWRPN | Art.2 Geom.Mean | Art.3 AADFMEA | Art.4 I2C Nano | Art.5 XAI XGBoost | **Nosso Artigo** |
|---|---|---|---|---|---|---|
| **Dominio** | FMEA generico | FMEA generico | FMEA generico | Nanosatelites | Energia | **CubeSat FMEA** |
| **Problema** | Subjetividade RPN | Subjetividade RPN | Agregacao grupo | Falha I2C | Previsao energia | **Subjetividade RPN** |
| **Metodo** | Dempster-Shafer | Fuzzy + geom.mean | Multi-obj optim. | Analise experimental | XGBoost+SHAP+LIME | **XGBoost+SHAP+Clustering** |
| **Usa ML?** | Nao | Nao | Nao | Nao | Sim (XGBoost) | **Sim (XGBoost)** |
| **Usa XAI?** | Nao | Nao | Nao | Nao | Sim (SHAP+LIME) | **Sim (SHAP)** |
| **Foco espacial?** | Nao | Nao | Nao | Sim (CubeSat) | Nao | **Sim (CubeSat)** |
| **RPN como alvo?** | Sim | Sim | Sim | Nao | Nao | **Sim** |
| **Clustering?** | Nao | Nao | Nao | Nao | Nao | **Sim (hierarquico)** |
| **Dataset real?** | Exemplos literatura | Exemplos literatura | Exemplos literatura | Testes experimentais | Dados residenciais | **63 modos de falha reais** |

## Diferenciais do Nosso Artigo (Gap Analysis)

Com base na comparacao acima, nosso artigo se diferencia por:

1. **Unico a combinar ML + FMEA + CubeSat:** Nenhum dos artigos IEEE Access encontrados combina machine learning com FMEA especificamente para CubeSats
2. **Explainability no FMEA:** Artigos 1-3 melhoram o RPN por vias matematicas/fuzzy, mas sem interpretabilidade via SHAP
3. **Dataset de missoes reais brasileiras:** Artigos 1-3 usam exemplos genericos da literatura; nos temos dados de AESP-14 e FloripaSat
4. **Clustering para grupos de risco acionaveis:** Nenhum dos artigos encontrados usa clustering hierarquico para classificar modos de falha em grupos de risco
5. **Framework end-to-end:** Da coleta de dados ate grupos de risco interpretaveis, um pipeline completo reproduzivel

## Como Usar Esses Artigos

- **Citacoes diretas:** Artigos 1, 2, 3 podem ser citados na secao II.2 (ML para RPN) para mostrar abordagens anteriores
- **Referencia de dominio:** Artigo 4 pode ser citado na secao II.1 (Confiabilidade CubeSat)
- **Referencia tecnica:** Artigo 5 pode ser citado na secao II.4 (XAI) para validar stack XGBoost+SHAP
- **Justificativa de gap:** A tabela comparativa alimenta diretamente a secao II.5 (Lacuna identificada)
