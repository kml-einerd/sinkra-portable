# Playbook de Engenharia de Prompts Sínkra

Referência para repetir o processo que transformou materiais extensos, conversas e sistemas confusos em modelos AS-IS, conhecimento rastreável, skills, nós semânticos e handoffs utilizáveis por outros agentes.

## 1. O que gerou valor

O resultado não veio de pedir apenas “analise profundamente”. Ele veio de combinar nove mecanismos:

1. **Estado congelado:** declarar o que já estava concluído e o que não deveria ser refeito.
2. **Missão delimitada:** definir resultado, escopo, restrições e condição de encerramento.
3. **Roteamento por skill:** indicar qual skill governa cada fase, sem misturar responsabilidades.
4. **Verdade operacional:** reconstruir o AS-IS antes de propor o TO-BE.
5. **Evidência e autoridade:** distinguir observado, declarado, inferido, proposto, gap e conflito.
6. **Unidade semântica:** usar chunks somente para leitura e reconstruir nós completos atravessando os cortes.
7. **Graph engineering:** separar identidade, relações, composições, runtime e evidências.
8. **Artefato obrigatório:** toda fase termina com arquivos persistidos, verificação e handoff.
9. **Gates explícitos:** o agente avança autonomamente dentro da wave e para somente diante de uma decisão real.

## 2. As quatro camadas que não podem ser misturadas

| Camada | Pergunta | Exemplos |
|---|---|---|
| Fonte | De onde veio? | vídeo, WhatsApp, documento, tela, log |
| Modelo AS-IS | O que acontece ou existe hoje? | entidades, stages, tasks, regras, exceções |
| Grafo reutilizável | Quais peças completas podem ser recombinadas? | definições, relações e composições |
| Decisão TO-BE | O que será mudado? | correção, nova arquitetura, automação, skill |

Nunca usar uma interpretação futura para “corrigir” silenciosamente o AS-IS. Nunca tratar um trecho bruto como um nó pronto. Nunca promover candidato sem decisão humana.

## 3. Arquitetura do workflow

```text
intenção do usuário
→ plano operacional curto
→ inventário e proveniência
→ reconstrução AS-IS
→ gate AS-IS
→ extração de nós candidatos
→ revisão de granularidade e grafo
→ plano de promoção
→ gate humano
→ Registry canônico
→ novas composições
```

### Fase 0 — Congelar o estado

Registrar antes de qualquer execução:

- o que já foi concluído e aprovado;
- quais artefatos são a fonte da continuação;
- o que está pausado;
- o que não pode ser refeito ou alterado;
- qual é a próxima transição autorizada.

Essa abertura impede o agente de reiniciar a investigação e consumir contexto reconstruindo algo que já existe.

### Fase 1 — Planejar a aplicação

Registrar um plano operacional curto em `sinkra-work/runs/` quando a execução
for longa, possuir múltiplas fontes ou precisar de checkpoints. O plano define
a aplicação do método naquele pacote; ele não redescobre o problema.

Exigir:

- fontes e outputs;
- divisão em waves;
- dependências reais;
- pontos de autorrevisão;
- gates humanos;
- estado recuperável e forma de retomar.

Agrupar na mesma wave tudo que puder avançar em paralelo. Separar somente o que depender do resultado de uma wave anterior.

### Fase 2 — Inventariar antes de interpretar

O primeiro output deve responder:

- quais fontes foram encontradas e realmente consumidas;
- período, formato, autor e autoridade;
- lacunas e conflitos;
- duplicações e variantes;
- cobertura processada.

Inventário não é burocracia: ele permite provar que o agente não ignorou silenciosamente uma pasta, trecho ou período.

### Fase 3 — Reconstruir o AS-IS

Usar `sinkra-mapear-processo`. Pedir casos reais e rastrear:

- evento inicial e condição final;
- entidade e lifecycle;
- stages e transições;
- tasks, executores, inputs e outputs;
- decisões, guards, loops, recusas e cancelamentos;
- artefatos e fontes de verdade.

Registrar propostas de melhoria separadamente como `to_be_candidates`.

### Fase 4 — Extrair o grão semântico

Usar `sinkra-extrair-nos` somente depois que existir um AS-IS rastreável.

O chunk é uma janela de leitura. O nó é a menor unidade que continua:

- compreensível sem reler toda a fonte;
- identificável e versionável;
- referenciável por outros objetos;
- reutilizável em outra composição;
- completo em seu contrato.

Separar:

