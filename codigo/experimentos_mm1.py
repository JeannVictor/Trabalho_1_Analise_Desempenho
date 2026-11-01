#!/usr/bin/env python3
"""Executa os simuladores em C, salva os CSVs e gera os gráficos."""

import argparse
import csv
import math
import os
import shutil
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "matplotlib-mm1"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from scipy.stats import t as student_t
except ImportError:
    student_t = None


PASTA = Path(__file__).resolve().parent

CENARIOS = [
    ("C1", 0.25, 1.0),
    ("C2", 0.50, 1.0),
    ("C3", 0.75, 1.0),
    ("C4", 0.90, 1.0),
    ("C5", 0.95, 1.0),
    ("C6", 0.99, 1.0),
    ("C7", 1.00, 1.0),
    ("C8", 1.10, 1.0),
]

ESTAVEIS = [cenario for cenario, lamb, mu in CENARIOS if lamb < mu]

METRICAS = [
    "ocupacao", "en", "ew", "erro_little",
    "taxa_chegada", "vazao", "fila_final", "tempo_final",
]

# Medidas que só a V4 calcula.
EXTRAS = ["enq", "ewq", "fila_maxima", "w_direto", "w_p50", "w_p95",
          "little_direto"]

# Experimento de aquecimento (só V4): janela de observação fixa, depois de
# descartar períodos iniciais de tamanhos diferentes.
CENARIOS_AQUECIMENTO = ["C4", "C5", "C6"]
JANELA_AQUECIMENTO = 10_000.0
AQUECIMENTOS = [0.0, 1_000.0, 10_000.0, 100_000.0]
# Com rho = 0,99 e janela curta, as médias por execução variam muito; com
# 30 repetições o IC t não se mostrou estável, por isso aqui são usadas 200.
REPETICOES_AQUECIMENTO = 200

MEDIDAS = [("ocupacao", "Ocupação"), ("en", r"$E[N]$"), ("ew", r"$E[W]$")]

# Figuras citadas no main.tex; são copiadas para artigo/imagem.
FIGURAS_ARTIGO = [
    "teoria_simulacao_v4", "convergencia_v4", "boxplots_en_v4",
    "fluxo_v4", "populacao_final_horizonte_v4", "excesso_horizonte_v3",
    "comparacao_v3_v4", "aquecimento_v4",
]


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("--versao", choices=["v3", "v4", "ambas"], default="ambas")
    parser.add_argument("--repeticoes", type=int, default=30)
    parser.add_argument("--rapido", action="store_true")
    parser.add_argument("--saida", type=Path, default=PASTA / "dados")
    parser.add_argument("--figuras", type=Path, default=PASTA / "dados" / "figuras")
    parser.add_argument("--artigo", type=Path,
                        default=PASTA.parent / "artigo" / "imagem")
    return parser.parse_args()


def compilar(fonte, executavel):
    comando = [
        "gcc", str(fonte), "-O2", "-std=c11", "-Wall", "-Wextra",
        "-lm", "-o", str(executavel),
    ]
    subprocess.run(comando, check=True)


def executar(executavel, lamb, mu, horizonte, semente, aquecimento=None):
    entrada = f"{1.0/lamb}\n{1.0/mu}\n{horizonte}\n{semente}\n"
    if aquecimento is not None:
        entrada += f"{aquecimento}\n"
    processo = subprocess.run(
        [str(executavel)], input=entrada, text=True,
        capture_output=True, check=True,
    )
    valores = {}
    for linha in processo.stdout.splitlines():
        if "=" in linha:
            chave, valor = linha.split("=", 1)
            valores[chave.strip()] = float(valor.strip())
    faltantes = [metrica for metrica in METRICAS if metrica not in valores]
    if faltantes:
        raise RuntimeError(f"Saída incompleta: {', '.join(faltantes)}")
    if "w_direto" in valores and valores["en"] > 0.0:
        # Lei de Little com o W medido cliente a cliente: diferença relativa
        # (%) entre E[N] e lambda * W. Ao contrário de erro_little, não é
        # nula por construção.
        valores["little_direto"] = 100.0 * (
            valores["en"] - valores["taxa_chegada"] * valores["w_direto"]
        ) / valores["en"]
    return valores


