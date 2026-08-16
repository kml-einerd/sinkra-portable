# Contrato do grafo de nós v1

## Sumário

1. Topologia
2. Classes e tipos
3. Definições e candidatos
4. Composições e bindings
5. Runtime e evidência
6. Relações
7. Promoção e decisão
8. Invariantes

## 1. Topologia

Registry canônico do projeto:

```text
sinkra-work/registry/nodes/
├── registry.jsonl
├── relations.jsonl
├── objects/<object-id>/vN.md
└── audit/promotions.jsonl
```

Estado do projeto consumidor:

```text
sinkra-work/node-graph/
├── candidates/*.md
├── compositions/*.md
├── runtime/*.json
├── evidence/*.md
├── relations.jsonl
├── promotion-plan.json
└── review-report.md
```

Manter um único Registry por projeto e fixar referências como `NODE-...@N` nas
composições. Para reuso entre projetos, apontar `--registry` para um caminho
compartilhado explicitamente autorizado; não copiar ou mesclar registries de
forma silenciosa.

## 2. Classes e tipos

| `object_class` | Tipos principais | Regra |
|---|---|---|
| `definition` | `entity`, `stage`, `task`, `rule`, `heuristic`, `process`, `template`, `artifact` | Núcleo reutilizável e sem contexto de uma composição |
| `composition` | `lifecycle`, `workflow`, `full-cycle`, `bundle` | Ordem, papel, condição e parâmetros por binding |
| `runtime` | `entity-instance`, `cycle-run`, `task-run`, `stage-event`, `artifact-instance` | Ocorrência histórica; nunca reutilizável |
| `evidence` | `source`, `excerpt`, `media`, `report` | Prova imutável e localizável |

Não usar `cycle` como tipo. Normalizar para `lifecycle`, `full-cycle` ou `cycle-run`. Não usar `verification` como tipo: usar `kind: task` com `capabilities: ["verification"]`.

## 3. Definições e candidatos

Usar Markdown com frontmatter JSON válido entre delimitadores `---`. JSON também é YAML válido e dispensa parser YAML no CLI.

```markdown
---
{
  "schema": "sinkra-node@1",
  "object_id": "NODE-TASK-<uuid4>",
  "object_class": "definition",
  "kind": "task",
  "name": "Validar completude",
  "version": 1,
  "status": "stable",
  "aliases": [],
  "capabilities": ["verification"],
  "reuse_policy": "reusable",
  "contract": {
    "verb": "validar",
    "executor": "worker",
    "inputs": [],
    "outputs": [],
    "preconditions": [],
    "completion": []
  },
  "constraints": [],
  "provenance": []
}
---

Descrição humana opcional.
```

Candidato troca `schema`, `object_id`, `version` e `status` por:

```json
{
  "schema": "sinkra-node-candidate@1",
  "candidate_id": "CAND-TASK-0001",
  "status": "candidate"
}
```

Campos de contexto como `parent`, `order`, `position`, `role`, `when` e `params` são proibidos na definição. O hash SHA-256 cobre o arquivo inteiro e fica somente em `registry.jsonl`, evitando hash circular. Versões são imutáveis em `objects/<object-id>/vN.md`.

## 4. Composições e bindings

Composição local usa `schema: sinkra-composition@1`, ID, tipo, versão, status e bindings. Um binding mínimo:

```json
{
  "ref": "NODE-TASK-<uuid>@1",
  "role": "quality-check",
  "when": {
    "condition": "informação obrigatória ausente",
    "evaluator": "worker"
  },
  "params": {
    "severity": "blocker"
  }
}
```

- condição intrínseca: `contract` da definição;
- adaptação contextual: `when` e `params` do binding;
- correção permanente: nova versão com relação `supersedes`;
- ocorrência ou exceção: runtime mais evidência.

Uma `TaskDefinition` pode participar de vários fluxos por bindings diferentes sem cópia. Uma `StageDefinition` deve participar de ao menos um `lifecycle`, por binding ou relação constitutiva `belongs-to`.

## 5. Runtime e evidência

Runtime usa JSON com `schema: sinkra-runtime@1`, `runtime_id`, `object_class: runtime`, `kind`, `definition_ref`, `status`, `recorded_at` e `evidence_refs`. `TaskRun` nunca é reutilizável nem promovível.

Evidência usa Markdown/JSON com `schema: sinkra-evidence@1`, `evidence_id`, `kind`, `source`, `locator`, `captured_at` e `sha256` quando houver arquivo. A evidência não muda para sustentar uma conclusão posterior; criar outra evidência.

Materiais devem ser classificados como:

- `source` ou `evidence`: entrada e prova;
- `template`: definição reutilizável;
- `artifact`: definição do entregável;
- `artifact-instance`: material produzido em runtime.

## 6. Relações

Usar uma relação JSON por linha em `relations.jsonl`:

```json
{"schema":"sinkra-relation@1","relation_id":"REL-<uuid4>","from_ref":"NODE-STAGE-<uuid>@1","type":"belongs-to","to_ref":"COMP-LIFECYCLE-<uuid>@1","scope":"constitutive","provenance":[]}
```

`scope` aceita:

- `constitutive`: sem a relação, o significado estrutural fica incompleto;
- `semantic`: associação útil, mas não formadora da identidade.

Ordem, papel e condição ficam no manifesto da composição. Estado da execução fica no runtime. Não criar camada genérica de anotações.

## 7. Promoção e decisão

Plano:

```json
{
  "schema": "sinkra-promotion-plan@1",
  "source_bundle": "sinkra-work/node-graph",
  "source_kind": "as-is",
  "items": [
    {"candidate_id": "CAND-TASK-0001", "action": "promote-new", "reason": "contrato completo"},
    {"candidate_id": "CAND-RULE-0002", "action": "hold", "reason": "sem validação"}
  ],
  "relations": []
}
```

Decisão:

```json
{
  "schema": "sinkra-promotion-decision@1",
  "plan_sha256": "<sha256-do-plano>",
  "status": "approved",
  "approved_items": ["CAND-TASK-0001"],
  "decided_by": "Nome humano",
  "decided_at": "2026-08-02T12:00:00Z"
}
```

Ações aceitas: `promote-new`, `promote-version`, `hold`, `archive`. `promote-version` exige `target_object_id`; o CLI cria `vN+1` e registra `supersedes`. Itens não aprovados não são promovidos. Ideias, blockers e tasks de WhatsApp ficam em `hold`, salvo aprovação nominal explícita.

## 8. Invariantes

1. Validar todo o plano antes de escrever; `--dry-run` não altera arquivos.
2. Usar UUID4, SHA-256, lock por diretório, arquivo temporário e `os.replace`.
3. Não apagar, renomear nem sobrescrever versões existentes.
4. Resolver versão fixada exatamente; ID sem versão lista versões disponíveis.
5. Cancelar composição ou run preserva definições, versões, evidências e histórico.
6. Reportar `unreferenced`, órfão, hash divergente e referência quebrada sem correção automática.
7. Validar refs canônicas do bundle com `validate <bundle> --registry <registry>`; sem Registry, não assumir que a ref existe.
