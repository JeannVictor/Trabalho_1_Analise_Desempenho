# Trabalho de Análise de Desempenho — Fila M/M/1

Autor: Jeann Victor Batista  
Disciplina: Análise de Desempenho — UNIFAL-MG  
Professor: Flávio Barbieri Gonzaga

---

## Arquivos do repositório

| Arquivo | Descrição |
|:---|:---|
| [`artigo/artigo.pdf`](./artigo/artigo.pdf) | Artigo compilado, pronto para leitura |
| [`artigo/main.tex`](./artigo/main.tex) | Fonte do artigo em LaTeX |
| [`artigo/imagem/`](./artigo/imagem/) | Figuras referenciadas pelo `main.tex` |
| [`codigo/simulacao_v3.c`](./codigo/simulacao_v3.c) | Simulador original fornecido em sala |
| [`codigo/simulacao_v3_testes.c`](./codigo/simulacao_v3_testes.c) | V3 com semente por parâmetro e saída em formato simples |
| [`codigo/simulacao_v4.c`](./codigo/simulacao_v4.c) | V4: encerra em T, valida entradas, corrige ocupação |
| [`codigo/experimentos_mm1.py`](./codigo/experimentos_mm1.py) | Compila, executa, agrega e plota os resultados |
| [`codigo/dados/resultados_ambas.csv`](./codigo/dados/resultados_ambas.csv) | Uma linha por execução individual |
| [`codigo/dados/resumo_ambas.csv`](./codigo/dados/resumo_ambas.csv) | Médias e intervalos de confiança por configuração |
| [`codigo/dados/little_ambas.csv`](./codigo/dados/little_ambas.csv) | Resíduo da Lei de Little por execução |
| [`codigo/dados/figuras/`](./codigo/dados/figuras/) | Figuras geradas pelo script |

---

## Estrutura de pastas

```
trabalho_1_ad/
├── artigo/
│   ├── artigo.pdf            ← PDF final
│   ├── main.tex              ← fonte LaTeX
│   └── imagem/               ← figuras usadas no .tex
└── codigo/
    ├── experimentos_mm1.py   ← script Python de automação
    ├── simulacao_v3.c        ← V3 original
    ├── simulacao_v3_testes.c ← V3 adaptada para o Python
    ├── simulacao_v4.c        ← V4 corrigida
    └── dados/
        ├── resultados_ambas.csv
        ├── resumo_ambas.csv
        ├── little_ambas.csv
        └── figuras/          ← figuras geradas pelo script
```

---

## Como rodar os experimentos

### Pré-requisitos

- **GCC** (para compilar os arquivos `.c`)
- **Python 3** com `matplotlib`, `numpy` e `scipy`

Instalar as dependências Python:

```bash
pip install matplotlib numpy scipy
```

### Executar

O script `experimentos_mm1.py` compila os simuladores automaticamente
e roda todas as combinações de cenário, horizonte e repetição.

A partir da **raiz do repositório**:

```bash
cd codigo
python3 experimentos_mm1.py --versao ambas --repeticoes 30 --saida dados
```

Isso vai:

1. Compilar `simulacao_v3_testes.c` e `simulacao_v4.c`
2. Rodar 7 cenários × 4 horizontes × 30 repetições em cada versão
3. Salvar os CSVs em `codigo/dados/`
4. Salvar as figuras em `codigo/dados/figuras/`

### Outras opções do script

```bash
# Rodar apenas a versão original
python3 experimentos_mm1.py --versao v3 --repeticoes 30 --saida dados

# Rodar apenas a versão corrigida
python3 experimentos_mm1.py --versao v4 --repeticoes 30 --saida dados

# Teste rápido (5 repetições, só horizontes menores)
python3 experimentos_mm1.py --versao ambas --rapido --saida dados
```

---

## Como rodar um simulador isolado

Cada simulador lê quatro valores de `stdin`, um por linha:

1. Tempo médio entre chegadas
2. Tempo médio de atendimento
3. Tempo total de simulação
4. Semente aleatória

### Compilar

```bash
cd codigo
gcc -O2 -std=c11 -Wall -Wextra simulacao_v4.c -o simulacao_v4 -lm
```

Observação: a flag `-lm` precisa vir **depois** do arquivo `.c` e do `-o`,
caso contrário o linker não encontra a função `log` da biblioteca matemática.

### Executar

```bash
echo "4.0 1.0 100.0 42" | ./simulacao_v4
```

### Saída esperada

```
ocupacao=0.250...
en=0.333...
ew=1.333...
erro_little=0.000...
taxa_chegada=0.250...
vazao=0.250...
fila_final=0
tempo_final=100.000...
```

### Significado dos campos

| Campo | Significado |
|:---|:---|
| `ocupacao` | fração do tempo com o servidor ocupado |
| `en` | E[N] — número médio de clientes no sistema |
| `ew` | E[W] — tempo médio de permanência |
| `erro_little` | resíduo E[N] − λ·E[W] |
| `taxa_chegada` | chegadas observadas por unidade de tempo |
| `vazao` | saídas observadas por unidade de tempo |
| `fila_final` | população no instante final |
| `tempo_final` | tempo efetivamente simulado |

---

## Como compilar o artigo

O artigo está em `artigo/main.tex`. Duas opções:

### Opção 1 — Overleaf (mais simples)

1. Faça upload de `artigo/main.tex` e da pasta `artigo/imagem/`
2. Compile direto no Overleaf

### Opção 2 — Local (com TeX Live instalado)

```bash
cd artigo
pdflatex main.tex
pdflatex main.tex   # segunda passada para referências
```

O PDF final é gerado em `artigo/artigo.pdf`.

---