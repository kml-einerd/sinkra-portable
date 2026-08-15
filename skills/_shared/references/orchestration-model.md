# Modelo de orquestração

## Responsabilidades

| Componente | Responsabilidade |
|---|---|
| `SKILL.md` | estado, rota, ordem, condições, gates e handoff |
| task | uma transformação atômica |
| checklist | verificações executadas |
| acceptance criterion | prova observável da qualidade do output |
| gate | autorização ou bloqueio da transição |
| referência | conhecimento carregado sob demanda |
| Worker | regra ou código determinístico |
| Agente | interpretação contextual dentro do método |
| Humano | intenção, risco, exceção e responsabilidade |

## Rotas

- **Fixa:** todas as tasks são obrigatórias e executadas em ordem.
- **Condicional:** o contexto escolhe um subconjunto; registrar tasks não
  aplicáveis.
- **Paralela:** tasks independentes compartilham o mesmo snapshot de contexto e
  convergem em um fan-in com owner.

## Waves e manifestação

Uma Wave ocupa a maior fronteira segura: todas as tasks já decididas, prontas e
independentes que cabem no limite configurado. Não reduzir a topologia para
economizar sessões quando existe avanço real; não aumentar a contagem com
trabalho duplicado.

Em modo de implementação, definição aceita deve produzir manifestação
inspecionável — mock, protótipo, diff, exemplo executável ou artefato do
processo — antes da próxima decisão dependente. Quando houver hipóteses reais,
materializá-las em paralelo com contrato comum de comparação. Writers usam
árvores isoladas; leitura pode compartilhar o mesmo snapshot.

O fan-in compara evidências, promove o que foi aceito e marca os demais
resultados como rejeitados. Não apagar evidência sem autorização explícita.

## Estado durável

Resolver primeiro a
[persistência portátil](runtime-and-persistence.md). Persistir após cada task
este checkpoint semântico em `sinkra-work/runs/`:

```yaml
run:
  id:
  entity:
  current_stage:
  completed_tasks: []
  skipped_tasks: []
  blockers: []
  decisions: []
  outputs: []
  next_task:
  updated_at:
```

Ao retomar, revalidar arquivos, decisões, ferramentas e regras externas que
podem ter mudado.

## Falhas

- governança, segurança ou integridade: bloquear;
- informação obrigatória ausente: `needs-information`;
- falha transitória: retry limitado e idempotente;
- telemetria opcional: registrar warning sem falsificar sucesso;
- conflito: preservar versões e escalar ao dono do gate.
