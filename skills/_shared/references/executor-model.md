# Modelo de executores

## Árvore de decisão

```text
exige intenção, assinatura, risco ou exceção?
→ Humano

é calculável, repetível e testável por regra?
→ Worker

exige interpretação contextual dentro de fontes e método?
→ Agente

mistura naturezas?
→ decompor ou declarar handoffs
```

Executor, reviewer, accountable e dono do gate são responsabilidades
independentes.

## Worker

Contratar por:

- transformação determinística;
- inputs, schema e limites;
- comando ou interface;
- outputs e códigos de falha;
- teste e idempotência;
- observabilidade e rollback.

Não usar Worker para ambiguidade ainda não modelada.

## Agente

Contratar por:

- objetivo e entidade;
- escopo de decisão;
- fontes e ferramentas permitidas;
- método e restrições;
- inputs e outputs;
- critérios de aceite;
- escalonamento e handoff.

Persona não substitui processo. Criar Agente somente quando uma task exige
competência contextual que não cabe em regra determinística.

## Topologia

Preencher a maior fronteira segura com Agentes quando houver especialização,
hipóteses distintas ou trabalho independente. Cada sessão precisa produzir
avanço ou opção comparável; contagem sem propósito não é paralelismo. Declarar
owner do fan-in, output comum e gate.

## Supervisor

O chat principal mantém intenção, backlog, decisões e fan-in. Workers recebem
somente um contrato delimitado. Quando o runtime puder abrir sessões:

1. propor uma Wave com objetivo, motivo, papéis, CLI, escopos, acesso,
   entregáveis, aceite e término;
2. obter uma aprovação humana para a onda inteira;
3. abrir e acompanhar as sessões sem usar o humano como mensageiro;
4. permitir um writer por árvore; paralelizar leitura ou diretórios isolados;
5. exigir reports de progresso/espera/conclusão e mostrar o monitor;
6. fazer fan-in, humano escolher e executor fechar o handoff.

Tudo que está pronto e independente entra na Wave até o limite configurado.
Tudo que depende do fan-in permanece fora até a escolha ser registrada.
