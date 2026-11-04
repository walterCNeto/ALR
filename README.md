# ALR - O custo fiscal da politica monetaria no Brasil

Avaliacao empirica dos argumentos de Andre Lara Resende (ALR) sobre o custo
fiscal da politica monetaria brasileira, com calibracao 2003-2026 e simulacao
contrafactual da proposta de setembro de 2026 (Eu Acuso).

**Autor:** Walter C. Neto
**Formacao:** Engenheiro Fisico (UFSCar), Mestre em Economia com enfase em
Engenharia Financeira (FGV-EESP).
**Publicacao:** novembro de 2026.

---

## O que este repositorio contem

Sete blocos empiricos integrados em um paper unico:

1. **Aritmetica fiscal** da divida publica (2017 vs 2026).
2. **Estimacoes estruturais** - curvas IS, Phillips NK hibrida e regra de Taylor.
3. **Fisher de longo prazo** - testes de cointegracao pi-i.
4. **Neutralidade da moeda** - VAR/VECM pi-i com IRF e decomposicao de variancia.
5. **Pass-through cambial** - regressao com defasagens e VAR trivariado.
6. **Posicionamento estrutural** do Brasil contra 31 paises (World Bank + literatura).
7. **Simulacao contrafactual** da proposta ALR (set/2026) no modelo calibrado.

Alem disso, uma secao propositiva de **salvaguardas em cenario desfavoravel**
com seis medidas concretas de protecao caso a proposta seja adotada.

## Principais achados

- A aritmetica fiscal apontada por ALR em 2017 se confirmou e se agravou:
  superavit primario estabilizador subiu de 5,1% para 7,1% do PIB.
- A curva de Phillips brasileira e empiricamente plana (kappa = 0,040,
  nao-significativo), corroborando a tese fraca de ALR.
- Fisher de longo prazo e parcialmente sustentado: ha cointegracao pi~i,
  mas a hipotese beta=1 (Fisher puro) e rejeitada com p < 0,001.
- A proposta ALR simulada no modelo calibrado entrega 44 p.p. de ganho
  fiscal em 5 anos sem descontrole inflacionario, desde que a
  reancoragem institucional funcione.
- O Brasil esta em um conjunto raro de emergentes onde a arquitetura
  institucional permite testar a proposta (divida 95% em moeda local,
  CBI 0,70, reservas 15% do PIB).

## Estrutura do repositorio

```
ALR/
|-- paper/                          Paper em LaTeX e PDF compilado
|   |-- main.tex
|   |-- main.pdf
|   +-- figs/                       Figuras do paper
|-- notebooks/                      Analise reprodutivel, um por bloco
|   |-- simulador_politica_monetaria.ipynb
|   |-- passo_1_1_fisher.ipynb
|   |-- passo_1_2_neutralidade.ipynb
|   |-- passo_1_3_cambio.ipynb
|   |-- bloco_2_simulacao_ALR.ipynb
|   |-- macro_sobre_macro.ipynb
|   +-- notebook_consolidado_final.ipynb
|-- scripts/
|   +-- gerar_figs_faltantes.py
|-- cache_dados/                    CSVs do BACEN/SGS (cache local)
|-- figs/                           Todas as figuras geradas
|-- LICENSE
+-- README.md
```

## Como reproduzir

### Pre-requisitos

```bash
pip install "numpy<2" pandas matplotlib statsmodels scipy jupyter requests
```

### Rodar a analise

```bash
cd notebooks/
jupyter notebook notebook_consolidado_final.ipynb
```

O notebook consolidado executa toda a cadeia de analise em um unico fluxo
e gera o dashboard de sintese, a tabela LaTeX para o paper e a conclusao
consolidada.

### Compilar o paper

```bash
cd paper/
pdflatex main.tex
pdflatex main.tex
```

## Fontes de dados

- **BACEN/SGS** - Selic, IPCA cheio e livres, PTAX, IBC-Br, divida bruta,
  resultados fiscais.
- **BACEN/Olinda** - expectativas Focus de IPCA, Selic, PIB, cambio.
- **IBGE/SIDRA** - PIB trimestral encadeado dessazonalizado.
- **World Bank WDI** - indicadores comparativos de 31 paises.
- **Literatura consolidada** - ECI (Atlas Harvard), CBI (Dincer-Eichengreen),
  divida em moeda local (BIS, Du-Schreger).

## Licencas

- Codigo: MIT License
- Texto do paper e figuras: CC BY 4.0

## Referencias principais

- Cochrane, J. H. (2023). *The Fiscal Theory of the Price Level*. Princeton.
- Gali, J. (2015). *Monetary policy, inflation, and the business cycle*. 2a ed.
- Lara Resende, A. (2017). Juros e conservadorismo intelectual. *Valor Economico*.
- Lara Resende, A. (2026). Eu Acuso: uma proposta para eliminar os juros absurdos.
  *Substack "Um Cetico Esperancoso"*, 25 de setembro de 2026.
- Minella, A. et al. (2003). Inflation targeting in Brazil. *JIMF*, 22(7).

Lista completa na bibliografia do paper.

## Contato

- Portfolio: [waltercneto.github.io](https://waltercneto.github.io)
- Email: walter.correa.neto@gmail.com
- LinkedIn: [waltercorreaneto](https://www.linkedin.com/in/waltercorreaneto/)

## Nota sobre metodos e ferramentas

Este trabalho foi concebido, conduzido e redigido por mim. No processo,
utilizei um assistente de inteligencia artificial (Claude, da Anthropic)
como ferramenta de apoio para acelerar a escrita do codigo de coleta e
tratamento de dados, depurar a integracao entre bibliotecas econometricas,
discutir escolhas de especificacao e formatacao do documento em LaTeX.
Todas as decisoes de modelagem, a interpretacao dos resultados e a
responsabilidade pelo conteudo sao exclusivamente minhas.
