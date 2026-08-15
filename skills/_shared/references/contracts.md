# Contratos operacionais

## Task

```yaml
task:
  id:
  verb:
  entity:
  from_stage:
  executor:
  reviewer:
  accountable:
  inputs: []
  instructions: []
  outputs: []
  acceptance_criteria: []
  expected_duration:
  next_consumer:
  failure_modes: []
```

Usar um verbo principal, um executor principal, inputs identificáveis e output
verificável. Para cada input declarar fonte, formato/schema, versão,
obrigatoriedade e tratamento quando ausente. Para cada output declarar destino,
formato/schema, proveniência e próximo consumidor. Estados mínimos: a fazer,
fazendo, concluída, bloqueada, aguardando informação, falhou, cancelada e não
aplicável.

## Decisão

```yaml
decision:
  id:
  decision_set_id:
  sequence:
  total:
  status:
  entity:
  question:
  user_mastery:
  primary_authority:
  options: []
  agent_recommendation:
  selected_option:
  rationale:
  accepted_risks: []
  constraints: []
  unresolved_questions: []
  evidence: []
  sources: []
  captured_at:
  decided_by:
  decided_at:
  ratified_by:
  ratified_at:
  next_consumer:
```

Estados mínimos: `proposed`, `selected`, `deferred`, `ratified` e
`superseded`. Opções propostas não limitam a decisão: combinação ou alternativa
do decisor deve ser persistida em `selected_option`. Toda decisão registra
fontes consumidas e momento de captura.

## Gate

```yaml
gate:
  entity:
  from_stage:
  to_stage:
  required_tasks: []
  acceptance_criteria: []
  automatic_checks: []
  human_decision:
  blockers: []
  warnings: []
  decision_owner:
  evidence: []
  outcome:
```

Resultados: `approved`, `rejected`, `blocked`, `needs-information` ou
`cancelled`. Checks automáticos rodam antes da decisão humana; blocker aberto
nunca vira `approved`. Executor não deve autoaprovar o próprio output quando o
risco pede autoridade separada.

## Handoff

```yaml
handoff:
  entity:
  current_state:
  objective:
  consumed_inputs: []
  excluded_sources: []
  produced_outputs: []
  decisions: []
  blockers: []
  revalidate: []
  next_action:
  next_owner:
  resume_from:
```

Estas projeções legíveis são os contratos portáteis. A skill preenche conteúdo,
fontes e referências e persiste o resultado em `sinkra-work/`.