def teoria(lamb, mu):
    rho = lamb / mu
    if rho >= 1.0:
        # Sem regime estacionário: o servidor tende a ficar sempre ocupado.
        return {"ocupacao": 1.0, "en": math.nan, "ew": math.nan,
                "enq": math.nan, "ewq": math.nan, "w_direto": math.nan,
                "w_p50": math.nan, "w_p95": math.nan}
    return {
        "ocupacao": rho,
        "en": rho / (1.0 - rho),
        "ew": 1.0 / (mu - lamb),
        "enq": rho * rho / (1.0 - rho),
        "ewq": rho / (mu - lamb),
        # Na M/M/1 FCFS, W é exponencial de taxa mu - lambda.
        "w_direto": 1.0 / (mu - lamb),
        "w_p50": math.log(2.0) / (mu - lamb),
        "w_p95": math.log(20.0) / (mu - lamb),
    }


def intervalo_confianca(valores):
    centro = mean(valores)
    if len(valores) < 2:
        return centro, math.nan, math.nan
    erro_padrao = stdev(valores) / math.sqrt(len(valores))
    critico = student_t.ppf(0.975, len(valores) - 1) if student_t else 1.96
    margem = critico * erro_padrao
    return centro, centro - margem, centro + margem


def salvar_csv(caminho, linhas):
    if not linhas:
        return
    colunas = []
    for linha in linhas:
        for coluna in linha:
            if coluna not in colunas:
                colunas.append(coluna)
    with caminho.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(linhas)


def resumir(resultados, campo="horizonte"):
    grupos = defaultdict(list)
    for resultado in resultados:
        chave = (resultado["versao"], resultado["cenario"], resultado[campo])
        grupos[chave].append(resultado)

    resumo = []
    for (versao, cenario, horizonte), linhas in sorted(grupos.items()):
        lamb = linhas[0]["lambda"]
        mu = linhas[0]["mu"]
        teoricos = teoria(lamb, mu)
        linha = {
            "versao": versao,
            "cenario": cenario,
            "lambda": lamb,
            "mu": mu,
            "rho": lamb / mu,
            campo: horizonte,
            "repeticoes": len(linhas),
        }
        extras = [extra for extra in EXTRAS if extra in linhas[0]]
        for metrica in METRICAS + extras:
            media, inferior, superior = intervalo_confianca(
                [item[metrica] for item in linhas]
            )
            linha[f"{metrica}_media"] = media
            linha[f"{metrica}_ic_inferior"] = inferior
            linha[f"{metrica}_ic_superior"] = superior

            if metrica in teoricos and math.isfinite(teoricos[metrica]):
                esperado = teoricos[metrica]
                linha[f"{metrica}_teorico"] = esperado
                linha[f"{metrica}_erro_relativo"] = (
                    abs(media - esperado) / abs(esperado) * 100.0
                    if esperado != 0.0 else math.nan
                )
        resumo.append(linha)
    return resumo


def barras_erro(linhas, metrica):
    """Distâncias da média até os limites do IC, no formato do errorbar."""
    inferior = [
        linha[f"{metrica}_media"] - linha[f"{metrica}_ic_inferior"]
        for linha in linhas
    ]
    superior = [
        linha[f"{metrica}_ic_superior"] - linha[f"{metrica}_media"]
        for linha in linhas
    ]
    return [inferior, superior]


def maior_horizonte(resumo, versao):
    dados = [linha for linha in resumo if linha["versao"] == versao]
    horizonte = max(linha["horizonte"] for linha in dados)
    return sorted(
        [linha for linha in dados if linha["horizonte"] == horizonte],
        key=lambda linha: linha["rho"],
    )


def salvar_figura(figura, pasta, nome):
    # PDF é vetorial: não perde qualidade quando o LaTeX redimensiona a figura.
    pasta.mkdir(parents=True, exist_ok=True)
    figura.tight_layout()
    figura.savefig(pasta / f"{nome}.pdf", bbox_inches="tight")
    plt.close(figura)


