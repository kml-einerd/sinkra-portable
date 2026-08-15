# Task 01 — Resolver contexto

## Objetivo

Definir o objeto, o estado atual, a transição desejada e se ainda existe uma
decisão humana necessária, sem repetir perguntas respondidas pelo workspace.

## Executar

1. Capturar o resultado pretendido e a execução que precisa ser destravada.
2. Inventariar artefatos, decisões, regras e outputs existentes.
3. Separar fonte elegível, excluída, conflitante e ausente.
4. Aplicar `reuse > adapt > create` antes de propor decisão ou artefato novo.
5. Classificar cada pendência como `resolvida`, `não bloqueante`, `pesquisa`,
   `decisão humana` ou `conflito`.
6. Excluir da elicitação itens resolvidos e não bloqueantes, preservando sua
   proveniência e sequência de execução.
7. Decompor somente os gaps humanos em decisões atômicas e ordená-las por
   dependência.
8. Manter somente uma decisão ativa por turno.
9. Identificar risco, reversibilidade, prazo e dono do gate.
10. Calibrar profundidade de leitura por novidade, centralidade e risco; ler a
   fonte completa quando qualquer um deles for alto.
11. Persistir contexto, fontes e pendências em `sinkra-work/`.

## Aceitar

- objeto e transição estão nomeados;
- cada pergunta de decisão admite alternativas comparáveis;
- fatos, interpretações, gaps e conflitos estão separados;
- fontes excluídas possuem motivo;
- somente gaps irredutíveis viraram perguntas humanas;
- nenhuma decisão válida foi reaberta nem artefato criado por quota;
- nenhum contexto recuperável será perguntado novamente.
