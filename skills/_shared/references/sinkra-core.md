# Núcleo Sínkra

## Fórmula

> Tasks, dentro de stages, movem entidades pelo lifecycle.

| Objeto | Função | Não confundir com |
|---|---|---|
| Entidade | objeto com identidade, nascimento, estados e morte | documento ou departamento |
| Lifecycle | trajetória completa da entidade | checklist |
| Stage | estado da entidade | status de uma task |
| Transição | mudança delimitada entre stages | projeto inteiro |
| Task | transformação atômica com input e output | intenção ampla |
| Skill | orquestra tasks, gates, persistência e handoff | Agente |
| Full cycle | compõe transições já estabilizadas | primeira versão de uma skill |

## Níveis

| Nível | Pergunta | Função |
|---|---|---|
| Estratégico | Quem somos e para quem? | contexto duradouro |
| Tático | O que entregamos agora? | orquestração da demanda |
| Operacional | Como produzimos? | execução |

Nível não é stage nem organograma. Uma entidade possui nível principal; suas
relações e seu contexto podem atravessar níveis.

## Relação, Herança e Spawn

- **Relação:** conecta entidades sem copiar identidade.
- **Herança:** propaga contexto segundo fonte, precedência e atualização.
- **Spawn:** cria entidade filha após evento ou gate.

Ao usar Herança ou Spawn, declarar origem, momento, campos, idempotência,
precedência, rollback e Journey Log.

## Nós e recomposição

Quando houver reuso entre fluxos, separar:

- **definição:** núcleo versionável e reutilizável;
- **composição:** ordem, papel, condição e parâmetros do binding;
- **runtime:** ocorrência histórica, nunca promovível como definição;
- **evidência:** prova imutável e localizável.

Chunk é fronteira de leitura, não fronteira semântica. Extrair nós somente de
um AS-IS rastreável e promover somente após decisão humana explícita.

## Princípios

- partir da entidade e da transição, não do Agente;
- preservar AS-IS antes de desenhar TO-BE;
- transformar output atual em input rastreável do próximo consumidor;
- registrar falta de informação em vez de inventar;
- aplicar `reuse > adapt > create`;
- reduzir caminhos errados com restrições, checklists e gates;
- retirar gate humano somente por evidência acumulada.
