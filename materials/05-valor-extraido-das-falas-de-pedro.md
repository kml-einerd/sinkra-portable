# Valor extraído das falas de Pedro Valério

## Resumo executivo

1. A unidade central de valor não é o prompt nem o modelo, mas uma metodologia própria de processos, regras, contexto e execução. **[opinião/recomendação — 00:50:22–00:50:42]**
2. A arquitetura deve ser independente de modelo, permitindo rotear cada atividade para a engine mais adequada sem reconstruir o sistema. **[recomendação — 00:54:16–00:54:58]**
3. Skills determinísticas devem executar passos definidos; agentes devem decidir caminhos, variáveis e executor. **[modelo operacional — 03:48:05–03:48:37]**
4. O trabalho multiagente precisa de orquestração governada: dependências, branches, worktrees, fan-in, conflitos, filas e gates. **[modelo operacional — 03:18:24–03:19:38; 03:29:45–03:31:48]**
5. Contexto durável — SOT, transcripts, decisões, learning e memória — é necessário para evitar a perda de continuidade entre sessões. **[relato/recomendação — 01:17:09–01:19:16; 02:02:39–02:05:25]**
6. A IA deve ser tratada como ferramenta probabilística, não como humano; o humano mantém responsabilidade, decisão e *skin in the game*. **[opinião/limite — 01:37:47–01:38:36; 04:10:40–04:12:01]**
7. A autonomia deve ser conquistada empiricamente: registrar decisões, medir discordâncias e só remover gates quando houver evidência suficiente. **[recomendação — 04:29:51–04:31:00]**

## Teses de maior valor

### 1. A era do prompt isolado perdeu centralidade

- **Tese:** A evolução relevante saiu de prompt engineering e passou por task, skill e harness; porém, a necessidade permanente é uma metodologia.
- **Evidência/timestamp:** Pedro afirma que prompt engineering era mais necessário quando os modelos eram ruins e que a constante é a metodologia. **[opinião — 00:49:52–00:50:22]**
- **Consequência prática:** Melhorar instruções pontuais não substitui processos, critérios de qualidade e forma de trabalho.
- **Ação recomendada:** Documentar o processo, as regras e os critérios antes de otimizar prompts individuais.

### 2. A diferenciação está nas regras próprias da operação

- **Tese:** O valor singular vem de quem define as regras, processos, estrutura e modelos usados pela equipe.
- **Evidência/timestamp:** Pedro destaca que o diferencial é trazer algo único da pessoa, negócio ou empresa para padronizar a entrega. **[opinião/recomendação — 00:50:22–00:50:42]**
- **Consequência prática:** Uma solução genérica pode usar bons modelos e ainda assim não reproduzir a qualidade específica de uma operação.
- **Ação recomendada:** Registrar padrões internos de decisão, execução e qualidade como ativos reutilizáveis.

### 3. A arquitetura deve acompanhar a mudança dos modelos

- **Tese:** Um sistema deve funcionar como uma arquitetura “flutuante”, capaz de aproveitar diferentes modelos sem ficar preso a um fornecedor ou engine.
- **Evidência/timestamp:** Pedro compara a arquitetura independente de modelo a um barco que acompanha a subida ou descida da maré. **[metáfora operacional — 00:54:16–00:54:58]**
- **Consequência prática:** A troca de modelo deixa de exigir a reconstrução de toda a operação.
- **Ação recomendada:** Separar o núcleo do processo dos adapters, terminais e engines específicas.

### 4. O modelo deve ser escolhido por atividade, não por lealdade

- **Tese:** Claude, Codex e Grok podem ser úteis em tarefas diferentes; o sistema deve encaminhar cada atividade conforme capacidade e qualidade.
- **Evidência/timestamp:** Pedro descreve o Claude como mais arquitetural, o Codex como mais direto e o Grok como orientado a resolver, além de propor delegação cross-model. **[avaliação/opinião — 00:48:28–00:49:30; 01:12:28–01:13:12]**
- **Consequência prática:** A pergunta deixa de ser “qual é o melhor modelo?” e passa a ser “qual modelo é mais adequado para esta tarefa?”.
- **Ação recomendada:** Criar uma matriz simples de atividades, modelos, resultados e custo observado.