def grafico_teoria(resumo, versao, pasta):
    """E[N] contra rho: curva teórica contínua e médias de dois horizontes."""
    dados = [linha for linha in resumo
             if linha["versao"] == versao and linha["rho"] < 1.0]
    maior = max(linha["horizonte"] for linha in dados)
    fig, eixo = plt.subplots(figsize=(5, 3.8))
    # A curva é calculada numa grade fina; ligar só os seis pontos por
    # retas sugeriria valores falsos entre os cenários.
    grade = [0.2 + i * (0.992 - 0.2) / 400 for i in range(401)]
    eixo.plot(grade, [r / (1.0 - r) for r in grade], color="black",
              label=r"Teoria $\rho/(1-\rho)$")
    for horizonte, marcador in [(maior / 100, "s"), (maior, "o")]:
        linhas = sorted([linha for linha in dados if linha["horizonte"] == horizonte],
                        key=lambda linha: linha["rho"])
        eixo.errorbar([linha["rho"] for linha in linhas],
                      [linha["en_media"] for linha in linhas],
                      yerr=barras_erro(linhas, "en"), fmt=marcador, capsize=3,
                      label=f"Simulação, $T=10^{round(math.log10(horizonte))}$")
    eixo.set_yscale("log")
    eixo.set_xlabel(r"Utilização $\rho$")
    eixo.set_ylabel(r"$E[N]$")
    eixo.grid(alpha=0.25)
    eixo.legend()
    salvar_figura(fig, pasta, f"teoria_simulacao_{versao}")


def grafico_convergencia(resumo, versao, pasta):
    """Médias divididas pelo valor teórico, em função do horizonte."""
    dados = [linha for linha in resumo if linha["versao"] == versao]
    fig, eixos = plt.subplots(2, 1, figsize=(5, 6.5), sharex=True)
    # E[W] fica de fora: o simulador calcula E[W] = E[N] / lambda observado,
    # então sua curva repete a de E[N].
    for eixo, (metrica, titulo) in zip(eixos, MEDIDAS[:2]):
        for cenario in ESTAVEIS:
            linhas = sorted([linha for linha in dados if linha["cenario"] == cenario],
                            key=lambda linha: linha["horizonte"])
            teorico = linhas[0][f"{metrica}_teorico"]
            # Dividir pelo teórico é linear: o IC da razão é o IC da média / teórico.
            eixo.errorbar([linha["horizonte"] for linha in linhas],
                          [linha[f"{metrica}_media"] / teorico for linha in linhas],
                          yerr=[[e / teorico for e in lado]
                                for lado in barras_erro(linhas, metrica)],
                          marker="o", capsize=3, label=cenario)
        eixo.axhline(1.0, linestyle=":", color="black")
        eixo.set_xscale("log")
        eixo.set_xlim(50, 2e6)
        eixo.set_ylabel(f"{titulo} simulado / teórico")
        eixo.grid(alpha=0.25)
    eixos[-1].set_xlabel("Horizonte de simulação $T$")
    eixos[-1].legend(ncol=3, fontsize="small", loc="lower right")
    salvar_figura(fig, pasta, f"convergencia_{versao}")


def grafico_boxplots(resultados, versao, pasta):
    """Dispersão de E[N] entre execuções no maior horizonte."""
    dados = [linha for linha in resultados
             if linha["versao"] == versao and linha["rho"] < 1.0]
    horizonte = max(linha["horizonte"] for linha in dados)
    dados = [linha for linha in dados if linha["horizonte"] == horizonte]
    fig, eixo = plt.subplots(figsize=(5, 3.4))
    # Cada valor é dividido pelo teórico para comparar cenários na mesma escala.
    valores = [
        [linha["en"] / teoria(linha["lambda"], linha["mu"])["en"]
         for linha in dados if linha["cenario"] == cenario]
        for cenario in ESTAVEIS
    ]
    eixo.boxplot(valores, showmeans=True)
    eixo.axhline(1.0, linestyle=":", color="black")
    eixo.set_xticks(range(1, len(ESTAVEIS) + 1), ESTAVEIS)
    eixo.set_ylabel(r"$E[N]$ simulado / teórico")
    eixo.grid(axis="y", alpha=0.25)
    salvar_figura(fig, pasta, f"boxplots_en_{versao}")


