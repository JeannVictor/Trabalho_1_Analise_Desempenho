# Guia de Estilo e Humanização de Textos Acadêmicos e Técnicos

## Parte 1: Prompt Consolidado (Catálogo de Marcadores Humanos 1 a 33)

### A. Especificidade e Rastreabilidade
1. **Parâmetros concretos com unidade e instrumento**
   - **Trecho:** “O smartphone utilizado é um Motorola Moto g6 Plus.” / “O comprimento do tubo é medido, utilizando a fita métrica, como sendo 47,6 cm. O diâmetro interno... 7,5 cm.”
   - **Motivo:** O autor registra o que de fato estava na bancada, incluindo como mediu.
   - **Contra-exemplo:** “Um smartphone moderno e um tubo de papelão padrão foram utilizados para o experimento.”
   - **Regra:** Troque substantivos genéricos por modelo, número, unidade e método de medição. Só use dados reais que você tenha. Nunca invente números.

2. **Quem fez o quê nas citações**
   - **Trecho:** “Parolin e Pezzi demonstraram como o experimento pode ser realizado utilizando dois smartphones [7]. Yavuz demonstrou como ele pode ser feito usando um único smartphone ao submergir parcialmente o tubo em água [8].”
   - **Motivo:** Cada referência recebe uma contribuição específica, e a lacuna que justifica o trabalho fica clara.
   - **Contra-exemplo:** “Diversos estudos exploraram o uso de smartphones em experimentos acústicos [7, 8].”
   - **Regra:** Uma frase por referência importante, dizendo o que ela fez de diferente. Só cite fontes verificadas.

3. **Contexto prático para o leitor**
   - **Trecho:** “Para usuários de produtos Apple, o aplicativo de gravação Voice Recorder Lite... e o gerador de sinais Audio Function Generator... podem ser utilizados.”
   - **Motivo:** Antecipa uma necessidade real de quem vai reproduzir o experimento.
   - **Contra-exemplo:** “Vários aplicativos estão disponíveis em ambas as plataformas.”
   - **Regra:** Onde o texto diz “vários/diversos/múltiplos”, substitua por 1 ou 2 nomes concretos.

### B. Honestidade Epistêmica
4. **Admitir o que não se sabe**
   - **Trecho:** “Parece que uma frequência de ressonância não gera um pico... O motivo para isso é desconhecido.”
   - **Motivo:** IA tende a preencher lacunas com explicações plausíveis. O humano deixa a lacuna aberta.
   - **Contra-exemplo:** “Isso provavelmente se deve à interferência destrutiva no sétimo harmônico, que é um fenômeno bem documentado.”
   - **Regra:** Onde a IA “explica demais” algo que o autor não verificou, troque por “não está claro por quê” e registre a consequência (como o autor contornou o problema).

5. **Hedge pontual e calibrado**
   - **Trecho:** “As baixas frequências emitidas pelo gerador de funções talvez estejam fazendo o smartphone vibrar.”
   - **Motivo:** Um único “talvez” (hedge), no ponto exato da incerteza.
   - **Contra-exemplo (inflado):** “As baixas frequências fazem o smartphone vibrar, degradando significativamente a qualidade do sinal.”
   - **Contra-exemplo (excesso):** “Poder-se-ia potencialmente argumentar que as baixas frequências talvez pudessem possivelmente contribuir para alguma vibração.”
   - **Regra:** Um hedge por incerteza real, nem zero nem empilhado.

6. **Resultado relatado sem verniz**
   - **Trecho:** “A velocidade do som no ar a 24 °C foi medida como c = 335 m s⁻¹... O valor medido de c está, portanto, dentro de 3% da previsão teórica.”
   - **Motivo:** Número, comparação e fim. Sem adjetivo de valor (“excelente”, “notável”).
   - **Contra-exemplo:** “Os resultados mostram uma concordância notável com a teoria, validando fortemente a abordagem proposta.”
   - **Regra:** Apague adjetivos avaliativos ao lado de resultados e deixe o número falar.