### 5. O hype de modelos pode destruir a entrega

- **Tese:** Testar continuamente cada lançamento pode produzir experimentação permanente sem conclusão de projetos.
- **Evidência/timestamp:** Pedro recomenda fugir do impulso de testar todo modelo novo e priorizar entregas, embora reconheça que mudanças relevantes não podem ser ignoradas. **[recomendação — 00:51:48–00:52:37]**
- **Consequência prática:** A equipe pode gastar mais tempo avaliando ferramentas do que produzindo resultados.
- **Ação recomendada:** Reservar uma janela limitada para avaliação e exigir um critério de adoção ou descarte.

### 6. O processo deve ser mapeado antes da skill

- **Tese:** Skills robustas nascem do mapeamento de entidades, etapas, dependências e transições do processo.
- **Evidência/timestamp:** Pedro diz que qualquer skill ou projeto começa pelo mapeamento do processo e exemplifica a eliminação de etapas desnecessárias em um aplicativo. **[recomendação — 01:36:12–01:37:35]**
- **Consequência prática:** O sistema pode eliminar handoffs, uploads, decisões manuais e etapas redundantes antes de automatizá-las.
- **Ação recomendada:** Mapear uma entidade, seu ciclo de vida, entradas, saídas e pontos de decisão antes de implementar a automação.

### 7. A skill é a ponte entre linguagem e determinismo

- **Tese:** A skill traduz a interpretação linguística da LLM em código, regras e ações determinísticas.
- **Evidência/timestamp:** Pedro descreve a skill como túnel ou ponte entre o determinístico e a LLM, acionando código e devolvendo ao terminal a estrutura necessária. **[modelo conceitual — 02:22:22–02:24:12]**
- **Consequência prática:** O sistema não precisa delegar à LLM decisões que podem ser executadas por algoritmo, score ou árvore de decisão.
- **Ação recomendada:** Identificar quais partes do processo exigem interpretação e quais devem ser codificadas.

### 8. A variabilidade da IA exige contenção arquitetural

- **Tese:** Quando uma LLM interpreta uma etapa determinística, o processo passa a incorporar variabilidade desnecessária.
- **Evidência/timestamp:** Pedro afirma que a IA varia e que usar sua interpretação em árvores de decisão, scores ou algoritmos torna variável uma etapa que poderia ser determinística. **[limite — 02:20:16–02:21:30]**
- **Consequência prática:** Resultados aparentemente equivalentes podem divergir entre execuções.
- **Ação recomendada:** Substituir interpretação livre por regras, validações e códigos sempre que o problema tiver critérios objetivos.

### 9. O contexto deve ser durável e recuperável

- **Tese:** Sessões fechadas precisam gerar handoffs, relatórios e registros para que o trabalho continue sem depender da memória do operador.
- **Evidência/timestamp:** Pedro descreve relatórios automáticos de sessões encerradas e o handoff capturado pelo Conductor. **[relato/recomendação — 01:17:09–01:18:54]**
- **Consequência prática:** O operador pode retomar projetos sem reconstruir manualmente o que aconteceu.
- **Ação recomendada:** Exigir, ao final de cada sessão, registro de ações, decisões, pendências, artefatos e próximo passo.

### 10. Memória operacional deve ser seletiva

- **Tese:** Sessões podem ser retiradas do espaço ativo e preservadas para retomada posterior, evitando consumo contínuo de memória e recursos.
- **Evidência/timestamp:** Pedro chama essa prática de colocar sessões em um “freezer” para não consumir recursos, mantendo a possibilidade de retorno. **[relato/prática — 01:26:12–01:27:08]**
- **Consequência prática:** O sistema mantém continuidade sem deixar todos os contextos ativos simultaneamente.
- **Ação recomendada:** Definir estados de sessão: ativa, pausada, arquivada e encerrada, com critérios de retomada.