def grafico_fluxo(resumo, versao, pasta):
    dados = maior_horizonte(resumo, versao)
    fig, eixo = plt.subplots(figsize=(5, 3.6))
    x = [linha["rho"] for linha in dados]
    for metrica, rotulo, marcador in [
        ("taxa_chegada", "Taxa de chegada observada", "o"),
        ("vazao", "Vazão observada", "s"),
    ]:
        eixo.errorbar(x, [linha[f"{metrica}_media"] for linha in dados],
                      yerr=barras_erro(dados, metrica),
                      fmt=marcador, capsize=4, label=rotulo)
    # Vazão teórica de longo prazo: min(lambda, mu).
    eixo.plot([0.2, 1.0, 1.15], [0.2, 1.0, 1.0], color="black", linewidth=1,
              label=r"Vazão teórica $\min(\lambda,\mu)$")
    eixo.set_xlabel(r"Utilização $\rho$")
    eixo.set_ylabel("Solicitações por unidade de tempo")
    eixo.grid(alpha=0.25)
    eixo.legend()
    salvar_figura(fig, pasta, f"fluxo_{versao}")


def grafico_populacao_horizonte(resumo, versao, pasta):
    """População final de C6 a C8 em função de T, com as previsões teóricas."""
    dados = [linha for linha in resumo if linha["versao"] == versao]
    fig, eixo = plt.subplots(figsize=(5, 3.8))
    referencias = {
        # Estável: N(T) tende à distribuição estacionária, de média rho/(1-rho).
        "C6": lambda t, lamb, mu: (lamb / mu) / (1.0 - lamb / mu),
        # Crítico: N(T) se comporta como |passeio aleatório| de variância 2T.
        "C7": lambda t, lamb, mu: math.sqrt(4.0 * t / math.pi),
        # Sobrecarregado: o excesso de chegadas se acumula linearmente.
        "C8": lambda t, lamb, mu: (lamb - mu) * t,
    }
    for cenario, referencia in referencias.items():
        linhas = sorted([linha for linha in dados if linha["cenario"] == cenario],
                        key=lambda linha: linha["horizonte"])
        x = [linha["horizonte"] for linha in linhas]
        barras = eixo.errorbar(
            x, [linha["fila_final_media"] for linha in linhas],
            yerr=barras_erro(linhas, "fila_final"), marker="o", linestyle="none",
            capsize=3, label=fr"{cenario} ($\rho={linhas[0]['rho']:g}$)",
        )
        cor = barras.lines[0].get_color()
        grade = [10 ** (2 + i * 4 / 100) for i in range(101)]
        lamb, mu = linhas[0]["lambda"], linhas[0]["mu"]
        eixo.plot(grade, [referencia(t, lamb, mu) for t in grade],
                  color=cor, linestyle="--", linewidth=1)
    eixo.set_xscale("log")
    eixo.set_yscale("log")
    eixo.set_xlabel("Horizonte de simulação $T$")
    eixo.set_ylabel(r"População final média $N(T)$")
    eixo.grid(alpha=0.25)
    eixo.legend()
    salvar_figura(fig, pasta, f"populacao_final_horizonte_{versao}")


def grafico_excesso_horizonte(resultados, pasta):
    """Quanto a V3 passa do horizonte, por carga, com a previsão teórica."""
    fig, eixo = plt.subplots(figsize=(5, 3.4))
    x, medias, erros = [], [], []
    for cenario, lamb, mu in CENARIOS:
        # O excesso não depende de T, então todos os horizontes são reunidos.
        excesso = [linha["tempo_final"] - linha["horizonte"] for linha in resultados
                   if linha["versao"] == "v3" and linha["cenario"] == cenario]
        media, inferior, _ = intervalo_confianca(excesso)
        x.append(lamb / mu)
        medias.append(media)
        erros.append(media - inferior)
    eixo.errorbar(x, medias, yerr=erros, fmt="o", capsize=4,
                  label="V3 (média e IC de 95%)")
    # Pela falta de memória, o tempo até o próximo evento depois de T é
    # exponencial de taxa lambda (servidor ocioso) ou lambda + mu (ocupado).
    grade = [0.2 + i * (1.15 - 0.2) / 200 for i in range(201)]
    eixo.plot(grade, [(1 - min(r, 1)) / r + min(r, 1) / (r + 1) for r in grade],
              color="black", linewidth=1,
              label=r"Teoria $(1-\rho)/\lambda + \rho/(\lambda+\mu)$")
    eixo.set_xlabel(r"Utilização $\rho$")
    eixo.set_ylabel(r"Tempo final $-$ $T$")
    eixo.grid(alpha=0.25)
    eixo.legend()
    salvar_figura(fig, pasta, "excesso_horizonte_v3")


