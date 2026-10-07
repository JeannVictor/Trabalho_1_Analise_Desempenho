#!/usr/bin/env python3
"""Executa os simuladores em C, salva CSV e gera gráficos."""

import argparse
import csv
import math
import os
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
    ("C6", 1.00, 1.0),
    ("C7", 1.10, 1.0),
]

METRICAS = [
    "ocupacao", "en", "ew", "erro_little",
    "taxa_chegada", "vazao", "fila_final", "tempo_final",
]


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("--versao", choices=["v3", "v4", "ambas"], default="v3")
    parser.add_argument("--repeticoes", type=int, default=30)
    parser.add_argument("--rapido", action="store_true")
    parser.add_argument("--saida", type=Path, default=PASTA / "resultados")
    return parser.parse_args()


def compilar(fonte, executavel):
    comando = [
        "gcc", str(fonte), "-O2", "-std=c11", "-Wall", "-Wextra",
        "-lm", "-o", str(executavel),
    ]
    subprocess.run(comando, check=True)


def executar(executavel, lamb, mu, horizonte, semente):
    entrada = f"{1.0/lamb}\n{1.0/mu}\n{horizonte}\n{semente}\n"
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
    return valores


def teoria(lamb, mu):
    rho = lamb / mu
    if rho >= 1.0:
        return {"ocupacao": rho, "en": math.nan, "ew": math.nan}
    return {
        "ocupacao": rho,
        "en": rho / (1.0 - rho),
        "ew": 1.0 / (mu - lamb),
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


def resumir(resultados):
    grupos = defaultdict(list)
    for resultado in resultados:
        chave = (resultado["versao"], resultado["cenario"], resultado["horizonte"])
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
            "horizonte": horizonte,
            "repeticoes": len(linhas),
        }
        for metrica in METRICAS:
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


def salvar_figura(figura, pasta, nome):
    pasta.mkdir(parents=True, exist_ok=True)
    figura.savefig(pasta / f"{nome}.png", dpi=200, bbox_inches="tight")
    figura.savefig(pasta / f"{nome}.pdf", bbox_inches="tight")
    plt.close(figura)


def grafico_convergencia(resumo, versao, pasta):
    dados = [linha for linha in resumo if linha["versao"] == versao and linha["rho"] < 1.0]
    fig, eixos = plt.subplots(1, 3, figsize=(15, 4.8))
    configuracoes = [
        ("ocupacao", "Ocupação"),
        ("en", r"$E[N]$"),
        ("ew", r"$E[W]$"),
    ]
    for cenario, _, _ in CENARIOS[:5]:
        linhas = sorted(
            [linha for linha in dados if linha["cenario"] == cenario],
            key=lambda linha: linha["horizonte"],
        )
        for eixo, (metrica, titulo) in zip(eixos, configuracoes):
            x = [linha["horizonte"] for linha in linhas]
            y = [linha[f"{metrica}_media"] for linha in linhas]
            erro_inferior = [
                linha[f"{metrica}_media"] - linha[f"{metrica}_ic_inferior"]
                for linha in linhas
            ]
            erro_superior = [
                linha[f"{metrica}_ic_superior"] - linha[f"{metrica}_media"]
                for linha in linhas
            ]
            barras = eixo.errorbar(
                x, y, yerr=[erro_inferior, erro_superior],
                marker="o", capsize=3, label=cenario,
            )
            cor = barras.lines[0].get_color()
            eixo.axhline(linhas[0][f"{metrica}_teorico"], color=cor,
                         linestyle=":", alpha=0.45)
            eixo.set_xscale("log")
            eixo.set_xlabel("Tempo de simulação")
            eixo.set_ylabel(titulo)
            eixo.grid(alpha=0.25)
    eixos[0].legend()
    fig.suptitle(f"Convergência — {versao.upper()}")
    fig.tight_layout()
    salvar_figura(fig, pasta, f"convergencia_{versao}")


def grafico_teoria(resumo, versao, pasta):
    dados = [linha for linha in resumo if linha["versao"] == versao and linha["rho"] < 1.0]
    maior_horizonte = max(linha["horizonte"] for linha in dados)
    dados = sorted(
        [linha for linha in dados if linha["horizonte"] == maior_horizonte],
        key=lambda linha: linha["rho"],
    )
    fig, eixos = plt.subplots(1, 3, figsize=(15, 4.8))
    for eixo, (metrica, titulo) in zip(
        eixos, [("ocupacao", "Ocupação"), ("en", r"$E[N]$"), ("ew", r"$E[W]$")]
    ):
        x = [linha["rho"] for linha in dados]
        y = [linha[f"{metrica}_media"] for linha in dados]
        erro_inferior = [
            linha[f"{metrica}_media"] - linha[f"{metrica}_ic_inferior"] for linha in dados
        ]
        erro_superior = [
            linha[f"{metrica}_ic_superior"] - linha[f"{metrica}_media"] for linha in dados
        ]
        eixo.errorbar(x, y, yerr=[erro_inferior, erro_superior],
                      fmt="o", capsize=4, label="Simulação")
        eixo.plot(x, [linha[f"{metrica}_teorico"] for linha in dados],
                  "s-", color="black", label="Teoria")
        eixo.set_xlabel(r"Utilização $\rho$")
        eixo.set_ylabel(titulo)
        eixo.grid(alpha=0.25)
    eixos[0].legend()
    fig.suptitle(f"Teoria e simulação — {versao.upper()} — T={maior_horizonte:g}")
    fig.tight_layout()
    salvar_figura(fig, pasta, f"teoria_simulacao_{versao}")


