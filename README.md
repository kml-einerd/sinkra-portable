# Sínkra Portable

Versão `0.2.0` — manifesto em [`PACKAGE.yaml`](PACKAGE.yaml).

Pacote autossuficiente para qualquer IA aplicar o método Sínkra sem instalar o
Sínkra Harness. Ele reúne instruções universais, sete skills operacionais,
referências, templates, materiais curados e uma estrutura simples de estado.

## Usar em qualquer IA

1. Envie ou disponibilize esta pasta inteira para a IA.
2. Envie o texto de [PROMPT.md](PROMPT.md).
3. A IA deve ler [AGENTS.md](AGENTS.md), depois
   [sinkra-core.md](skills/_shared/references/sinkra-core.md).
4. Para cada pedido, ela escolhe uma skill e carrega somente os arquivos
   referenciados por seu `SKILL.md`.

Se a plataforma suportar Agent Skills, copie a pasta `skills/` inteira para o
diretório de skills da plataforma. Não instale uma pasta `sinkra-*` isolada:
as sete skills compartilham contratos em `skills/_shared`. Se a plataforma não
suportar skills, a IA pode ler os arquivos diretamente.

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
│   └── sinkra-*/              sete skills operacionais
├── materials/                 fontes curadas para consulta sob demanda
└── scripts/validate_portable.py verificação estrutural sem dependências
```

## Validar a cópia

Em uma máquina com Python 3.11 ou superior:

```text
python scripts/validate_portable.py
```

O comando é somente leitura e confirma arquivos obrigatórios, links locais,
frontmatter das skills e cópias operacionais dos contratos.

O método documental funciona sem Python. Promoção e validação determinística do
Registry de nós exigem Python 3.11 ou superior; sem ele, a IA pode preparar e
revisar candidatos, mas deve bloquear a promoção e registrar o handoff.

## O que ficou de fora

Não há CLI, runtime, daemon, banco, locks, budgets, adapters ou schemas do
Harness. Gates e estado continuam explícitos, mas são aplicados pela IA e pelo
humano por meio de arquivos legíveis.

Não carregar `materials/` inteiro em toda tarefa. Ler primeiro
[`materials/README.md`](materials/README.md) para saber o que é canônico,
histórico ou apenas evidência.
