/* Versão corrigida do simulacao_v3.c.
 * Correções: entrada validada, semente controlada, horizonte exato,
 * ocupação limitada ao período observado e áreas finalizadas em T.
 * Extensões: fila de espera (E[Nq] e E[Wq]), comprimento máximo da fila,
 * período de aquecimento opcional (quinto valor da entrada) e tempo de
 * permanência medido cliente a cliente (média e percentis).
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    unsigned long numero_eventos;
    double soma_areas;
    double tempo_anterior;
} Info;

static void inicia_info(Info *info) {
    info->numero_eventos = 0;
    info->soma_areas = 0.0;
    info->tempo_anterior = 0.0;
}

static void atualiza_area(Info *info, double tempo) {
    info->soma_areas += info->numero_eventos
        * (tempo - info->tempo_anterior);
    info->tempo_anterior = tempo;
}

/* Vetor de double que cresce conforme necessário. */
typedef struct {
    double *dados;
    size_t tamanho;
    size_t capacidade;
} Vetor;

static void insere(Vetor *vetor, double valor) {
    if (vetor->tamanho == vetor->capacidade) {
        vetor->capacidade = vetor->capacidade ? 2 * vetor->capacidade : 1024;
        vetor->dados = realloc(vetor->dados,
                               vetor->capacidade * sizeof(double));
        if (!vetor->dados) {
            exit(EXIT_FAILURE);
        }
    }
    vetor->dados[vetor->tamanho++] = valor;
}

static int compara(const void *a, const void *b) {
    double x = *(const double *)a;
    double y = *(const double *)b;
    return (x > y) - (x < y);
}

/* Percentil pelo posto mais próximo, num vetor já ordenado. */
static double percentil(const Vetor *vetor, double p) {
    if (!vetor->tamanho) {
        return 0.0;
    }
    return vetor->dados[(size_t)(p * (vetor->tamanho - 1))];
}

static double aleatorio(void) {
    double u = rand() / ((double)RAND_MAX + 1.0);
    return 1.0 - u;
}