def grafico_erros(resumo, versao, pasta):
    dados = [linha for linha in resumo if linha["versao"] == versao and linha["rho"] < 1.0]
    maior_horizonte = max(linha["horizonte"] for linha in dados)
    dados = sorted(
        [linha for linha in dados if linha["horizonte"] == maior_horizonte],
        key=lambda linha: linha["rho"],
    )
    fig, eixo = plt.subplots(figsize=(9, 5))
    for metrica, rotulo in [("ocupacao", "Ocupação"), ("en", "E[N]"), ("ew", "E[W]")]:
        eixo.plot(
            [linha["rho"] for linha in dados],
            [linha[f"{metrica}_erro_relativo"] for linha in dados],
            marker="o", label=rotulo,
        )
    eixo.set_xlabel(r"Utilização $\rho$")
    eixo.set_ylabel("Erro relativo (%)")
    eixo.grid(alpha=0.25)
    eixo.legend()
    fig.tight_layout()
    salvar_figura(fig, pasta, f"erros_relativos_{versao}")


def grafico_fluxo(resumo, versao, pasta):
    dados = [linha for linha in resumo if linha["versao"] == versao]
    if not dados:
        return
    maior_horizonte = max(linha["horizonte"] for linha in dados)
    dados = sorted(
        [linha for linha in dados if linha["horizonte"] == maior_horizonte],
        key=lambda linha: linha["rho"],
    )
    fig, eixo = plt.subplots(figsize=(9, 5))
    x = [linha["rho"] for linha in dados]
    for metrica, rotulo in [
        ("taxa_chegada", "Taxa de chegada observada"),
        ("vazao", "Vazão observada"),
    ]:
        y = [linha[f"{metrica}_media"] for linha in dados]
        inferior = [
            linha[f"{metrica}_media"] - linha[f"{metrica}_ic_inferior"]
            for linha in dados
        ]
        superior = [
            linha[f"{metrica}_ic_superior"] - linha[f"{metrica}_media"]
            for linha in dados
        ]
        eixo.errorbar(
            x, y, yerr=[inferior, superior], marker="o", capsize=4,
            label=rotulo,
        )
    eixo.plot(x, [linha["lambda"] for linha in dados], "--", color="gray",
              label=r"Taxa configurada $\lambda$")
    eixo.axhline(1.0, linestyle=":", color="black", label=r"Capacidade $\mu=1$")
    eixo.set_xlabel(r"Utilização $\rho$")
    eixo.set_ylabel("Requisições por unidade de tempo")
    eixo.grid(alpha=0.25)
    eixo.legend()
    fig.suptitle(f"Chegadas e vazão — {versao.upper()} — T={maior_horizonte:g}")
    fig.tight_layout()
    salvar_figura(fig, pasta, f"fluxo_{versao}")


def grafico_excesso_horizonte(resumo, versao, pasta):
    dados = [linha for linha in resumo if linha["versao"] == versao]
    if not dados:
        return
    fig, eixo = plt.subplots(figsize=(9, 5))
    for cenario, _, _ in CENARIOS:
        linhas = sorted(
            [linha for linha in dados if linha["cenario"] == cenario],
            key=lambda linha: linha["horizonte"],
        )
        x = [linha["horizonte"] for linha in linhas]
        y = [linha["tempo_final_media"] - linha["horizonte"] for linha in linhas]
        inferior = [
            min(
                linha["tempo_final_media"] - linha["tempo_final_ic_inferior"],
                linha["tempo_final_media"] - linha["horizonte"],
            ) for linha in linhas
        ]
        superior = [
            linha["tempo_final_ic_superior"] - linha["tempo_final_media"]
            for linha in linhas
        ]
        eixo.errorbar(x, y, yerr=[inferior, superior], marker="o",
                      capsize=3, label=cenario)
    eixo.set_xscale("log")
    eixo.set_xlabel("Horizonte solicitado")
    eixo.set_ylabel("Tempo efetivo − horizonte")
    eixo.grid(alpha=0.25)
    eixo.legend()
    fig.suptitle(f"Ultrapassagem do horizonte — {versao.upper()}")
    fig.tight_layout()
    salvar_figura(fig, pasta, f"excesso_horizonte_{versao}")


