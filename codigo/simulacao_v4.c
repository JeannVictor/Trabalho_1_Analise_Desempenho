/* Versão corrigida do simulacao_v3.c, sem acrescentar novas medidas.
 * Correções: entrada validada, semente controlada, horizonte exato,
 * ocupação limitada ao período observado e áreas finalizadas em T.
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

static double aleatorio(void) {
    double u = rand() / ((double)RAND_MAX + 1.0);
    return 1.0 - u;
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
    Info ocupado;
    inicia_info(&en);
    inicia_info(&ew_chegadas);
    inicia_info(&ew_saidas);
    inicia_info(&ocupado);

    double tempo_decorrido = 0.0;
    double chegada_cliente = -log(aleatorio()) / taxa_chegada;
    double saida_cliente = 0.0;
    unsigned long fila = 0;

    while (tempo_decorrido < tempo_simulacao) {
        int proximo_e_chegada = !fila || chegada_cliente <= saida_cliente;
        double proximo_evento = proximo_e_chegada
            ? chegada_cliente
            : saida_cliente;

        if (proximo_evento > tempo_simulacao) {
            atualiza_area(&en, tempo_simulacao);
            atualiza_area(&ew_chegadas, tempo_simulacao);
            atualiza_area(&ew_saidas, tempo_simulacao);
            atualiza_area(&ocupado, tempo_simulacao);
            tempo_decorrido = tempo_simulacao;
            break;
        }

        atualiza_area(&en, proximo_evento);
        atualiza_area(&ew_chegadas, proximo_evento);
        atualiza_area(&ew_saidas, proximo_evento);
        atualiza_area(&ocupado, proximo_evento);
        tempo_decorrido = proximo_evento;

        if (proximo_e_chegada) {
            if (!fila) {
                saida_cliente = tempo_decorrido
                    - log(aleatorio()) / taxa_atendimento;
                ocupado.numero_eventos = 1;
            }
            fila++;
            en.numero_eventos++;
            ew_chegadas.numero_eventos++;
            chegada_cliente = tempo_decorrido
                - log(aleatorio()) / taxa_chegada;
        } else {
            fila--;
            en.numero_eventos--;
            ew_saidas.numero_eventos++;
            if (fila) {
                saida_cliente = tempo_decorrido
                    - log(aleatorio()) / taxa_atendimento;
            } else {
                ocupado.numero_eventos = 0;
            }
        }
    }

    double lambda_observado = ew_chegadas.numero_eventos / tempo_simulacao;
    double vazao = ew_saidas.numero_eventos / tempo_simulacao;
    double en_final = en.soma_areas / tempo_simulacao;
    double ew_final = ew_chegadas.numero_eventos
        ? (ew_chegadas.soma_areas - ew_saidas.soma_areas)
            / ew_chegadas.numero_eventos
        : 0.0;

    printf("ocupacao=%.12f\n", ocupado.soma_areas / tempo_simulacao);
    printf("en=%.12f\n", en_final);
    printf("ew=%.12f\n", ew_final);
    printf("erro_little=%.12f\n", en_final - lambda_observado * ew_final);
    printf("taxa_chegada=%.12f\n", lambda_observado);
    printf("vazao=%.12f\n", vazao);
    printf("fila_final=%lu\n", fila);
    printf("tempo_final=%.12f\n", tempo_decorrido);
    return EXIT_SUCCESS;
}