### C. Decisões, Descartes e Trade-offs
7. **Dados descartados e por quê**
   - **Trecho:** “O início da gravação de áudio mostra-se barulhento demais para ter utilidade... Essa região da gravação é, portanto, cortada antes da análise.” / “esses pontos podem ser ignorados, pois estão distantes dos pontos onde a intensidade sonora da gravação atinge o pico.”
   - **Motivo:** Mostra o “bastidor” da análise: o que não funcionou e a justificativa.
   - **Contra-exemplo:** “O pré-processamento dos dados foi realizado para garantir a qualidade ideal do sinal.”
   - **Regra:** Substitua descrições abstratas de “tratamento” por o que foi descartado, por quê e o efeito na análise.

8. **Escolha de método com critério explícito**
   - **Trecho:** “Este método gera resultados idênticos aos obtidos pelo ZCM. No entanto, o método FFT é significativamente mais lento e, portanto, não é utilizado na análise final.”
   - **Motivo:** Compara alternativas por um critério mensurável e decide.
   - **Contra-exemplo:** “Ambos os métodos se mostraram eficazes, cada um oferecendo vantagens únicas.”
   - **Regra:** Nunca deixe “ambos têm vantagens” sem dizer quais e qual foi escolhido.

9. **Aproximação justificada em tom pragmático**
   - **Trecho:** “À temperatura ambiente e pressão atmosférica normal, o ar se comporta de forma suficientemente próxima a um gás ideal para o nosso propósito.”
   - **Motivo:** O “para o nosso propósito” é um registro levemente coloquial e honesto sobre o limite do modelo.
   - **Contra-exemplo:** “Assume-se que o ar se comporta como um gás ideal sob essas condições.”
   - **Regra:** Quando houver aproximação, diga em uma frase por que ela basta para o objetivo.

### D. Voz e Ritmo
10. **Voz do autor e guia do leitor**
    - **Trecho:** “Olhando para a figura 4, notamos que...” / “Acontece que o comprimento acústico do tubo é ligeiramente maior que seu comprimento físico.” / “Vemos que as frequências de ressonância em função de n seguem a equação de uma reta.”
    - **Motivo:** O texto conduz o leitor com marcas de descoberta (“acontece que”, “notamos”).
    - **Contra-exemplo:** “Como pode ser claramente observado, a Figura 4 demonstra diversos fenômenos notáveis.”
    - **Regra:** Use “nós/notamos/vemos que” e vá direto ao que a figura mostra.

11. **Ritmo irregular**
    - **Trecho:** “O termômetro não é utilizado diretamente na medição, mas serve para medir a temperatura da sala durante o experimento.” (longa) seguida de “A Equação (7) é válida apenas para um gás ideal.” (curta)
    - **Motivo:** A extensão das frases acompanha a complexidade do conteúdo, não um padrão.
    - **Contra-exemplo:** Vários parágrafos com frases de 18 a 22 palavras e estrutura sujeito-verbo-objeto-complemento.
    - **Regra:** Depois de uma frase longa com duas ideias, quebre a próxima em curta. Se três frases seguidas têm o mesmo tamanho, reescreva uma.

12. **Modéstia no objetivo e na conclusão**
    - **Trecho:** “O objetivo deste artigo é tentar realizar o experimento utilizando apenas um smartphone...” / “O experimento exige certa quantidade de programação.”
    - **Motivo:** “Tentar” e a admissão de um custo (programação) mostram um autor que não vende demais.
    - **Contra-exemplo:** “Este artigo apresenta uma abordagem inovadora e revolucionária que revoluciona o ensino de física.”
    - **Regra:** Em introduções e conclusões, troque promessas (“revoluciona”, “inovador”) por escopo real e uma limitação.

13. **Conselho prático proporcional**
    - **Trecho:** “Ter acesso a uma sala como essa não é crítico para o experimento, embora se deva buscar limitar o ruído de fundo o máximo possível.”
    - **Motivo:** Relativiza a condição ideal e diz o que importa de fato.
    - **Contra-exemplo:** “Uma câmara anecoica foi utilizada para garantir condições experimentais ideais.”
    - **Regra:** Quando houver condição ideal, diga se ela é essencial e qual é o mínimo aceitável.

### E. Sobre Imperfeições e Erros Fatos
Trechos com pequenas irregularidades reais ocorrem naturalmente na escrita humana. Não insira erros de digitação de propósito. O que vale aproveitar é a irregularidade natural: ritmo variado, apartes pragmáticos e escolhas justificadas.

---

