# Persistência e aprendizagem

## Bundle de execução

Cada execução deve deixar:

- estado atual;
- outputs e seus destinos;
- decisões e proveniência;
- tasks concluídas, bloqueadas e não aplicáveis;
- gate e evidências;
- próximo consumidor;
- evento de Journey Log.

Persistir em `sinkra-work/` conforme
[runtime-and-persistence.md](runtime-and-persistence.md).

## Journey Log

```yaml
event:
  run_id:
  entity:
  transition:
  task:
  executor:
  sources: []
  decision_refs: []
  output_refs: []
  gate_outcome:
  corrections: []
  occurred_at:
```

Adicionar cada evento a `sinkra-work/journey.yaml`, preservando os anteriores.

## Calibrar autonomia

Medir runs, propostas, overrides, tipos de erro, impacto e reversibilidade.
Somente então recomendar:

- manter gate;
- amostrar parte das execuções;
- remover gate para uma transição específica;
- restaurar gate.

Esta versão registra evidência, mas não implementa engine automática de
learning ou confiança.