### 11. A sessão principal deve concentrar a orquestração

- **Tese:** O usuário deve conversar com uma interface principal, enquanto ela cria, acompanha e coordena as sessões secundárias.
- **Evidência/timestamp:** Pedro descreve uma sessão master que monitora terminais e uma interface única que cria e processa os demais. **[modelo operacional — 01:18:54–01:19:55]**
- **Consequência prática:** Reduz-se a necessidade de acompanhar manualmente múltiplos chats e terminais.
- **Ação recomendada:** Centralizar decisões, status, exceções e solicitações humanas em uma fila única.

### 12. Paralelismo precisa ser governado por dependências

- **Tese:** Disparar agentes em paralelo não basta; é preciso analisar o que é sequencial, o que é independente e o que pode conflitar.
- **Evidência/timestamp:** Pedro explica a lógica de dependências, DAG, execução sequencial e workers paralelos. **[modelo operacional — 02:35:20–02:37:04]**
- **Consequência prática:** Mais agentes podem reduzir tempo, mas somente quando as tarefas não competem pelos mesmos recursos.
- **Ação recomendada:** Antes de cada wave, listar dependências, arquivos lidos, arquivos alterados e pontos de sincronização.

### 13. Branches e worktrees devem ser escolhidas conforme o risco

- **Tese:** Não há uma configuração fixa: o sistema deve decidir entre branch única, branches separadas ou worktrees conforme complexidade e possibilidade de conflito.
- **Evidência/timestamp:** Pedro descreve diferentes estratégias e a análise prévia de arquivos tocados por cada story. **[recomendação operacional — 03:29:45–03:31:48]**
- **Consequência prática:** Evita-se pagar o custo de isolamento quando a tarefa é simples e reduz-se o risco de colisões em ondas complexas.
- **Ação recomendada:** Criar uma regra de preflight baseada em número de stories, arquivos compartilhados e necessidade de isolamento.

### 14. Quality assurance deve envolver mais de um motor

- **Tese:** O desenvolvimento precisa de revisão, validação e, quando possível, mecanismos de self-healing e múltiplos motores.
- **Evidência/timestamp:** Pedro afirma que todo story deve passar por QA obrigatório em mais de um motor e descreve o ciclo validate, develop, review, apply, fix, push, deploy, verify e close. **[modelo operacional — 02:03:25–02:05:25]**
- **Consequência prática:** A engine que produz uma alteração não é a única responsável por declarar que ela está correta.
- **Ação recomendada:** Separar executor e revisor e registrar os resultados de cada etapa.

### 15. Smoke tests não substituem testes reais

- **Tese:** Testes que apenas confirmam uma condição preparada pelo próprio sistema podem dar uma falsa sensação de sucesso.
- **Evidência/timestamp:** Pedro critica smoke tests usados como validação suficiente e recomenda spikes, testes reais, telemetria e métricas. **[crítica/recomendação — 01:44:45–01:46:19]**
- **Consequência prática:** Um agente pode “provar” uma implementação que funciona somente no cenário que ele mesmo construiu.
- **Ação recomendada:** Para cada entrega relevante, incluir pelo menos um teste de comportamento real e uma evidência observável de execução.

### 16. O ciclo de aprendizado deve partir dos runs

- **Tese:** Cada execução de uma skill deve gerar log; os logs devem ser digeridos em aprendizados avaliados e qualificados.
- **Evidência/timestamp:** Pedro descreve o encadeamento execução, log, digest, avaliação e qualificação do learning. **[modelo operacional — 02:06:50–02:09:09]**
- **Consequência prática:** Melhorias deixam de depender apenas de memória informal ou percepção subjetiva.
- **Ação recomendada:** Registrar cada run com entrada, decisão, resultado, falha, intervenção humana e aprendizado proposto.

### 17. A autonomia deve ser liberada por evidência

