# Sínkra Portable

Pacote autossuficiente para qualquer IA aplicar o método Sínkra sem instalar o
Sínkra Harness. Ele reúne instruções universais, seis skills operacionais,
referências, templates, materiais curados e uma estrutura simples de estado.

## Usar em qualquer IA

1. Envie ou disponibilize esta pasta inteira para a IA.
2. Envie o texto de [PROMPT.md](PROMPT.md).
3. A IA deve ler [AGENTS.md](AGENTS.md), depois
   [sinkra-core.md](skills/_shared/references/sinkra-core.md).
4. Para cada pedido, ela escolhe uma skill e carrega somente os arquivos
   referenciados por seu `SKILL.md`.

Se a plataforma suportar Agent Skills, copie `skills/_shared` e as pastas
`skills/sinkra-*` para o diretório de skills da plataforma, preservando a mesma
estrutura relativa. Se não suportar, a IA pode ler os arquivos diretamente.

## Começar um projeto

Copie `skills/_shared/templates/sinkra-work` para a raiz do projeto atendido. A
IA deve atualizar os arquivos após cada task relevante e retomar sempre pelo
último handoff, nunca apenas pela memória do chat.

## Estrutura

```text
sinkra-portable/
├── AGENTS.md                  instruções universais para a IA
├── PROMPT.md                  prompts de ativação e retomada
├── skills/                    método executável em Agent Skills
│   ├── _shared/               contratos, referências e template de estado
│   └── sinkra-*/              seis skills operacionais
└── materials/                 fontes curadas para consulta sob demanda
```

## O que ficou de fora

Não há CLI, runtime, daemon, banco, locks, budgets, adapters ou schemas do
Harness. Gates e estado continuam explícitos, mas são aplicados pela IA e pelo
humano por meio de arquivos legíveis.

Não carregar `materials/` inteiro em toda tarefa. Usá-lo para aprofundar ou
resolver divergências; o fluxo normal começa pelas skills e referências.
