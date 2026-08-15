# Portabilidade e persistência

Executar sempre em modo portátil, sem runtime próprio.

## Inicializar

1. Reutilizar a fonte de estado declarada pelo projeto.
2. Na ausência dela, copiar `skills/_shared/templates/sinkra-work/` para a raiz
   do projeto atendido.
3. Usar `sinkra-work/state.yaml` como índice do trabalho atual.
4. Persistir decisões, evidências, runs, registry, Journey Log e handoffs nas
   pastas correspondentes.
5. Usar os templates compartilhados como contratos legíveis.

Registrar autoridade e resultado do gate sem alegar enforcement mecânico
inexistente. Não simular locks, budgets, validações ou automações que o host não
executou de verdade.

## Precedência

As instruções de segurança e do projeto atendido prevalecem. As skills governam
método, conteúdo, interação e composição das tasks. `sinkra-work/` governa a
continuidade entre sessões.

## Retomar

Antes de continuar:

- localizar último estado e handoff;
- revalidar arquivos, decisões, ferramentas e regras externas listadas;
- continuar do `next_action`, sem reconstruir o trabalho pelo chat;
- registrar drift antes de substituir qualquer artefato.