### F. Evidência e Raciocínio
14. **Previsão e medida lado a lado, com a diferença atribuída**
    - **Trecho:** “Δt₂/Δt₁ ≈ 1,199, enquanto √(a₂/a₁) ≈ 1,207, de modo que a dependência teórica s = ½at² é facilmente comprovada.” / “as áreas [...] também são parecidas (a diferença é um pouco maior que 2%), considerando o ruído experimental.”
    - **Motivo:** Os dois números ficam na mesma frase e a discrepância aparece em porcentagem com uma causa provável.
    - **Contra-exemplo:** “Os resultados concordam de forma excelente com a teoria.”
    - **Regra:** Ponha previsão e medida na mesma frase, com as mesmas casas decimais. Diga a diferença em % e a que a atribui, e só então conclua.

15. **Cadeia de cálculo rastreável**
    - **Trecho:** “Das massas do carrinho (m_c = 318,8 g) e do corpo em queda (m_b = 358,05 g) calcula-se a aceleração teórica sem atrito, a_teo = 5,18 m/s² [...] μ = (m_b g − (m_c + m_b) a_exp)/(m_c g), resultando μ = 0,61.”
    - **Motivo:** O leitor vê as entradas, a fórmula e o resultado, conseguindo refazer a conta diretamente.
    - **Contra-exemplo:** “O coeficiente de atrito foi obtido a partir dos dados experimentais.”
    - **Regra:** Para cada número derivado, escreva: entradas → fórmula → resultado.

16. **Mostrar por que um efeito é real**
    - **Trecho:** As oscilações “aparecem de forma consistente em todos os experimentos e, então, não podem ser consideradas um artefato experimental”; três medições independentes são mostradas “para ilustrar a repetibilidade”.
    - **Motivo:** O argumento apoia-se em um teste concreto (repetição em todas as execuções), não em uma simples afirmação.
    - **Contra-exemplo:** “Esse comportamento é claramente de origem física, e não instrumental.”
    - **Regra:** Quando negar que algo seja artefato ou acaso, diga qual teste sustenta isso (quantas repetições, em que condições).

17. **Hipótese testada que não funcionou**
    - **Trecho:** “Para o comportamento teórico, testamos acelerações com amortecimento puramente de Coulomb e puramente viscoso, mas os resultados parecem uma mistura de ambos, o que dificulta a análise.”
    - **Motivo:** Mostra uma tentativa frustrada e o desdobramento real da análise.
    - **Contra-exemplo:** “O modelo de amortecimento adotado descreve adequadamente os dados.”
    - **Regra:** Cite a alternativa testada, o que deu errado e qual encaminhamento foi adotado (somente se isso tiver de fato ocorrido).

18. **Interpretação assumida como própria**
    - **Trecho:** “Em nossa opinião, essas oscilações aparecem devido ao efeito combinado [...]” / “Do nosso ponto de vista, essas oscilações refletem variações na aceleração [...]”
    - **Motivo:** Separa o fato medido da interpretação do autor sem fingir consenso universal.
    - **Contra-exemplo:** “Essas oscilações são causadas pelo efeito combinado [...]”
    - **Regra:** Interpretação sem teste direto recebe um rótulo explícito (“interpretamos como”, “em nossa leitura”).

### G. Escala e Contexto Concreto
19. **Número com escala**
    - **Trecho:** “elongação inicial do fio em torno de 1,2·10⁻³ m (o comprimento do fio usado era aproximadamente 1,75 m)”.
    - **Motivo:** Fornece um parâmetro de referência para o leitor julgar a dimensão do valor.
    - **Contra-exemplo:** “A elongação do fio é muito pequena.”
    - **Regra:** Troque qualificadores como "pequeno", "grande" ou "significativo" por um número acompanhado de referência (razão, % ou ordem de grandeza).

20. **O exemplo mostrado é um entre vários**
    - **Trecho:** “Em nossos experimentos, usamos diferentes configurações [...] A Figura 1 mostra os resultados de um desses experimentos [...] apenas um dos corpos estava em movimento antes do impacto.”
    - **Motivo:** Informa o universo de testes, qual recorte foi selecionado e sob quais condições.
    - **Contra-exemplo:** “A Figura 1 apresenta os resultados obtidos.”
    - **Regra:** Diga quantos casos foram testados, qual deles está ilustrado na figura e qual era a condição específica.

