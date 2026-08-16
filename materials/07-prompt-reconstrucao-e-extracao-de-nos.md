# Prompt — Reconstrução AS-IS e extração de nós candidatos

## Preencha somente este bloco

```yaml
modo: "LEGADO_OPERACIONAL | HISTORICO_WHATSAPP"
objetivo: "<o que preciso reconstruir ou recuperar>"
fontes: "<arquivos, pastas, exportações ou links locais>"
escopo: "<empresa, sistema, projeto, processo ou período>"
restricoes: "<o que não deve ser alterado, inferido ou implementado>"
```

## Missão

Leia integralmente `AGENTS.md` e preserve o estado existente do projeto. Se o
Sínkra Harness estiver instalado, retome seu fluxo governado; não atualize nem
reinstale o Harness sem solicitação.

Ative `sinkra-mapear-processo` para reconstruir o AS-IS. Use
`sinkra-arquitetar-sistema` somente depois do gate AS-IS e apenas se o escopo
autorizar desenho TO-BE. Execute a skill pela sintaxe nativa deste CLI ou leia e
siga seu `SKILL.md` quando invocação direta não estiver disponível.

Transforme materiais dispersos, antigos ou contraditórios em um modelo
rastreável. Identifique o que existe, como funciona, quais elementos participam,
quais condições controlam o fluxo, como os elementos se ligam e onde há herança,
override, exceção, conflito ou lacuna.

Não organize por cortes arbitrários de arquivo ou janela de contexto. Os chunks
são apenas unidades temporárias de leitura. Reconstrua unidades semânticas
completas e gere **nós candidatos**: a menor unidade que continua compreensível,
referenciável, versionável e reutilizável fora da fonte original.

## Regras de verdade

1. Preserve a fonte original e registre arquivo, mensagem, autor, data, página,
   linha ou intervalo sempre que estiver disponível.
2. Classifique cada afirmação como `observado`, `declarado`, `inferido`,
   `proposto` ou `desconhecido`; não transforme inferência em fato.
3. Normalize a representação, não a história: preserve o termo original como
   alias quando adotar um nome canônico.
4. Não misture AS-IS com melhoria. Guarde correções e otimizações em
   `to_be_candidates`.
5. Não atribua IDs definitivos do futuro registry. Use IDs provisórios estáveis
   no formato `CAND-<TIPO>-<sequência>` e produza um mapa de equivalências para
   duplicatas ou aliases.

## Modelo a reconstruir

Mapeie, quando existirem evidências: sistemas e entidades; lifecycles, stages e
transições; eventos, condições e guards; processos e tasks; atores e executores;
entradas, saídas e artefatos; decisões, exceções, loops, dependências e heranças.

Separe identidade de composição:

- o nó candidato guarda significado, tipo, contrato, restrições e proveniência;
- relações ficam no registro externo de arestas;
- ordem, papel, projeto, pai e configuração ficam em manifests de composição;
- a mesma unidade não deve ser copiada para aparecer em duas composições;
- fonte ou trecho bruto nunca substitui um nó semântico reconstruído.

## Contrato de um nó candidato

Crie um arquivo Markdown com YAML para cada candidato:

```yaml
---
candidate_id: CAND-RULE-0001
kind: entity | rule | condition | process | task | idea | decision | artifact | heuristic
name: "<nome canônico>"
status: candidate
source_terms: ["<termos originais>"]
definition: "<significado completo e independente>"
contract:
  inputs: []
  outputs: []
  preconditions: []
  completion: []
constraints: []
provenance:
  - source: "<fonte>"
    locator: "<página, linha, mensagem ou intervalo>"
    authority: observed | declared | inferred | proposed | unknown
confidence: high | medium | low
open_gaps: []
---
```

Se um campo não se aplicar, deixe uma lista vazia. Se deveria existir mas não
foi encontrado, registre em `open_gaps`; não complete por imaginação.

## Ajuste por modo

### `LEGADO_OPERACIONAL`

Reconstrua o fluxo real antes de recomendar qualquer ajuste. Dê prioridade a
entidades, estados, transições, guards, entradas, saídas, artefatos, executores,
relações e heranças. Quando documentos divergirem, preserve as variantes e
indique qual possui maior autoridade e por quê.

### `HISTORICO_WHATSAPP`

Leia mensagens anteriores e posteriores para recuperar o contexto. Classifique
cada achado como `idea`, `task_candidate`, `confirmed_task`, `decision`,
`question` ou `blocker`.

Uma conversa, desejo ou sugestão não vira task confirmada sem evidência de
compromisso. Toda task precisa de verbo, resultado esperado, input, output,
executor quando conhecido e critério de conclusão. Campos ausentes viram gaps.
Una repetições sem perder autores, datas, mudanças de entendimento ou referências
de origem.

## Fluxo de trabalho

1. Inventarie fontes, formatos, períodos, lacunas e autoridade.
2. Reconstrua o AS-IS e valide internamente consistência, conflitos e exceções.
3. Extraia e deduplique os nós candidatos atravessando fronteiras de chunks.
4. Registre arestas tipadas e manifests candidatos sem embutir composição nos nós.
5. Audite cobertura, rastreabilidade e informação ausente antes do handoff.

Faça perguntas somente quando uma resposta humana mudar materialmente a
interpretação. Caso contrário, avance e registre a incerteza.

## Saída obrigatória

Grave tudo em uma pasta nova e isolada dentro do projeto, sem alterar as fontes:

```text
<output>/
├── 00-inventario-e-proveniencia.md
├── 01-modelo-as-is.md
├── node-candidates/
├── graph/
│   ├── edges.yaml
│   └── composition-candidates/
└── 99-gaps-e-handoff.md
```

O handoff deve informar: cobertura processada; quantidades por tipo; conflitos
não resolvidos; gaps que impedem promoção; e quais candidatos estão prontos para
receber `object_id`, versão e hash no registry definitivo.

Não implemente o TO-BE, não altere operações e não promova candidatos para nós
canônicos sem autorização. Primeiro entregue o modelo para revisão.