- **Tese:** Um gate humano só deve ser removido depois de medir quanto o humano corrige ou altera as decisões do agente.
- **Evidência/timestamp:** Pedro relata que registrou decisões entre validate e develop e só retiraria o gate após uma amostra de meses mostrar baixa taxa de mudança. **[recomendação — 04:29:51–04:31:00]**
- **Consequência prática:** A automação avança de forma gradual, baseada em comportamento observado, não em confiança abstrata.
- **Ação recomendada:** Criar um log de override humano e definir um limiar explícito para cada remoção de gate.

### 18. Heurísticas devem ser classificadas e encaminhadas

- **Tese:** Heurísticas de decisão, score, regras e governança têm funções diferentes e devem alimentar camadas diferentes do sistema.
- **Evidência/timestamp:** Pedro associa árvores de decisão às skills, scores aos quality gates, decisões aos agentes e regras aos mecanismos de governança. **[modelo conceitual — 03:48:05–03:51:12]**
- **Consequência prática:** Evita-se usar uma regra de qualidade como se fosse uma decisão de roteamento, ou uma decisão contextual como se fosse um axioma.
- **Ação recomendada:** Classificar cada heurística por finalidade e registrar onde ela será aplicada.

### 19. Heurísticas próprias precisam ser confrontadas

- **Tese:** Um sistema que contém somente as heurísticas do seu criador pode perpetuar tanto suas boas decisões quanto seus erros.
- **Evidência/timestamp:** Pedro alerta que agentes limitados ao contexto e às decisões de uma única pessoa ficam presos a esse universo e recomenda incorporar heurísticas externas. **[limite/recomendação — 04:31:51–04:32:52]**
- **Consequência prática:** A memória organizacional pode cristalizar uma decisão ruim e reproduzi-la indefinidamente.
- **Ação recomendada:** Incluir revisão externa, comparação entre especialistas ou research antes de consolidar uma heurística como regra.

## Playbook operacional de Pedro

### Escolha de modelos

1. **Escolher por atividade, não por marca.** Pedro diferencia os modelos por estilo de execução: Claude mais arquitetural, Codex mais direto e Grok mais orientado a resolver. **[00:48:28–00:49:30]**
2. **Usar roteamento.** A seleção deve ocorrer no nível da atividade, com possibilidade de delegação a outro terminal ou engine. **[01:12:28–01:13:12]**
3. **Considerar o perfil do operador.** Para uso mais direto, o Codex pode ser mais adequado; para explorar arquiteturas e ferramentas, Claude pode oferecer mais maleabilidade. **[04:24:08–04:27:16]**
4. **Não trocar por hype.** Adoção deve ser subordinada a entrega, qualidade e utilidade observadas. **[00:51:48–00:52:37]**
5. **Usar revisão cruzada.** Pedro relata usar o Codex como revisor do trabalho de outras LLMs. **[01:46:09–01:46:19]**

### Arquitetura independente de modelo

1. Separar processo, registros, skills e regras dos adapters de cada terminal. **[02:24:12–02:26:44]**
2. Criar uma camada de controle própria sobre as engines externas. **[02:28:43]**
3. Manter registry de engines separado da execução. **[03:20:33]**
4. Projetar eventos de spawn, wave e sessão como uma camada de comunicação controlável externamente. **[03:28:28]**
5. Tratar a ferramenta como infraestrutura de entrega, não como um chat específico. **[03:26:54–03:27:08]**

### Contexto e memória

1. Gerar SOT para registrar a fonte de verdade de um projeto ou de um recorte específico. **[01:31:39–01:32:04; 01:42:57–01:43:12]**
2. Produzir handoff ao fechar cada sessão. **[01:17:09–01:18:54]**
3. Preservar sessões complexas em estado pausado, sem mantê-las consumindo recursos. **[01:26:12–01:27:08]**
4. Manter transcripts, decisões, registros de learning e proveniência. **[02:02:39–02:05:25; 03:32:06–03:32:47]**
5. Tornar o aprendizado global quando ele for aplicável a vários projetos. **[02:08:09]**

### Decomposição e ciclos