21. **Dica de bancada com a consequência**
    - **Trecho:** “a parte inferior do carrinho deve ser protegida, por exemplo com fita isolante, para evitar riscar o trilho, o que também alteraria o coeficiente de atrito ao longo do experimento.”
    - **Motivo:** O cuidado prático vem acompanhado da ação e do dano gerado caso seja ignorado.
    - **Contra-exemplo:** “Recomenda-se cuidado com os equipamentos utilizados.”
    - **Regra:** Escreva a recomendação prática no formato: ação concreta + consequência direta de ignorá-la.

22. **Valor nominal x valor medido**
    - **Trecho:** “o valor da tensão da fonte E (≈ 3 V)” na descrição do circuito; depois: “O erro de leitura do voltímetro foi de ± 0,01 V e do microamperímetro de ± 0,1 µA. A tensão inicial em todas as leituras foi de E = 2,67 V.”
    - **Motivo:** Distingue o parâmetro de projeto do valor real aferido na bancada, registrando a incerteza instrumental.
    - **Contra-exemplo:** “Utilizou-se uma fonte de 3 V e instrumentos de alta precisão.”
    - **Regra:** Separe o valor planejado do observado e declare a incerteza do instrumento.

### H. Posicionamento diante da Literatura e do Público
23. **Crítica específica ao método vizinho**
    - **Trecho:** “se sua sensibilidade não for adequada, os valores de tensão medidos [...] terão intervalos de medição relativamente altos”; “assume-se [...] o mesmo comportamento linear [...] o que não condiz com os resultados experimentais”; “Em nossa metodologia [...] a medida é feita diretamente, sem o uso de extrapolação gráfica. Dessa forma, os erros [...] dependem somente da precisão dos instrumentos utilizados [...] e da qualidade dos LEDs.”
    - **Motivo:** Detalha a limitação, o mecanismo físico/matemático e o impacto do novo método sobre a margem de erro.
    - **Contra-exemplo:** “Os métodos existentes apresentam limitações que a abordagem proposta busca superar.”
    - **Regra:** Apresente a limitação existente → o mecanismo que a causa → a alteração exata no erro trazida pelo seu método.

24. **Diferença justificada pelo público, não por ranking**
    - **Trecho:** Outros autores usaram metodologia semelhante “porém com sistemas de aquisição de dados mais complexos”; as resistências adicionais exigem interpretações “que estão fora do escopo da abordagem experimental”.
    - **Motivo:** Em vez de classificar o trabalho alheio como inferior, explica que ele atende a outro contexto de aplicação.
    - **Contra-exemplo:** “Nossa abordagem é superior às demais.”
    - **Regra:** Justifique escolhas metodológicas com base no perfil de uso (custo, nível técnico do aluno, tempo disponível), não em superioridade genérica.

25. **Motivação ancorada em restrição real**
    - **Trecho:** “grande parte da atividade experimental depende de aparatos complexos e caros, ficando, portanto, sua aquisição fora da realidade da grande maioria das escolas, ou mesmo das faculdades e universidades.”
    - **Motivo:** A introdução parte de um gargalo prático e verificável do ambiente do autor.
    - **Contra-exemplo:** “A atividade experimental desempenha papel fundamental no ensino de física.”
    - **Regra:** Abra o trabalho citando uma restrição concreta e checável (orçamento, equipamentos, tempo de aula, acesso a dados), evitando truísmos.

### I. Recursos de Escrita Didática
26. **Glosa do termo**
    - **Trecho:** “Os LEDs (do inglês, *light emitting diode* ou 'diodo emissor de luz')"; “*gap* (do inglês, 'lacuna') ou barreira de potencial”.
    - **Motivo:** Fornece a sigla técnica de uso corrente, a origem no idioma original e a tradução direta.
    - **Contra-exemplo:** Usar siglas sem definição ou substituí-las por paráfrases vagas ("dispositivos de luz").
    - **Regra:** Na primeira menção, registre o termo corrente, o nome original em inglês e o equivalente em português.

27. **Parêntese com definição, data e nome**
    - **Trecho:** “efeito fotoelétrico (que consiste na emissão de elétrons por um condutor quando exposto a radiações de altas frequências, primeiramente observado por A. E. Becquerel, em 1839, e confirmado por Heinrich Hertz, em 1887)”.
    - **Motivo:** O aposto traz definição sucinta, nomes e anos verificáveis na história da ciência.
    - **Contra-exemplo:** “Desde o início do século XX, a física passou por profundas transformações.”
    - **Regra:** Insira apostos explicativos contendo definição curta, nomes e datas históricas verificadas.

