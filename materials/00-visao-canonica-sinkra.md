# Visão canônica do Sínkra

> Status: explicação atual da visão. Os contratos executáveis permanecem em
> `skills/` e `skills/_shared/`.

## Em uma frase

O Sínkra transforma intenção e conhecimento disperso em processos executáveis,
rastreáveis e melhoráveis, começando pelas entidades e transições do negócio —
não pelos agentes ou ferramentas disponíveis.

## Gramática central

```text
entidade
→ lifecycle
→ stage atual
→ task de transformação
→ output verificável
→ gate
→ próximo stage
→ Journey Log e aprendizado
```

- **Entidade:** objeto com identidade, estado, relações e ciclo de vida.
- **Lifecycle:** caminho completo de nascimento, evolução e encerramento.
- **Stage:** condição reconhecível da entidade em determinado momento.
- **Task:** transformação atômica com input, executor, output e aceite.
- **Gate:** autoridade que libera, bloqueia ou pede informação para a transição.

Checklist verifica. Acceptance criterion prova. Gate autoriza. Nenhum deles é
sinônimo do outro.

## Ciclo do método

1. Reconstruir o AS-IS sem corrigir a história.
2. Resolver gaps e decisões com autoridade e evidência explícitas.
3. Desenhar TO-BE somente depois do AS-IS validado.
4. Contratar Humano, Worker ou Agente para cada task.
5. Forjar transições recorrentes como skills e aprender pelos runs.

Quando houver potencial de reuso entre fluxos, extrair nós somente depois do
AS-IS. Separar definição reutilizável, composição contextual, ocorrência de
runtime e evidência.

## Escolha de executor

| Executor | Usar quando | Não delegar sozinho |
|---|---|---|
| Humano | responsabilidade, exceção, risco, autoria ou relação | repetição mecânica evitável |
| Worker | regra determinística, cálculo, validação ou integração | interpretação ambígua |
| Agente | linguagem, pesquisa, síntese ou decisão contextual | aprovação crítica do próprio output |

Executor, reviewer, accountable e dono do gate são papéis diferentes, mesmo
quando uma pessoa acumula mais de um em tarefas de baixo risco.

## Verdade e decisão

Classificar afirmações como observadas, declaradas, inferidas, propostas, gaps
ou conflitos. Perguntar se o humano domina o tema antes de escolhê-lo como
fonte primária. Quando não domina, pesquisar fontes adequadas e explicar pelas
consequências práticas.

Levar uma decisão por turno. As opções devem ser reais e não têm cardinalidade
fixa; o decisor pode combinar caminhos ou criar outro. Recomendação do agente e
decisão humana permanecem separadas. Executar somente após a ratificação exigida
pelo risco e pelo contrato.

## Reuso e composição

Aplicar `reuse > adapt > create`:

1. procurar definição, template, skill ou relação existente;
2. adaptar por binding, parâmetros ou nova versão quando necessário;
3. criar somente quando o Registry e o projeto não contiverem solução válida.

Ordem, papel e condição pertencem à composição. O núcleo reutilizável não deve
carregar contexto de uma única execução. Runtime e evidência nunca viram
definições reutilizáveis.

## Persistência e continuidade

Conversa não é memória operacional. Cada unidade relevante atualiza
`sinkra-work/` com estado, decisões, evidências, gates, outputs, runs, Journey
Log e handoff. Outra IA deve continuar pelo último `next_action` sem depender do
histórico do chat.

Revalidar arquivos, decisões, ferramentas e regras externas ao retomar. Não
reescrever uma versão anterior silenciosamente; registrar drift, substituição e
motivo.

## Aprendizado e autonomia

Cada run produz evidência sobre uma transição específica. Aprendizado útil tem
fonte, contexto, resultado e consequência operacional. Remover intervenção
humana somente quando amostra, taxa de correção e risco justificarem; não
generalizar confiança de uma skill para outra.

## O que o Sínkra não é

- um prompt gigante carregado em todas as conversas;
- um conjunto de agentes soltos procurando trabalho;
- documentação TO-BE apresentada como realidade atual;
- automação que esconde ausência de autoridade ou evidência;
- o Harness: o Harness é uma implementação possível de enforcement mecânico.

## Resultado esperado

Um sistema Sínkra bem formado permite localizar a entidade, entender seu estado,
ver qual task a move, saber quem executa e quem autoriza, encontrar o output e a
evidência e retomar a próxima ação sem reconstruir o contexto.