1. Mapear entidade e ciclo de vida antes de criar a skill. **[03:00:39–03:02:27]**
2. Decompor o fluxo em etapas como validate, develop, review, fix, deploy, verify e close. **[02:05:01–02:05:25]**
3. Fazer cada skill avançar uma entidade em seu ciclo de vida. **[03:10:36–03:11:13]**
4. Transformar o full cycle em unidade reutilizável. **[02:54:30–02:56:03]**
5. Agrupar full cycles em waves, com registro, telemetria e aprendizado. **[02:55:37–02:56:29]**

### Orquestração multiagente

1. Usar uma sessão master para coordenar children e companions. **[01:18:54–01:19:55]**
2. Fazer análise de paralelismo antes do disparo. **[01:10:45–01:11:28]**
3. Separar executor, revisor, bloqueio, cascade e fan-in. **[03:18:24–03:18:52]**
4. Centralizar decisões pendentes em uma fila humana. **[01:11:28–01:12:06]**
5. Resolver branches, worktrees, conflitos e integração no fan-in. **[03:18:52–03:19:38; 03:29:45–03:31:48]**
6. Não presumir que um agente consiga orquestrar outros agentes de forma confiável; Pedro ressalta limitações de variação e de instanciação. **[03:44:25–03:45:11]**

### Gates humanos e métricas

1. Manter gates quando a pessoa ainda não entende o comportamento do sistema. **[03:38:38–03:38:59]**
2. Usar gates para decisões de close, deploy, merge e aprovação. **[01:11:28–01:12:06; 04:18:07]**
3. Registrar overrides humanos antes de remover gates. **[04:29:51–04:31:00]**
4. Medir scores, testes, telemetria e métricas reais. **[01:11:45–01:12:06; 01:44:45–01:46:19]**
5. Ajustar a quantidade de guardrails ao nível técnico do operador. **[04:15:08–04:16:30]**
6. Implementar compatibilidade automática apenas quando não houver risco de perda de sessão ou crash; caso contrário, falhar de forma segura. **[04:20:40]**

### Aprendizado e heurísticas

1. Transformar runs em logs e logs em learnings avaliados. **[02:06:50–02:07:14]**
2. Separar heurísticas para skills, quality gates, agentes e governança. **[03:48:05–03:51:12]**
3. Registrar decisões arquiteturais em ADRs e revisá-las conforme a centralidade da engine. **[04:05:08–04:06:15]**
4. Explicar uma decisão por vez, com contexto prático e exemplos não técnicos. **[04:06:15–04:07:14]**
5. Confrontar heurísticas internas com referências ou pessoas externas para evitar fechamento do sistema. **[04:31:51–04:32:52]**
6. Priorizar reuse, depois adapt e somente então create. **[03:07:20–03:08:23]**

### Design de ferramentas

1. Priorizar velocidade de interação, ausência de lag e familiaridade visual. **[01:09:44–01:10:03; 03:17:44–03:18:24]**
2. Separar daemon de terminais e interface Cockpit para preservar sessões entre reinícios. **[02:01:21–02:02:49]**
3. Usar uma interface única para controlar múltiplas sessões. **[01:19:16–01:19:55]**
4. Implementar fila de decisões em vez de deixar eventos de vários terminais “pipocando”. **[01:11:45–01:12:06]**
5. Começar com uma hipótese pequena e uma única ferramenta de leitura antes de construir uma infraestrutura ampla. **[03:52:25–03:53:41]**
6. Preferir o navegador interno quando ele for considerado mais rápido e confiável no contexto observado. **[04:03:35–04:03:39]**

## Alertas e limites

### Críticas de Pedro