28. **Material do dia a dia com substituto**
    - **Trecho:** “Fios de conexão (podem ser fios de internet ou fios apropriados para prototipagem em Protoboard)”; “Bateria de 3 V (de lítio, daquelas encontradas em produtos eletrônicos) ou duas pilhas AA em série”.
    - **Motivo:** Emprega vocabulário de bancada e dá opções acessíveis para substituição de componentes.
    - **Contra-exemplo:** “Foram utilizados materiais de baixo custo e fácil aquisição.”
    - **Regra:** Em vez de escrever “baixo custo”, nomeie o componente, informe onde obtê-lo ou indique um substituto direto.

29. **Âncora observável**
    - **Trecho:** “Neste instante a corrente no LED atinge o valor máximo [...] e ele brilhará”; “a consequente diminuição do brilho no LED pode ser acompanhada instantaneamente pelo microamperímetro.”
    - **Motivo:** Associa conceitos teóricos a manifestações visuais ou leituras diretas no instrumento.
    - **Contra-exemplo:** “O comportamento do dispositivo pode ser monitorado em tempo real.”
    - **Regra:** Conecte variações de grandezas a um sinal perceptível (emissão de luz, desvio do ponteiro, alteração no gráfico).

### J. Extensões e Conclusões Não Óbvias
30. **Alternativas por nível de recurso**
    - **Trecho:** “Outra alternativa, para laboratórios mais equipados, é medir o comprimento de onda dos LEDs por meio da difração [...] através de uma rede de difração” [PL]. “Os usuários também poderiam adicionar um segundo smartphone ao corpo em queda e verificar que a aceleração [...] é a mesma” [AT].
    - **Contra-exemplo:** “Trabalhos futuros podem explorar melhorias adicionais.”
    - **Regra:** Cada proposta de desdobramento deve definir: quem pode realizar, quais equipamentos são necessários e o que será testado.

31. **Uso inverso e benefício colateral**
    - **Trecho:** “esta atividade experimental pode ser usada com a finalidade de se determinar os comprimentos de onda de diversos LEDs (uma vez conhecido h)” [PL]. “Alguns dos conceitos reforçados [...] aceleração, colisões, momento, atrito [...] e até mesmo elasticidade”; “aprender a importância da precisão dos sensores” [AT].
    - **Motivo:** Aponta aplicações secundárias do arranjo (a ferramenta vira objeto de estudo ou gera aprendizado prático não planejado).
    - **Contra-exemplo:** “O experimento reforça diversos conceitos importantes.”
    - **Regra:** Cite no máximo uma aplicação inversa ou um aprendizado secundário específico.

32. **Adjetivo avaliativo com critério verificável**
    - **Trecho:** “O resultado [...] pode ser considerado como satisfatório, visto que o valor da constante de Planck registrado na literatura encontra-se dentro da margem de erro do obtido neste trabalho.” (Verificação: 6,63 está contido no intervalo 6,89 ± 0,69).
    - **Motivo:** Valida o uso de um qualificador ao vinculá-lo a uma comparação matemática verificável pelo leitor.
    - **Contra-exemplo:** “Os resultados foram excelentes.”
    - **Regra:** Se utilizar um adjetivo avaliativo, insira imediatamente “visto que/pois” seguido do critério numérico que o justifica.

33. **Origem do dado fraco e ordem das causas de erro**
    - **Trecho:** O erro “se deve, em grande parte, ao valor do comprimento de onda [...] uma vez que os obtivemos de tabelas encontradas na rede [...] esses valores podem variar significativamente de acordo com o fabricante. Além disso [...] consideramos os LEDs como fontes monocromáticas [...] Outro fator [...] a precisão dos instrumentos”.
    - **Motivo:** Classifica as fontes de desvio em ordem de relevância (causa principal seguida de secundárias) e indica a origem dos dados problemáticos.
    - **Contra-exemplo:** “Diversos fatores podem ter contribuído para o erro, como limitações instrumentais e condições experimentais.”
    - **Regra:** Ordene as causas de erro começando pela principal e indicando a origem do dado impreciso. Estime o peso relativo dos desvios ou suavize a atribuição se não houver dados exatos.

---

