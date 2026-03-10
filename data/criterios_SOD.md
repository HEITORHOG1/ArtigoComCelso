# Criterios de Atribuicao S, O, D para FMEA de CubeSats

Escalas adaptadas para o dominio de nanossatelites/CubeSats.
Baseadas em ECSS-Q-ST-30-02C, MIL-STD-1629A e AIAG FMEA (4th ed.), com adaptacoes
para o contexto de missoes CubeSat universitarias.

---

## TABELA 1 — SEVERIDADE (S)

Avalia o impacto da falha sobre a missao, o satelite e a seguranca.

| S | Classificacao | Descricao (contexto CubeSat) | Exemplo |
|---|---|---|---|
| 1 | None | Sem efeito perceptivel na missao | Variacao cosmetica em telemetria |
| 2 | Very minor | Degradacao insignificante, sem impacto funcional | Leve aumento de ruido em sensor nao-critico |
| 3 | Minor | Pequena degradacao de desempenho, missao nao afetada | Reduzida margem de potencia em condicao nominal |
| 4 | Low | Degradacao moderada de um subsistema, missao parcialmente afetada | Reducao de 10-20% na taxa de downlink |
| 5 | Moderate | Perda parcial de funcionalidade de um subsistema | Perda de um canal de comunicacao redundante |
| 6 | Significant | Perda significativa de desempenho, objetivo secundario comprometido | Falha em payload secundario, missao primaria ok |
| 7 | High | Perda de um objetivo primario da missao | Falha no payload principal, subsistemas operacionais |
| 8 | Very high | Perda de multiplos objetivos da missao | Falha em EPS degrada COM + payload |
| 9 | Critical | Perda total da missao (sem risco de seguranca) | Satelite inoperante mas sem debris perigoso |
| 10 | Catastrophic | Perda total da missao com risco de seguranca ou debris | Falha em deployment gera debris; risco em reentrada |

**Referencia:** ECSS-Q-ST-30-02C Table 5-1 (severity categories I-IV), adaptada para escala 1-10.

---

## TABELA 2 — OCORRENCIA (O)

Avalia a probabilidade de ocorrencia do modo de falha durante a vida da missao.
Calibrada com dados estatisticos de Villela et al. (2019) e Bouwmeester et al. (2022).

| O | Classificacao | Probabilidade estimada | Taxa de falha por missao | Referencia |
|---|---|---|---|---|
| 1 | Extremely unlikely | < 1 em 10.000 missoes | < 0.0001 | Componente space-grade qualificado, redundante |
| 2 | Remote | 1 em 5.000 | 0.0002 | Componente space-grade qualificado |
| 3 | Very low | 1 em 2.000 | 0.0005 | Componente COTS com screening rigoroso |
| 4 | Low | 1 em 500 | 0.002 | Componente COTS com screening basico |
| 5 | Moderate-low | 1 em 200 | 0.005 | Componente COTS sem screening, ambiente moderado |
| 6 | Moderate | 1 em 100 | 0.01 | Falha documentada em <5% das missoes CubeSat |
| 7 | Moderate-high | 1 em 50 | 0.02 | Falha documentada em 5-10% das missoes CubeSat |
| 8 | High | 1 em 20 | 0.05 | Falha documentada em 10-20% das missoes (ex: COM) |
| 9 | Very high | 1 em 10 | 0.10 | Falha documentada em 20-30% das missoes inaugurais |
| 10 | Almost certain | > 1 em 5 | > 0.20 | Falha esperada sem mitigacao (ex: AESP-14 antenna) |

**Referencia:** Villela et al. (2019) reportam ~25-30% de falha em missoes inaugurais.
Bouwmeester et al. (2022) fornecem dados de falha por subsistema via Kaplan-Meier.

---

## TABELA 3 — DETECTABILIDADE (D)

Avalia a capacidade de detectar a falha ou sua causa antes do impacto na missao.
No contexto CubeSat, a deteccao depende de: testes em solo, telemetria, e diagnostico em orbita.

| D | Classificacao | Descricao (contexto CubeSat) | Metodo de deteccao |
|---|---|---|---|
| 1 | Almost certain | Falha sempre detectada antes do lancamento | Teste funcional automatizado em solo |
| 2 | Very high | Falha quase sempre detectada em teste | Teste ambiental completo (thermal-vac, vibracao) |
| 3 | High | Alta probabilidade de deteccao em integracao | Inspecao visual + teste eletrico de integracao |
| 4 | Moderately high | Detectavel por revisao de projeto ou simulacao | Revisao de projeto + simulacao termica/eletrica |
| 5 | Moderate | Detectavel por telemetria nominal em orbita | Monitoramento de housekeeping (tensao, temp) |
| 6 | Low-moderate | Detectavel apenas por telemetria detalhada | Analise de tendencia em dados de telemetria |
| 7 | Low | Dificil de detectar; requer diagnostico especializado | Correlacao cruzada de multiplos sensores |
| 8 | Very low | Detectavel apenas apos manifestacao parcial da falha | Falha percebida apenas quando desempenho cai |
| 9 | Remote | Quase impossivel de detectar em orbita | Falha latente sem sintoma ate evento critico |
| 10 | Absolutely undetectable | Nenhum metodo de deteccao disponivel | Degradacao interna sem telemetria (ex: radiacao acumulada) |

**Referencia:** Adaptado de AIAG FMEA 4th ed. detection scale para contexto orbital.

---

## FORMULA RPN

```
RPN = S x O x D
```

- Range: 1 (minimo) a 1000 (maximo)
- RPN > 400: Alto risco — acao corretiva prioritaria
- RPN 200-400: Risco intermediario — monitoramento e mitigacao
- RPN < 200: Baixo risco — aceitavel com monitoramento padrao

---

## NOTAS DE APLICACAO

1. **Consistencia:** Todos os modos de falha devem ser avaliados usando estas mesmas tabelas
2. **Fontes:** Cada atribuicao deve referenciar a fonte (artigo, standard, ou expert judgment)
3. **Subsistema-dependente:** A mesma falha pode ter S, O, D diferentes dependendo do subsistema
4. **Fase da missao:** O e D podem variar conforme a fase (desenvolvimento vs. orbita)
5. **COTS vs space-grade:** O tende a ser maior para COTS sem screening