- **Contra a engenharia de prompt como centro da disciplina:** ele a considera superestimada quando os modelos melhoram. **[02:57:56]**
- **Contra testar modelos indefinidamente:** o hype pode substituir a entrega. **[00:51:48–00:52:37]**
- **Contra smoke tests como prova suficiente:** são rápidos, mas podem validar uma construção artificial. **[01:44:45–01:46:19]**
- **Contra a automação sem governança:** paralelismo apenas disparado pode gerar conflitos em Git, arquivos e branches. **[01:10:45–01:11:28; 03:18:24–03:19:38]**
- **Contra tratar a IA como humana:** ela não possui, segundo Pedro, risco real ou *skin in the game*. **[01:37:47–01:38:36]**
- **Contra culpar a ferramenta:** decisões automatizadas continuam sendo responsabilidade de quem as tomou. **[04:10:40–04:12:01]**
- **Contra sistemas fechados nas próprias heurísticas:** uma decisão ruim registrada pode ser reproduzida repetidamente. **[04:31:51–04:32:52]**

### Riscos técnicos e operacionais relatados

- **Variabilidade dos modelos:** o mesmo input pode gerar outputs diferentes. **[02:20:16–02:20:46]**
- **Falsa aparência de conclusão:** Pedro relata que alguns modelos podem criar testes ou respostas que parecem comprovar uma execução sem comprovar o resultado real. **[01:44:25–01:46:19]**
- **Dependência de ambiente:** múltiplos terminais, Docker, contêineres e processos de sistema podem degradar o desempenho; ele cita varreduras de antivírus como possível fonte de lentidão. **[01:52:34–01:53:07]**
- **Limite de escala:** Pedro reconhece que uma execução muito grande pode travar ou perder desempenho. **[01:52:09–01:52:34]**
- **Cotas e falhas de API:** children podem concluir código e gates, mas travar perto do fim por limite de API. **[03:36:41–03:37:30]**
- **Conflitos de integração:** múltiplas worktrees podem alterar o mesmo arquivo e exigir resolução no fan-in. **[03:30:59–03:31:48; 03:37:30]**
- **Cobertura incompleta:** Pedro relata testes aprovados, mas também ressalva que a capacidade multi-engine ainda não estava completa e que alguns testes não exercitavam engines em produção. **[03:19:38]**
- **Incompatibilidade entre formatos:** skills e agentes podem exigir adaptações específicas entre ambientes, como Markdown, extensões ou TOML. **[01:41:11–01:41:47]**
- **Excesso de testes:** IA pode testar elementos óbvios ou aplicar CI/CD de forma desnecessária, consumindo tempo e tokens. **[03:22:10–03:23:16]**
- **Autonomia prematura:** Pedro recomenda não deixar o sistema controlar aquilo que o operador ainda não compreende. **[03:38:38–03:38:59]**

### Condições de validade

As ideias deixam de funcionar ou exigem adaptação quando:

1. O processo não foi mapeado e as entidades, dependências e critérios continuam ambíguos. **[01:36:12–01:37:35]**
2. A tarefa exige determinismo, mas é deixada para interpretação livre da LLM. **[02:20:46–02:24:12]**
3. Há mais sessões paralelas do que a infraestrutura consegue sustentar. **[01:52:34–01:53:07]**
4. O sistema não registra handoffs, decisões, logs e artefatos. **[01:17:09–01:18:54; 03:11:38]**
5. O gate é removido sem amostra real de decisões humanas e overrides. **[04:29:51–04:31:00]**
6. O operador não conhece suas próprias limitações nem instala guardrails compatíveis com elas. **[04:15:08–04:16:30]**
7. A solução depende de uma única engine ou de recursos específicos de uma interface. **[02:24:12–02:28:43]**

## Plano de aplicação em 7 dias

### Dia 1 — Escolher um processo pequeno

1. Selecionar uma única entidade ou fluxo recorrente, com começo, fim e resultado observável.
2. Registrar suas etapas, entradas, saídas, decisões e pontos de espera.
   **Critério de teste:** outra pessoa consegue descrever o fluxo sem perguntar o que cada etapa significa. **[01:36:12–01:37:35]**

### Dia 2 — Separar determinismo de interpretação

3. Classificar cada etapa como: regra/código, interpretação de linguagem ou decisão humana.
4. Retirar da LLM pelo menos uma decisão que possa ser feita por regra, score ou árvore.
   **Critério de teste:** executar a mesma entrada duas vezes e verificar se a parte determinística permanece igual. **[02:20:46–02:24:12]**