### Checklist de Revisão Posterior
1. Existe algum “vários/diversos/numerosos/muitos” sem exemplo? → Nomeie 1 ou 2.
2. Existe verbo abstrato de método (“otimizado”, “alavancado”, “garantido”)? → Diga exatamente o que foi feito.
3. Existe adjetivo de valor ao lado de um resultado? → Remova ou adicione critério numérico testável (Regra 32).
4. Existe explicação para algo que o autor não verificou? → Troque por “não está claro por quê”.
5. Cada descarte ou escolha de método tem motivo e consequência documentados?
6. As frases de um mesmo parágrafo variam em extensão?
7. A conclusão menciona ao menos uma limitação ou custo real?
8. Há parâmetros de medição sem instrumento, modelo ou incerteza declarada?
9. Os desdobramentos futuros especificam recursos necessários e o parâmetro a ser testado?

### Ressalvas de Aplicação
A presença destes padrões só é válida quando amparada por dados experimentais e decisões reais. Tentar simular especificidade sem possuir os dados de bancada resultará em invenção de informações.

---

# Relatório: Marcadores de Escrita por IA e Diretrizes de Reescrita Técnica

## 1. Mapeamento de Vícios de Linguagem de LLMs

Modelos de linguagem apresentam padrões de redação que diferem do registro de escrita de pesquisadores em laboratório. A tabela abaixo sintetiza os principais marcadores identificados, suas estruturas típicas e as estratégias de correção baseadas no catálogo de marcadores humanos.

| Marcador de IA | Estrutura Típica em LLMs | Problema de Redação | Regra de Correção Humana |
|---|---|---|---|
| **Contrastes Artificiais** | "Não é X, mas Y" / "Não apenas X, mas também Y" | Cria falsa oposição para enfatizar a segunda parte da frase. | **Regra 10 & 11:** Vá direto ao fato sem antíteses decorativas. |
| **Tautologia após Dois-Pontos** | "O resultado é relevante: demonstra X" | Repete a premissa inicial com palavras ligeiramente diferentes. | **Regra 6 & 15:** Apresente o número, a fórmula ou a comparação direta. |
| **Tríades Estáticas** | "Precisão, eficiência e confiabilidade" | Agrupa adjetivos abstratos em trios para simular abrangência. | **Regra 1 & 7:** Substitua adjetivos por parâmetros mensuráveis e cortes reais. |
| **Dressed-Up Verbs & Supervalorização** | "Configura-se como" / "Desempenha papel crucial" | Usa verbos e adjetivos inflados no lugar de dados de medição. | **Regra 6 & 32:** Elimine adjetivos de valor ou vincule-os a critérios numéricos. |
| **Ressalvas Genéricas** | "Embora positivo, limitações devem ser consideradas" | Insere cautela abstrata sem citar a limitação real ocorrida. | **Regra 17 & 33:** Cite o erro real, a origem do dado e a ordem das causas. |
| **Autoridades Vagas** | "Estudos demonstram" / "Especialistas afirmam" | Evoca consenso sem fornecer citação ou dados específicos. | **Regra 2 & 27:** Nomeie o autor, a contribuição única ou a data histórica. |

---

## 2. Avaliação de Marcadores de Autoria

A presença de conectivos isolados ou termos técnicos não permite determinar se um texto foi escrito por humano ou por IA. A análise estilística depende da densidade de estruturas vazias por bloco de texto.

| Padrão Observado | Frequência em IA | Frequência em Humano | Relevância como Indicador |
|---|---|---|---|
| Repetição de frases curtas seguidas de explicações por dois-pontos | Alta | Baixa | Moderada |
| Enumeração sistemática de 3 adjetivos abstractos | Muito Alta | Rara | Alta |
| Omissão de modelos de aparelhos, incertezas e marcas | Alta | Rara em textos experimentais | Alta |
| Variação no tamanho de frases dentro do mesmo parágrafo | Baixa | Alta | Alta |
| Uso isolado de "Além disso" ou "Ademais" | Alta | Média | Baixa |

A escrita técnica de laboratório diferencia-se pela presença de restrições operacionais, marcas de instrumentos, valores nominais contrastados com valores aferidos e decisões de descarte justificadas. Sem esses dados concretos de bancada, ajustes estilísticos apenas mascaram trechos genéricos sem adicionar valor factual ao texto.
