/* Cópia de teste do simulacao_v3.c.
 * Mantém a lógica original. Apenas recebe a semente, remove as mensagens
 * de cada evento e imprime uma saída simples para o Python.
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

static double aleatorio(void) {
    double u = rand() / ((double)RAND_MAX + 1.0);
    return 1.0 - u;
}

static double menor(double a, double b) {
    return a < b ? a : b;
}

int main(void) {
    double media_entre_chegadas;
    double media_atendimento;
    double tempo_simulacao;
    unsigned int semente;

    if (scanf("%lf %lf %lf %u", &media_entre_chegadas,
              &media_atendimento, &tempo_simulacao, &semente) != 4) {
        return EXIT_FAILURE;
    }
    if (media_entre_chegadas <= 0.0 || media_atendimento <= 0.0 ||
        tempo_simulacao <= 0.0) {
        return EXIT_FAILURE;
    }

    srand(semente);
    double taxa_chegada = 1.0 / media_entre_chegadas;
    double taxa_atendimento = 1.0 / media_atendimento;

    Info en;
    Info ew_chegadas;
    Info ew_saidas;
    inicia_info(&en);
    inicia_info(&ew_chegadas);
    inicia_info(&ew_saidas);

    double tempo_decorrido = 0.0;
    double chegada_cliente = -log(aleatorio()) / taxa_chegada;
    double saida_cliente = 0.0;
    unsigned long fila = 0;
    double soma_atendimentos = 0.0;

    /* O comportamento de ultrapassar o horizonte é preservado de propósito. */
    while (tempo_decorrido < tempo_simulacao) {
        tempo_decorrido = fila
            ? menor(chegada_cliente, saida_cliente)
            : chegada_cliente;

        if (tempo_decorrido == chegada_cliente) {
            if (!fila) {
                saida_cliente = tempo_decorrido
                    - log(aleatorio()) / taxa_atendimento;
                soma_atendimentos += saida_cliente - tempo_decorrido;
            }
            fila++;
            chegada_cliente = tempo_decorrido
                - log(aleatorio()) / taxa_chegada;

            en.soma_areas += en.numero_eventos
                * (tempo_decorrido - en.tempo_anterior);
            en.tempo_anterior = tempo_decorrido;
            en.numero_eventos++;

            ew_chegadas.soma_areas += ew_chegadas.numero_eventos
                * (tempo_decorrido - ew_chegadas.tempo_anterior);
            ew_chegadas.tempo_anterior = tempo_decorrido;
            ew_chegadas.numero_eventos++;
        } else {
            fila--;
            if (fila) {
                saida_cliente = tempo_decorrido
                    - log(aleatorio()) / taxa_atendimento;
                soma_atendimentos += saida_cliente - tempo_decorrido;
            }

            en.soma_areas += en.numero_eventos
                * (tempo_decorrido - en.tempo_anterior);
            en.tempo_anterior = tempo_decorrido;
            en.numero_eventos--;

            ew_saidas.soma_areas += ew_saidas.numero_eventos
                * (tempo_decorrido - ew_saidas.tempo_anterior);
            ew_saidas.tempo_anterior = tempo_decorrido;
            ew_saidas.numero_eventos++;
        }
    }

    ew_chegadas.soma_areas += ew_chegadas.numero_eventos
        * (tempo_decorrido - ew_chegadas.tempo_anterior);
    ew_saidas.soma_areas += ew_saidas.numero_eventos
        * (tempo_decorrido - ew_saidas.tempo_anterior);

    double lambda_observado = ew_chegadas.numero_eventos / tempo_decorrido;
    double vazao = ew_saidas.numero_eventos / tempo_decorrido;
    double en_final = en.soma_areas / tempo_decorrido;
    double ew_final = (ew_chegadas.soma_areas - ew_saidas.soma_areas)
        / ew_chegadas.numero_eventos;

    printf("ocupacao=%.12f\n", soma_atendimentos / tempo_decorrido);
    printf("en=%.12f\n", en_final);
    printf("ew=%.12f\n", ew_final);
    printf("erro_little=%.12f\n", en_final - lambda_observado * ew_final);
    printf("taxa_chegada=%.12f\n", lambda_observado);
    printf("vazao=%.12f\n", vazao);
    printf("fila_final=%lu\n", fila);
    printf("tempo_final=%.12f\n", tempo_decorrido);
    return EXIT_SUCCESS;
}