### Dia 3 — Criar uma skill mínima

5. Implementar uma skill para uma única transição do processo, com entrada, saída e status explícitos.
6. Registrar o resultado de cada execução em um log.
   **Critério de teste:** três execuções produzem registros comparáveis e permitem identificar falhas. **[03:10:36–03:11:13; 02:06:50–02:07:14]**

### Dia 4 — Criar contexto durável

7. Gerar uma SOT curta e um handoff contendo decisões, artefatos, pendências e próximo passo.
   **Critério de teste:** interromper a sessão e retomá-la usando apenas esses registros. **[01:31:39–01:32:04; 01:17:09–01:18:54]**

### Dia 5 — Testar roteamento e revisão

8. Executar a mesma atividade com dois modelos ou dois modos de execução e comparar qualidade, velocidade e falhas.
9. Fazer uma engine revisar o resultado da outra, sem aceitar apenas um smoke test.
   **Critério de teste:** registrar diferenças concretas e escolher o encaminhamento por evidência. **[01:12:28–01:13:12; 01:46:09–01:46:19]**

### Dia 6 — Adicionar um gate humano

10. Criar um gate de aprovação antes da etapa de maior risco e registrar todas as alterações feitas pelo humano.
    **Critério de teste:** produzir uma pequena amostra de decisões e medir a taxa de override. **[04:29:51–04:31:00]**

### Dia 7 — Avaliar automação

- Consolidar logs, falhas, overrides, duração e qualidade.
- Decidir se o fluxo deve permanecer manual, ganhar um novo guardrail ou avançar para execução parcial.
- Não remover o gate apenas porque algumas execuções funcionaram; exigir evidência acumulada. **[03:38:38–03:38:59; 04:29:51–04:31:00]**

## Índice por tema

| Tema | Timestamps principais |
|---|---|
| Modelos e diferenças de uso | 00:48:28–00:49:30; 04:24:08–04:27:16 |
| Fim do prompt engineering | 00:49:52–00:50:22; 02:57:56 |
| Metodologia e processos | 00:50:22–00:50:42; 01:36:12–01:37:47; 02:34:38–02:35:20 |
| Independência de modelo | 00:54:16–00:54:58; 02:24:12–02:28:43 |
| SOT, contexto e memória | 01:17:09–01:19:16; 01:26:12–01:27:08; 01:31:39–01:32:04 |
| Skills e agentes | 03:10:36–03:11:13; 03:48:05–03:48:37 |
| Ciclo de desenvolvimento | 02:03:25–02:06:16; 02:54:30–02:56:29 |
| Waves e paralelismo | 01:10:45–01:11:28; 02:35:20–02:37:04; 03:18:24–03:19:38 |
| Branches, worktrees e conflitos | 03:29:45–03:31:48; 03:36:41–03:37:30 |
| Gates e autoridade humana | 01:11:28–01:12:06; 03:32:06–03:32:47; 04:18:07 |
| Testes, QA e telemetria | 01:44:45–01:46:19; 02:03:25–02:05:25; 03:19:38 |
| Learning e digestão | 02:06:50–02:09:09; 03:01:55–03:02:27 |
| Heurísticas | 03:48:05–03:51:12; 04:31:51–04:32:52 |
| Responsabilidade humana | 01:37:47–01:38:36; 04:10:40–04:12:01 |
| Limitações da IA | 02:20:16–02:21:30; 04:46:39–04:47:30 |
| Desempenho e infraestrutura | 01:09:44–01:10:03; 01:52:34–01:53:07 |
| Sobrevivência de sessões | 02:01:21–02:02:49; 03:16:30–03:17:24 |
| Roteamento e adapters | 01:12:28–01:13:12; 02:25:10–02:26:44; 04:27:11–04:27:16 |
| Decisões e ADRs | 03:00:39–03:05:41; 04:05:08–04:07:14 |
| Reuse, adapt, create | 03:07:20–03:09:56 |
| Remoção gradual de gates | 04:29:51–04:31:00 |