def grafico_populacao_rho(resumo, versao, pasta):
    dados = [linha for linha in resumo if linha["versao"] == versao]
    if not dados:
        return
    fig, eixo = plt.subplots(figsize=(9, 5))
    for horizonte in sorted({linha["horizonte"] for linha in dados}):
        linhas = sorted(
            [linha for linha in dados if linha["horizonte"] == horizonte],
            key=lambda linha: linha["rho"],
        )
        x = [linha["rho"] for linha in linhas]
        y = [linha["fila_final_media"] for linha in linhas]
        inferior = [
            min(
                linha["fila_final_media"] - linha["fila_final_ic_inferior"],
                max(linha["fila_final_media"] - 1e-3, 0.0),
            ) for linha in linhas
        ]
        superior = [
            linha["fila_final_ic_superior"] - linha["fila_final_media"]
            for linha in linhas
        ]
        eixo.errorbar(x, y, yerr=[inferior, superior], marker="o",
                      capsize=3, label=f"T={horizonte:g}")
    eixo.axvline(1.0, linestyle=":", color="black", label=r"$\rho=1$")
    eixo.set_yscale("log")
    eixo.set_xlabel(r"Utilização $\rho$")
    eixo.set_ylabel("População final média")
    eixo.grid(alpha=0.25)
    eixo.legend()
    fig.suptitle(f"População final em função da carga — {versao.upper()}")
    fig.tight_layout()
    salvar_figura(fig, pasta, f"populacao_final_rho_{versao}")


def grafico_comparacao(resultados, pasta):
    versoes = {linha["versao"] for linha in resultados}
    if versoes != {"v3", "v4"}:
        return
    indices = defaultdict(dict)
    for linha in resultados:
        chave = (linha["cenario"], linha["horizonte"], linha["repeticao"])
        indices[chave][linha["versao"]] = linha

    fig, eixos = plt.subplots(1, 3, figsize=(15, 4.8))
    for eixo, (metrica, titulo) in zip(
        eixos, [("ocupacao", "Ocupação"), ("en", r"$E[N]$"), ("ew", r"$E[W]$")]
    ):
        for cenario, _, _ in CENARIOS[:5]:
            horizontes = sorted({chave[1] for chave in indices if chave[0] == cenario})
            medias = []
            inferiores = []
            superiores = []
            for horizonte in horizontes:
                diferencas = []
                for chave, pares in indices.items():
                    if chave[0] == cenario and chave[1] == horizonte \
                            and "v3" in pares and "v4" in pares:
                        diferencas.append(pares["v3"][metrica] - pares["v4"][metrica])
                media, inferior, superior = intervalo_confianca(diferencas)
                medias.append(media)
                inferiores.append(media - inferior)
                superiores.append(superior - media)
            eixo.errorbar(horizontes, medias, yerr=[inferiores, superiores],
                          marker="o", capsize=3, label=cenario)
        eixo.axhline(0.0, linestyle=":", color="black")
        eixo.set_xscale("log")
        eixo.set_xlabel("Tempo de simulação")
        eixo.set_ylabel(f"V3 − V4: {titulo}")
        eixo.grid(alpha=0.25)
    eixos[0].legend()
    fig.suptitle("Efeito das correções do V4")
    fig.tight_layout()
    salvar_figura(fig, pasta, "comparacao_v3_v4")


def grafico_boxplots(resultados, versao, pasta):
    dados = [
        linha for linha in resultados
        if linha["versao"] == versao and linha["rho"] < 1.0
    ]
    if not dados:
        return
    maior_horizonte = max(linha["horizonte"] for linha in dados)
    dados = [linha for linha in dados if linha["horizonte"] == maior_horizonte]
    cenarios = [cenario for cenario, _, _ in CENARIOS[:5]]
    fig, eixos = plt.subplots(1, 2, figsize=(12, 5))
    for eixo, (metrica, titulo) in zip(eixos, [("en", r"$E[N]$"), ("ew", r"$E[W]$")]):
        valores = [
            [linha[metrica] for linha in dados if linha["cenario"] == cenario]
            for cenario in cenarios
        ]
        eixo.boxplot(valores, showmeans=True)
        eixo.set_xticks(range(1, len(cenarios) + 1), cenarios)
        eixo.set_ylabel(titulo)
        eixo.set_yscale("log")
        eixo.grid(axis="y", alpha=0.25)
    fig.suptitle(f"Variabilidade entre repetições — {versao.upper()} — T={maior_horizonte:g}")
    fig.tight_layout()
    salvar_figura(fig, pasta, f"boxplots_en_ew_{versao}")


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


def main():
    args = argumentos()
    args.saida.mkdir(parents=True, exist_ok=True)
    pasta_figuras = args.saida / "figuras"
    horizontes = [100.0, 1_000.0, 10_000.0] if args.rapido else [
        100.0, 1_000.0, 10_000.0, 100_000.0,
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

    for versao in versoes:
        executavel = args.saida / f"simulacao_{versao}"
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
        grafico_convergencia(resumo, versao, pasta_figuras)
        grafico_teoria(resumo, versao, pasta_figuras)
        grafico_erros(resumo, versao, pasta_figuras)
        grafico_fluxo(resumo, versao, pasta_figuras)
        grafico_excesso_horizonte(resumo, versao, pasta_figuras)
        grafico_populacao_rho(resumo, versao, pasta_figuras)
        grafico_boxplots(resultados, versao, pasta_figuras)
    grafico_comparacao(resultados, pasta_figuras)


if __name__ == "__main__":
    main()