- `definition`: núcleo reutilizável;
- `composition`: ordem, papel, condição e parâmetros;
- `runtime`: ocorrência histórica;
- `evidence`: prova imutável.

### Fase 5 — Revisar antes de promover

Executar revisão adversarial para detectar:

- fragmentos que deveriam ser um único nó;
- mega-nós que escondem múltiplas responsabilidades;
- duplicatas com nomes diferentes;
- ordem ou contexto embutidos no núcleo;
- definição misturada com runtime;
- inferência promovida a fato;
- referência quebrada ou proveniência insuficiente.

O output dessa fase é um plano: `promote-new`, `promote-version`, `hold` ou `archive`.

### Fase 6 — Promover somente após gate

O agente pode preparar e validar. A promoção exige decisão humana nominal. O gate deve mostrar:

- candidatos selecionados;
- duplicatas resolvidas;
- versões e relações afetadas;
- blockers e warnings;
- evidências usadas;
- efeito esperado da decisão.

Ideias, blockers e tasks recuperados do WhatsApp ficam em `hold` por padrão.

## 4. Como dividir o trabalho entre agentes

| Papel | Responsabilidade | Não deve fazer |
|---|---|---|
| Orquestrador principal | manter intenção, backlog, decisões e waves | executar tudo sozinho |
| Executor | produzir uma wave e suas evidências | aprovar o próprio gate |
| Reviewer independente | tentar invalidar claims e critérios | reescrever a entrega inteira |
| Humano | decidir ambiguidades materiais e promoções | repetir verificações automáticas |

O agente principal conversa com o usuário uma decisão por vez. Enquanto isso, pode despachar trabalhos independentes. Cada executor recebe escopo, fontes, output, critérios de sucesso e proibições.

## 5. Estrutura de um prompt forte

Montar o prompt nesta ordem:

```text
1. ESTADO ATUAL
   O que já existe, foi aprovado ou está pausado.

2. MISSÃO
   Um resultado observável e uma condição de encerramento.

3. FONTES
   Caminhos, autoridade, período e cobertura esperada.

4. RESTRIÇÕES
   O que não alterar, inferir, promover, implementar ou refazer.

5. SKILLS E ROTEAMENTO
   Qual skill governa cada fase e quando ocorre o handoff.

6. REGRAS DE VERDADE
   Classes de evidência, AS-IS/TO-BE e tratamento de gaps.

7. WORKFLOW
   Waves, dependências, paralelismo, autorrevisões e gates.

8. CONTRATO DE OUTPUT
   Arquivos, formatos, IDs, campos e localização.

9. CRITÉRIOS DE SUCESSO
   Provas verificáveis, não adjetivos como “completo”.

10. HANDOFF
    Estado final, pendências, próxima ação e resume_from.
```

## 6. Template mestre — materiais volumosos

```markdown
# CONTEXTO

Estamos continuando um trabalho já iniciado.

Estado confirmado:
- concluído: <outputs e gates aprovados>;
- pausado em: <transição exata>;
- fonte da continuação: <arquivos ou pacote>;
- não refazer: <fases encerradas>.

# MISSÃO

Transformar <fontes> em <resultado persistido>, preservando proveniência,
contradições e lacunas. Encerrar quando <critério observável>.

# PREPARAÇÃO

Antes de executar, monte um plano operacional curto com fontes, outputs, waves,
dependências, pontos de autorrevisão, gates e estado recuperável. Mostre o plano
e aguarde aprovação.

# ROTEAMENTO

1. Use `sinkra-mapear-processo` somente se o AS-IS ainda não estiver validado.
2. Use `sinkra-extrair-nos` para candidate e review.
3. Use `sinkra-auditar-sistema` com reviewer independente ao final de cada wave material.
4. Não execute promote sem decisão humana explícita.

# REGRAS DE VERDADE

- Classifique claims como observado, declarado, inferido, proposto, gap ou conflito.
- Preserve fonte e locator.
- Não transforme exemplo em regra universal.
- Não complete ausência por imaginação.
- Não misture AS-IS com TO-BE.
- Não use chunks como fronteiras dos nós.

# EXECUÇÃO

- Atravesse os materiais antes de fechar unidades semânticas.
- Produza algo verificável em cada wave; não entregue apenas narrativa.
- Faça perguntas somente quando a resposta mudar materialmente o modelo.
- Registre incertezas não bloqueantes e continue.
- Pare em decisões irreversíveis, promoção ou mudança de escopo.

# OUTPUT

Grave tudo em <pasta isolada> sem alterar as fontes.

Entregue:
1. inventário e proveniência;
2. modelo ou candidatos;
3. relações e composições externas;
4. relatório de revisão;
5. gaps, decisões e handoff.

# HANDOFF

Informe cobertura, contagens, evidências, conflitos, itens em hold, gates e a
próxima ação executável. Outra sessão deve conseguir continuar somente pelos
artefatos persistidos.
```

