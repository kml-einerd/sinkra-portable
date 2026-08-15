# Task 06 — Contratar a construção

## Objetivo

Converter a decisão em trabalho delimitado e verificável.

## Executar

1. Definir estado atual e estado alvo.
2. Declarar escopo e não-objetivos.
3. Decompor em tasks com um verbo e um output principal.
4. Escolher Humano, Worker ou Agente por natureza do trabalho.
5. Definir inputs, outputs, consumers, dependências e ordem.
6. Definir critérios, blockers, warnings e dono de cada gate.
7. Definir persistência, falhas, retry e resume.
8. Preencher
   [construction-contract.yaml](../../_shared/templates/construction-contract.yaml).
9. Separar a maior fronteira segura em Wave: tudo que está pronto e
   independente entra; dependências aguardam o fan-in.
10. Para cada sessão declarar objetivo, motivo, CLI/comando, acesso, cwd ou
    worktree, entregável, aceite, report e encerramento.

## Aceitar

Outro executor consegue iniciar a primeira task sem reconstruir a conversa e
consegue verificar quando a transição terminou.
