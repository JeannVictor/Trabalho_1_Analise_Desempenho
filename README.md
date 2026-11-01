# Trabalho de Análise de Desempenho — Fila M/M/1

Autores: Jeann Victor Batista e Thallysson Luis Teixeira Carvalho  
Disciplina: Análise de Desempenho — UNIFAL-MG  
Professor: Flávio Barbieri Gonzaga

---

## Arquivos do repositório

| Arquivo | Descrição |
|:---|:---|
| [`artigo/artigo.pdf`](./artigo/artigo.pdf) | Artigo compilado, pronto para leitura |
| [`artigo/main.tex`](./artigo/main.tex) | Fonte do artigo em LaTeX |
| [`artigo/imagem/`](./artigo/imagem/) | Cópia das 7 figuras (PDF) usadas no `main.tex` |
| [`codigo/simulacao_v3.c`](./codigo/simulacao_v3.c) | Simulador original fornecido em sala |
| [`codigo/simulacao_v3_testes.c`](./codigo/simulacao_v3_testes.c) | V3 com semente por parâmetro e saída em formato simples |
| [`codigo/simulacao_v4.c`](./codigo/simulacao_v4.c) | V4: encerra em T, valida entradas, corrige ocupação; mede E[Nq], E[Wq], fila máxima e o tempo de cada cliente (média, P50, P95); aquecimento opcional |
| [`codigo/experimentos_mm1.py`](./codigo/experimentos_mm1.py) | Compila, executa, agrega e plota os resultados |
| [`codigo/dados/resultados_ambas.csv`](./codigo/dados/resultados_ambas.csv) | Uma linha por execução individual |
| [`codigo/dados/resumo_ambas.csv`](./codigo/dados/resumo_ambas.csv) | Médias e intervalos de confiança por configuração |
| [`codigo/dados/little_ambas.csv`](./codigo/dados/little_ambas.csv) | Resíduo da Lei de Little por configuração |
| [`codigo/dados/aquecimento_v4.csv`](./codigo/dados/aquecimento_v4.csv) | Experimento de aquecimento (V4), uma linha por execução |
| [`codigo/dados/resumo_aquecimento_v4.csv`](./codigo/dados/resumo_aquecimento_v4.csv) | Médias e ICs do experimento de aquecimento |
| [`codigo/dados/figuras/`](./codigo/dados/figuras/) | Todas as figuras geradas (V3 e V4), inclusive as que não entram no artigo |

---

## Estrutura de pastas

```
trabalho_1/
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
        ├── aquecimento_v4.csv
        ├── resumo_aquecimento_v4.csv
        └── figuras/          ← todas as figuras geradas pelo script
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
python3 experimentos_mm1.py
```

Isso vai:

1. Compilar `simulacao_v3_testes.c` e `simulacao_v4.c`
2. Rodar 8 cenários (ρ de 0,25 a 1,10, incluindo 0,99) × 5 horizontes (10² a 10⁶) × 30 repetições em cada versão
3. Rodar o experimento de aquecimento da V4 (C4 a C6, janela de 10⁴ s, aquecimentos de 0 a 10⁵ s, 200 repetições)
4. Salvar os CSVs em `codigo/dados/`
5. Salvar todas as figuras (PDF) em `codigo/dados/figuras/` e copiar as usadas no artigo para `artigo/imagem/`

### Outras opções do script

```bash
# Rodar apenas a versão original
python3 experimentos_mm1.py --versao v3

# Rodar apenas a versão corrigida
python3 experimentos_mm1.py --versao v4

# Teste rápido (5 repetições, só horizontes menores)
python3 experimentos_mm1.py --versao ambas --rapido
```

As figuras do artigo pressupõem `--versao ambas` (o padrão): com uma versão só,
a comparação V3 × V4 não é gerada (e, sem a V3, nem o excesso de horizonte).

---

## Como rodar um simulador isolado

Cada simulador lê quatro valores de `stdin` (a V4 aceita um quinto, opcional), um por linha:

1. Tempo médio entre chegadas
2. Tempo médio de atendimento
3. Tempo total de simulação
4. Semente aleatória
5. (só V4, opcional) Tempo de aquecimento descartado antes da coleta — padrão 0

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
enq=0.083...
ewq=0.333...
fila_maxima=...
w_direto=1.333...
w_p50=0.92...
w_p95=3.99...
```

As seis últimas linhas só aparecem na V4.

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
| `enq` | E[Nq] — número médio na fila de espera (só V4) |
| `ewq` | E[Wq] — tempo médio de espera antes do atendimento (só V4) |
| `fila_maxima` | maior população observada na janela (só V4) |
| `w_direto` | média do tempo no sistema medido cliente a cliente (só V4) |
| `w_p50`, `w_p95` | mediana e percentil 95 desse tempo (só V4) |

---

## Como compilar o artigo

O artigo está em `artigo/main.tex`. Duas opções:

### Opção 1 — Overleaf (mais simples)

1. Faça upload de `artigo/main.tex` e da pasta `artigo/imagem/`
2. Compile direto no Overleaf

### Opção 2 — Local (com TeX Live instalado)

O artigo usa a classe `abntex2` (modelo de artigo ABNT NBR 6022:2018, em duas colunas).

```bash
cd artigo
pdflatex -jobname=artigo main.tex
pdflatex -jobname=artigo main.tex   # segunda passada para referências
```

O PDF final é gerado em `artigo/artigo.pdf`.

---