## 7. Ajustes por tipo de fonte

### Legado operacional

Priorizar entidade, lifecycle, stages, transitions, guards, tasks, executores, inputs, outputs e artefatos. Quando documentos divergirem, preservar todas as variantes e apontar a autoridade de cada uma.

### WhatsApp

Ler antes e depois de cada mensagem. Classificar como `idea`, `task_candidate`, `confirmed_task`, `decision`, `question` ou `blocker`. Desejo não vira task sem compromisso observável. Unir repetições sem perder autor, data ou evolução da ideia.

### Vídeo ou interação guiada

Separar:

- fala explícita;
- ação realizada na tela;
- instrução do facilitador;
- resposta do usuário;
- comportamento constante do sistema;
- elemento específico daquele caso.

Analisar janelas anteriores e posteriores. Usar visão somente quando a tela acrescentar estrutura que a transcrição não contém.

### Sistema já modelado

Não reconstruir a fonte original. Ler o handoff e validar o pacote persistido. Começar na próxima transição: extração de nós, review, promoção ou composição.

## 8. Prompts de controle

### Retomar uma sessão

```markdown
Retome do ponto registrado no handoff. Não use a memória da conversa como fonte
primária. Confirme os artefatos persistidos, o último gate aprovado e a próxima
transição. Não refaça fases encerradas. Mostre a primeira ação e continue.
```

### Pedir revisão independente

```markdown
Atue como reviewer independente. Leia a spec, os outputs e as evidências.
Verifique o resultado, não a confiança do executor. Classifique achados como
bloqueador, correção ou observação. Não edite e não aprove o próprio trabalho.
```

### Impedir documentação sem manifestação

```markdown
Para cada definição tomada, produza o menor artefato verificável que a manifeste.
Quando existirem alternativas, gere opções comparáveis na mesma wave. Volte ao
usuário com contraste, evidência e recomendação; não apenas com uma descrição.
```

### Evitar perguntas demais

```markdown
Pergunte somente quando a resposta alterar materialmente a interpretação, o
escopo ou uma decisão irreversível. Para incerteza não bloqueante, avance com a
hipótese explicitamente marcada e registre o gap.
```

## 9. Critérios para saber se o prompt está pronto

Antes de enviar, conferir:

- Existe um resultado observável, não apenas “analisar”?
- O estado anterior e o ponto de retomada estão explícitos?
- AS-IS, candidatos e TO-BE estão separados?
- Toda afirmação crítica pode apontar para uma fonte?
- O output possui arquivos, formato e localização?
- As waves refletem dependências reais?
- O agente sabe onde deve avançar sozinho e onde deve parar?
- Outro agente consegue continuar pelo handoff sem reler a conversa?

## 10. Antipadrões que reduziram qualidade

- Pedir “capacidade máxima” sem contrato de output.
- Mandar resumir antes de inventariar e relacionar.
- Cortar nós pelo tamanho do arquivo ou janela de contexto.
- Misturar extração, correção e implementação na mesma fase.
- Pedir que o mesmo agente execute e aprove seu gate.
- Parar a cada microtask que já estava autorizada.
- Manter decisões apenas no chat.
- Usar `latest` ou nomes soltos quando uma versão ou ID deveria estar fixada.
- Reabrir um AS-IS aprovado porque uma nova skill foi instalada.

## 11. Referências canônicas deste playbook

- [prompt de reconstrução e extração](07-prompt-reconstrucao-e-extracao-de-nos.md)
- [mapear processo](../skills/sinkra-mapear-processo/SKILL.md)
- [extrair nós](../skills/sinkra-extrair-nos/SKILL.md)
- [contrato do grafo](../skills/sinkra-extrair-nos/references/node-graph-contract.md)
- [evidência e autoridade](../skills/_shared/references/evidence-and-authority.md)
- [contratos operacionais](../skills/_shared/references/contracts.md)

## 12. Regra de ouro

O prompt ideal não tenta carregar todo o conhecimento dentro dele. Ele aponta para fontes, skills e contratos; congela o estado; define o próximo resultado; dá autonomia dentro da wave; exige evidência e artefatos; e reserva ao humano apenas as decisões que realmente mudam o sistema.