int main(void) {
    double media_entre_chegadas;
    double media_atendimento;
    double tempo_simulacao;
    unsigned int semente;
    double aquecimento = 0.0;

    if (scanf("%lf %lf %lf %u", &media_entre_chegadas,
              &media_atendimento, &tempo_simulacao, &semente) != 4) {
        return EXIT_FAILURE;
    }
    /* O aquecimento é opcional: sem o quinto valor, a coleta começa em 0. */
    if (scanf("%lf", &aquecimento) != 1) {
        aquecimento = 0.0;
    }
    if (media_entre_chegadas <= 0.0 || media_atendimento <= 0.0 ||
        tempo_simulacao <= 0.0 || aquecimento < 0.0 ||
        aquecimento >= tempo_simulacao) {
        return EXIT_FAILURE;
    }

    srand(semente);
    double taxa_chegada = 1.0 / media_entre_chegadas;
    double taxa_atendimento = 1.0 / media_atendimento;

    Info en;
    Info ew_chegadas;
    Info ew_saidas;
    Info ocupado;
    Info espera; /* clientes aguardando, sem contar o que está em atendimento */
    inicia_info(&en);
    inicia_info(&ew_chegadas);
    inicia_info(&ew_saidas);
    inicia_info(&ocupado);
    inicia_info(&espera);

    double tempo_decorrido = 0.0;
    double chegada_cliente = -log(aleatorio()) / taxa_chegada;
    double saida_cliente = 0.0;
    unsigned long fila = 0;
    unsigned long fila_maxima = 0;
    unsigned long presentes_no_aquecimento = 0;
    int coletando = aquecimento == 0.0;

    /* Instantes de chegada de quem ainda não saiu, em ordem de chegada:
     * como o atendimento é FCFS, quem sai é sempre o primeiro da lista. */
    Vetor instantes_chegada = {NULL, 0, 0};
    size_t primeiro_da_fila = 0;
    Vetor permanencias = {NULL, 0, 0};

    while (tempo_decorrido < tempo_simulacao) {
        int proximo_e_chegada = !fila || chegada_cliente <= saida_cliente;
        double proximo_evento = proximo_e_chegada
            ? chegada_cliente
            : saida_cliente;

        /* Fim do aquecimento: descarta o que foi acumulado até aqui.
         * Quem já está no sistema entra como "chegada" da janela, para que
         * a diferença entre as áreas de chegadas e saídas continue sendo N(t). */
        if (!coletando && proximo_evento > aquecimento) {
            inicia_info(&en);
            inicia_info(&ew_chegadas);
            inicia_info(&ew_saidas);
            inicia_info(&ocupado);
            inicia_info(&espera);
            en.tempo_anterior = ew_chegadas.tempo_anterior = aquecimento;
            ew_saidas.tempo_anterior = ocupado.tempo_anterior = aquecimento;
            espera.tempo_anterior = aquecimento;
            en.numero_eventos = fila;
            ew_chegadas.numero_eventos = fila;
            ocupado.numero_eventos = fila ? 1 : 0;
            espera.numero_eventos = fila ? fila - 1 : 0;
            presentes_no_aquecimento = fila;
            fila_maxima = fila;
            coletando = 1;
        }

        if (proximo_evento > tempo_simulacao) {
            atualiza_area(&en, tempo_simulacao);
            atualiza_area(&ew_chegadas, tempo_simulacao);
            atualiza_area(&ew_saidas, tempo_simulacao);
            atualiza_area(&ocupado, tempo_simulacao);
            atualiza_area(&espera, tempo_simulacao);
            tempo_decorrido = tempo_simulacao;
            break;
        }

        atualiza_area(&en, proximo_evento);
        atualiza_area(&ew_chegadas, proximo_evento);
        atualiza_area(&ew_saidas, proximo_evento);
        atualiza_area(&ocupado, proximo_evento);
        atualiza_area(&espera, proximo_evento);
        tempo_decorrido = proximo_evento;

        if (proximo_e_chegada) {
            if (!fila) {
                saida_cliente = tempo_decorrido
                    - log(aleatorio()) / taxa_atendimento;
                ocupado.numero_eventos = 1;
            }
            fila++;
            insere(&instantes_chegada, tempo_decorrido);
            en.numero_eventos++;
            ew_chegadas.numero_eventos++;
            chegada_cliente = tempo_decorrido
                - log(aleatorio()) / taxa_chegada;
        } else {
            fila--;
            double chegou = instantes_chegada.dados[primeiro_da_fila++];
            /* Só entra quem chegou e saiu dentro da janela observada. */
            if (coletando && chegou >= aquecimento) {
                insere(&permanencias, tempo_decorrido - chegou);
            }
            en.numero_eventos--;
            ew_saidas.numero_eventos++;
            if (fila) {
                saida_cliente = tempo_decorrido
                    - log(aleatorio()) / taxa_atendimento;
            } else {
                ocupado.numero_eventos = 0;
            }
        }
        espera.numero_eventos = fila ? fila - 1 : 0;
        if (coletando && fila > fila_maxima) {
            fila_maxima = fila;
        }
    }

    double janela = tempo_simulacao - aquecimento;
    unsigned long chegadas = ew_chegadas.numero_eventos
        - presentes_no_aquecimento;
    double lambda_observado = chegadas / janela;
    double vazao = ew_saidas.numero_eventos / janela;
    double en_final = en.soma_areas / janela;
    double ew_final = chegadas
        ? (ew_chegadas.soma_areas - ew_saidas.soma_areas) / chegadas
        : 0.0;
    double enq_final = espera.soma_areas / janela;
    double ewq_final = chegadas ? espera.soma_areas / chegadas : 0.0;

    double soma_permanencias = 0.0;
    for (size_t i = 0; i < permanencias.tamanho; i++) {
        soma_permanencias += permanencias.dados[i];
    }
    double w_direto = permanencias.tamanho
        ? soma_permanencias / permanencias.tamanho
        : 0.0;
    qsort(permanencias.dados, permanencias.tamanho, sizeof(double), compara);

    printf("ocupacao=%.12f\n", ocupado.soma_areas / janela);
    printf("en=%.12f\n", en_final);
    printf("ew=%.12f\n", ew_final);
    printf("erro_little=%.12f\n", en_final - lambda_observado * ew_final);
    printf("taxa_chegada=%.12f\n", lambda_observado);
    printf("vazao=%.12f\n", vazao);
    printf("fila_final=%lu\n", fila);
    printf("tempo_final=%.12f\n", tempo_decorrido);
    printf("enq=%.12f\n", enq_final);
    printf("ewq=%.12f\n", ewq_final);
    printf("fila_maxima=%lu\n", fila_maxima);
    printf("w_direto=%.12f\n", w_direto);
    printf("w_p50=%.12f\n", percentil(&permanencias, 0.50));
    printf("w_p95=%.12f\n", percentil(&permanencias, 0.95));
    free(instantes_chegada.dados);
    free(permanencias.dados);
    return EXIT_SUCCESS;
}
