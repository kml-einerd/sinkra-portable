# Prompt de ativação

```text
Use a pasta Sínkra Portable anexada como sua camada metodológica.

Leia primeiro AGENTS.md e skills/_shared/references/sinkra-core.md. Localize ou
crie sinkra-work/state.yaml no projeto atendido. Escolha a skill adequada ao
pedido e leia integralmente seu SKILL.md, carregando somente as tasks,
checklists e referências indicadas.

Trate skills/ e skills/_shared/ como fonte operacional. Consulte
materials/README.md antes de usar materiais históricos ou de evidência.

Se esta plataforma não suportar skills nativamente, execute os arquivos como
instruções. Não dependa da memória do chat: registre estado, decisões,
evidências, outputs, gates e handoff em sinkra-work/.

Antes de agir, informe em uma frase a skill escolhida, a entidade e a transição
ou objetivo em trabalho.
```

# Prompt de retomada

```text
Leia AGENTS.md, sinkra-work/state.yaml e o último arquivo em
sinkra-work/handoffs/. Revalide as fontes e decisões que podem ter mudado.
Retome exatamente pelo next_action registrado, usando a skill indicada. Ao
terminar uma unidade, atualize o estado, registre evidências e deixe novo
handoff.
```
