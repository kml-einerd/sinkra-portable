# Sínkra Portable

Usar este pacote como camada metodológica. Partir da entidade e da transição;
Agentes, Workers e Humanos são executores contratados pelas tasks.

## Inicialização obrigatória

1. Ler `skills/_shared/references/sinkra-core.md`.
2. Localizar ou criar `sinkra-work/state.yaml` no projeto atendido.
3. Ler o último handoff e revalidar arquivos, decisões e blockers.
4. Escolher uma skill pela tabela abaixo e ler integralmente seu `SKILL.md`.
5. Carregar somente as tasks, checklists e referências pedidas pela skill.

## Roteamento

| Pedido | Skill |
|---|---|
| Arquitetar projeto, processo ou sistema completo | `sinkra-arquitetar-sistema` |
| Reconstruir e validar somente o AS-IS | `sinkra-mapear-processo` |
| Resolver decisões e transformar intenção em contrato | `sinkra-elicitar-construcao` |
| Separar Humano, Worker e Agente | `sinkra-modelar-executores` |
| Converter transição validada em skill | `sinkra-forjar-skill` |
| Extrair, deduplicar e recombinar nós de um AS-IS validado | `sinkra-extrair-nos` |
| Auditar integridade, drift e lacunas | `sinkra-auditar-sistema` |

Se o host não invocar skills, ler e executar diretamente o `SKILL.md`
correspondente. `sinkra-arquitetar-sistema` é a orquestradora geral.

## Regras invioláveis

- Preservar AS-IS antes de propor TO-BE.
- Separar fato, observação, interpretação, proposta, gap e conflito.
- Não inventar informação ausente; declarar o blocker e sua rota de resolução.
- Aplicar `reuse > adapt > create`.
- Separar executor, reviewer, accountable e dono do gate.
- Transformar output atual em input rastreável do próximo consumidor.
- Registrar decisão, evidência, gate, output, próximo owner e ponto de retomada.
- Retirar gate humano somente por evidência acumulada da transição específica.

## Persistência

Usar apenas `sinkra-work/` no projeto atendido:

```text
sinkra-work/
├── state.yaml
├── decisions/
├── evidence/
├── gates/
├── handoffs/
├── outputs/
├── registry/
├── runs/
├── journey.yaml
└── learnings.md
```

Atualizar `state.yaml` após cada task relevante. Ao encerrar, produzir um
handoff que permita outra IA continuar sem o histórico da conversa.

## Interação humana

Resolver contexto recuperável antes de perguntar. Levar ao humano somente
decisão irredutível, conflito de autoridade, risco ou exceção. Apresentar uma
decisão por turno com situação, consequências, opções reais e recomendação
separada. Registrar a escolha e pedir ratificação do conjunto antes de executar
mudanças que dependam dela.

## Limites

Este pacote não fornece enforcement mecânico. Não alegar locks, validações ou
gates automáticos que não foram realmente executados. Usar ferramentas nativas
do host quando disponíveis e registrar evidência observável do resultado.

`skills/` e `skills/_shared/` são normativos para operação. `materials/` é
explicativo e segue a precedência declarada em `materials/README.md`.