def grafico_comparacao(resultados, pasta):
    indices = defaultdict(dict)
    for linha in resultados:
        chave = (linha["cenario"], linha["horizonte"], linha["repeticao"])
        indices[chave][linha["versao"]] = linha

    # Ocupação em diferença absoluta (mesma escala em todos os cenários);
    # E[N] em diferença relativa, porque varia de 0,33 a 99 entre cenários.
    paineis = [
        ("ocupacao", "V3 $-$ V4: ocupação", lambda v3, v4: v3 - v4),
        ("en", r"V3 $-$ V4: $E[N]$ (%)", lambda v3, v4: 100.0 * (v3 - v4) / v4),
    ]
    fig, eixos = plt.subplots(2, 1, figsize=(5, 6.5), sharex=True)
    for eixo, (metrica, titulo, diferenca) in zip(eixos, paineis):
        for cenario in ESTAVEIS:
            horizontes = sorted({chave[1] for chave in indices if chave[0] == cenario})
            medias = []
            inferiores = []
            superiores = []
            for horizonte in horizontes:
                diferencas = [
                    diferenca(pares["v3"][metrica], pares["v4"][metrica])
                    for chave, pares in indices.items()
                    if chave[0] == cenario and chave[1] == horizonte
                    and pares["v4"][metrica] != 0.0
                ]
                media, inferior, superior = intervalo_confianca(diferencas)
                medias.append(media)
                inferiores.append(media - inferior)
                superiores.append(superior - media)
            eixo.errorbar(horizontes, medias, yerr=[inferiores, superiores],
                          marker="o", capsize=3, label=cenario)
        eixo.axhline(0.0, linestyle=":", color="black")
        eixo.set_xscale("log")
        eixo.set_xlim(50, 2e6)
        eixo.set_ylabel(titulo)
        eixo.grid(alpha=0.25)
    eixos[-1].set_xlabel("Horizonte de simulação $T$")
    eixos[0].legend(ncol=3, fontsize="small")
    salvar_figura(fig, pasta, "comparacao_v3_v4")


def grafico_aquecimento(resumo, pasta):
    """E[N]/teórico numa janela fixa, para cada período de aquecimento."""
    fig, eixo = plt.subplots(figsize=(5, 3.6))
    posicoes = range(len(AQUECIMENTOS))
    for cenario in CENARIOS_AQUECIMENTO:
        linhas = sorted([linha for linha in resumo if linha["cenario"] == cenario],
                        key=lambda linha: linha["aquecimento"])
        teorico = linhas[0]["en_teorico"]
        eixo.errorbar(posicoes, [linha["en_media"] / teorico for linha in linhas],
                      yerr=[[e / teorico for e in lado]
                            for lado in barras_erro(linhas, "en")],
                      marker="o", capsize=3,
                      label=fr"{cenario} ($\rho={linhas[0]['rho']:g}$)")
    eixo.axhline(1.0, linestyle=":", color="black")
    # O eixo é categórico porque o aquecimento zero não cabe em escala log.
    eixo.set_xticks(list(posicoes),
                    ["0"] + [f"$10^{round(math.log10(a))}$" for a in AQUECIMENTOS[1:]])
    eixo.set_xlabel(f"Aquecimento descartado (s); janela de $10^{round(math.log10(JANELA_AQUECIMENTO))}$ s")
    eixo.set_ylabel(r"$E[N]$ simulado / teórico")
    eixo.grid(alpha=0.25)
    eixo.legend(fontsize="small")
    salvar_figura(fig, pasta, "aquecimento_v4")


def salvar_tabela_little(resultados, caminho):
    grupos = defaultdict(list)
    for linha in resultados:
        chave = (linha["versao"], linha["cenario"], linha["horizonte"])
        grupos[chave].append(abs(linha["erro_little"]))
    linhas = []
    for (versao, cenario, horizonte), valores in sorted(grupos.items()):
        linhas.append({
            "versao": versao,
            "cenario": cenario,
            "horizonte": horizonte,
            "erro_absoluto_medio": mean(valores),
            "maior_erro_absoluto": max(valores),
        })
    salvar_csv(caminho, linhas)


def experimento_aquecimento(fonte, repeticoes):
    resultados = []
    with tempfile.TemporaryDirectory() as pasta_binarios:
        executavel = Path(pasta_binarios) / "simulacao_v4"
        compilar(fonte, executavel)
        for cenario, lamb, mu in CENARIOS:
            if cenario not in CENARIOS_AQUECIMENTO:
                continue
            indice_cenario = CENARIOS_AQUECIMENTO.index(cenario)
            for indice, aquecimento in enumerate(AQUECIMENTOS):
                for repeticao in range(1, repeticoes + 1):
                    # Faixa de sementes separada da do experimento principal.
                    semente = 20_000_000 + indice_cenario * 100_000 \
                        + indice * 1_000 + repeticao
                    valores = executar(executavel, lamb, mu,
                                       aquecimento + JANELA_AQUECIMENTO,
                                       semente, aquecimento)
                    resultados.append({
                        "versao": "v4",
                        "cenario": cenario,
                        "lambda": lamb,
                        "mu": mu,
                        "rho": lamb / mu,
                        "aquecimento": aquecimento,
                        "repeticao": repeticao,
                        "semente": semente,
                        **valores,
                    })
    return resultados


def main():
    args = argumentos()
    args.saida.mkdir(parents=True, exist_ok=True)
    horizontes = [100.0, 1_000.0, 10_000.0] if args.rapido else [
        100.0, 1_000.0, 10_000.0, 100_000.0, 1_000_000.0,
    ]
    repeticoes = 5 if args.rapido else args.repeticoes
    versoes = ["v3", "v4"] if args.versao == "ambas" else [args.versao]
    fontes = {
        "v3": PASTA / "simulacao_v3_testes.c",
        "v4": PASTA / "simulacao_v4.c",
    }

    resultados = []
    total = len(versoes) * len(CENARIOS) * len(horizontes) * repeticoes
    contador = 0

    with tempfile.TemporaryDirectory() as pasta_binarios:
        for versao in versoes:
            executavel = Path(pasta_binarios) / f"simulacao_{versao}"
            compilar(fontes[versao], executavel)
            for indice_cenario, (cenario, lamb, mu) in enumerate(CENARIOS):
                for indice_horizonte, horizonte in enumerate(horizontes):
                    for repeticao in range(1, repeticoes + 1):
                        semente = 10_000_000 + indice_cenario * 100_000 \
                            + indice_horizonte * 1_000 + repeticao
                        valores = executar(executavel, lamb, mu, horizonte, semente)
                        resultados.append({
                            "versao": versao,
                            "cenario": cenario,
                            "lambda": lamb,
                            "mu": mu,
                            "rho": lamb / mu,
                            "horizonte": horizonte,
                            "repeticao": repeticao,
                            "semente": semente,
                            **valores,
                        })
                        contador += 1
                        if contador % 50 == 0 or contador == total:
                            print(f"{contador}/{total}")

    resumo = resumir(resultados)
    nome = args.versao
    salvar_csv(args.saida / f"resultados_{nome}.csv", resultados)
    salvar_csv(args.saida / f"resumo_{nome}.csv", resumo)
    salvar_tabela_little(resultados, args.saida / f"little_{nome}.csv")

    for versao in versoes:
        grafico_teoria(resumo, versao, args.figuras)
        grafico_convergencia(resumo, versao, args.figuras)
        grafico_boxplots(resultados, versao, args.figuras)
        grafico_fluxo(resumo, versao, args.figuras)
        grafico_populacao_horizonte(resumo, versao, args.figuras)
    if "v3" in versoes:
        grafico_excesso_horizonte(resultados, args.figuras)
    if "v4" in versoes:
        aquecimento = experimento_aquecimento(
            fontes["v4"], 20 if args.rapido else REPETICOES_AQUECIMENTO)
        resumo_aquecimento = resumir(aquecimento, campo="aquecimento")
        salvar_csv(args.saida / "aquecimento_v4.csv", aquecimento)
        salvar_csv(args.saida / "resumo_aquecimento_v4.csv", resumo_aquecimento)
        grafico_aquecimento(resumo_aquecimento, args.figuras)
    if len(versoes) == 2:
        grafico_comparacao(resultados, args.figuras)

        # O artigo usa a V4 (corrigida) e as duas figuras que mostram a V3.
        args.artigo.mkdir(parents=True, exist_ok=True)
        for nome in FIGURAS_ARTIGO:
            shutil.copy(args.figuras / f"{nome}.pdf", args.artigo / f"{nome}.pdf")


if __name__ == "__main__":
    main()
