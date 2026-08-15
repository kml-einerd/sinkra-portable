# Interação guiada de decisões — extração e calibração

## Conclusão

O vídeo mostra quatro fases do mesmo sistema:

1. às `02:58:29`, Alan pede um diagnóstico das decisões humanas necessárias
   antes de continuar o backlog e automatizar a execução;
2. às `03:29:19`, a governance pipeline faz preflight, reaproveita decisões e
   leva ao humano somente os gaps reais;
3. às `03:45:36`, um gate técnico em lote expõe esses gaps, mas ainda transfere
   jargão e escolhas simultâneas ao humano;
4. às `04:06:15`, Pedro transforma o gate em conversa guiada, não técnica, com
   uma decisão por vez, exemplo prático, opções e ratificação final.

A elicitação não é o início do método. Ela é a superfície humana de uma cadeia
que antes compreende, classifica e reduz o espaço de decisão.

## O que eles buscavam no início

Alan queria saber quais decisões deveriam ser tomadas antes de continuar uma
grande fila de mudanças: quais ADRs precisavam ser formalizados, quais lacunas
dependiam realmente de Pedro ou de outro humano e como registrar isso para que
a execução posterior pudesse ser automática sem perder governança.

O pedido não era “faça perguntas”. Era:

```text
entenda o estado e o trabalho pretendido
→ descubra quais decisões já existem
→ separe o que não bloqueia
→ identifique o que exige pesquisa
→ leve ao humano somente decisões irredutíveis
→ registre para destravar execução rastreável
```

## Linha do tempo causal

| Tempo | Evidência | Implicação |
|---|---|---|
| `02:57:44` | Alan omite deliberadamente o nome da skill para testar o comportamento a partir da intenção | linguagem natural e comando explícito devem acionar a mesma cadeia |
| `02:58:29–02:59:16` | pedido busca decisões e ADRs necessários antes de continuar backlog e mudanças | o objetivo é destravar execução segura, não produzir perguntas |
| `02:59:37–03:00:39` | agente conclui sua análise, pergunta se o humano domina e trata ADR como entidade com ciclo | a pergunta de domínio ocorre depois da análise e o resultado tem destino operacional |
| `03:02:50` | relatório separa ADRs posteriores não bloqueantes, decisões que já existem e sequência de desbloqueio | nem toda pendência vira nova decisão ou novo artefato |
| `03:06:20–03:06:25` | trabalho pode avançar sem novo ADR, mantendo gates e rastreabilidade | “sem novo ADR” não significa “sem governança” |
| `03:08:00–03:08:44` | pipeline percorre registros e aplica `reuse > adapt > create` | reaproveitar precede perguntar e criar |
| `03:29:19` | Alan invoca explicitamente `/governance-pipeline` | comando explícito é uma segunda porta para o mesmo mecanismo |
| `03:32:06–03:33:33` | preflight resolve inputs, ADRs, gaps e escolhe elicitação direta ou research companion | contexto e autoridade vêm antes da pergunta |
| `03:45:36–03:47:50` | gate GAPS apresenta várias decisões técnicas e respostas compactas | anti-padrão: lote e jargão transferem carga cognitiva ao humano |
| `03:46:27` | Pedro diz que não sabia responder sem conhecer épicos e projeto | não pedir decisão sem contexto elegível suficiente |
| `03:48:05–03:48:58` | skill mantém passo a passo; agente decide caminhos e variáveis | protocolo determinístico, interpretação contextual |
| `03:50:09–03:51:28` | decision trees vão para skills, scores para quality gates, decisões para agentes e axiomas para governança | conhecimento extraído precisa ser roteado para um mecanismo ativo |
| `03:53:09–03:54:28` | hipótese mínima e testes abertos que tentam induzir erro | validar o mecanismo antes de ampliar autonomia |
| `03:56:42–03:57:12` | Cockpit sinaliza atenção e centraliza decisões; Pedro não conversa com sessões-filhas | um canal humano principal e um registro de decisão |
| `04:04:52–04:05:59` | ADR é criado; profundidade de revisão varia com novidade, centralidade e risco | esforço de leitura não é fixo |
| `04:06:15–04:07:14` | comando para elicitar cada decisão de modo não técnico, com exemplos reais; uma por vez | núcleo do protocolo |
| `04:07:46–04:09:18` | D1 mostra problema, exemplo, opções, recomendação e escolha | contrato visual da resposta |
| `04:14:01` | explicitar uma decisão implica apresentar opções | opção é parte obrigatória da arquitetura |
| `04:20:40–04:21:08` | Pedro rejeita A/B/C e cria D, combinando compatibilidade com fail-safe | opções propostas não formam menu fechado |
| `04:29:28–04:29:48` | só D6 muda; sistema resume D1–D9 e pede ratificação | escolha local e ratificação global são gates distintos |
| `04:29:51–04:31:39` | gate só é retirado após logs e alta concordância em muitas execuções | autonomia nasce de evidência longitudinal |
| `04:31:51–04:35:00` | heurísticas externas quebram conformismo e memória ruim | revisão externa é mecanismo de aprendizagem e segurança |

## O que a tela evidencia

### Análise e preflight

- o relatório distingue decisões necessárias, posteriores e já cobertas;
- a sequência de desbloqueio não exige criar um ADR para cada item;
- o preflight resolve input, numeração, referências e colisões antes de criar;
- especialistas consolidam decisões, gaps e proveniência até o primeiro gate
  humano;
- elicitação direta e pesquisa são rotas escolhidas conforme domínio e fonte.

### Gate inicial

- um documento único contém várias decisões;
- títulos e opções usam nomes internos, siglas e termos técnicos;
- recomendações aparecem, mas não há contexto prático suficiente;
- a resposta compacta (`1A, 2B, 3A...`) privilegia velocidade, não compreensão.

### Elicitação calibrada

- o ADR permanece visível como fonte, separado da conversa;
- a conversa mostra `D<n> de <total>` e uma pergunta em linguagem comum;
- situação atual e exemplo prático aparecem antes das opções;
- cada opção explica efeito, ganho, perda e risco;
- a recomendação do agente é explícita, sem se passar pela decisão humana;
- o agente espera a escolha antes de avançar;
- no final, alterações são aplicadas ao ADR e o conjunto é ratificado.

### Cockpit

- sessões de execução ficam separadas da fila e do histórico de decisões;
- mudança visual chama atenção somente quando existe ação humana pendente;
- o humano fala com a sessão principal ou com o registro, não com children;
- o canal de decisão pode mudar — tela, notificação, Telegram ou WhatsApp — sem
  mudar o contrato.

## Protocolo invariável

```text
capturar intenção e execução a destravar
→ resolver fonte, estado e autoridade
→ aplicar reuse > adapt > create
→ classificar: resolvido, não bloqueante, pesquisa, decisão humana ou conflito
→ levar ao humano somente gaps irredutíveis
→ decompor esses gaps em decisões atômicas
→ ordenar por dependência e risco
→ mostrar uma decisão por turno
→ traduzir para consequência observável
→ apresentar exemplo prático real
→ oferecer somente opções viáveis e uma recomendação justificada
→ aceitar escolha, combinação, nova opção ou adiamento
→ registrar imediatamente sem avançar em silêncio
→ resumir o conjunto e pedir ratificação
→ atualizar artefatos e executar somente após o gate
→ observar overrides antes de reduzir controle humano
```

## Contrato de resposta

```markdown
## D<n> de <total> — <pergunta em linguagem comum>

<situação atual e por que a decisão existe>

### Exemplo prático
<cenário observável por uma pessoa afetada>

### Opções

**A — <nome>**
<efeito, ganho, perda, risco e reversibilidade>

**B — <nome> — recomendada**
<efeito, ganho, perda, risco e motivo da recomendação>

Qual caminho você escolhe? Pode responder com uma opção, combinar caminhos,
propor outra alternativa ou adiar.
```

Depois da resposta, o sistema deve devolver uma confirmação curta do que foi
registrado e abrir somente a próxima decisão. Ao terminar:

```markdown
## Ratificação

D1=A · D2=A · D3=adiada · D4=alternativa do decisor

Mudanças em relação ao draft: <lista>
Riscos aceitos: <lista>
Pendências: <lista>

Responda `ratifico` ou `ajustar: ...`.
```

## Constante versus contextual

| Constante | Contextual |
|---|---|
| uma decisão por turno | quantidade total de decisões |
| linguagem do decisor | nomes de ADR, Epic, código e agentes |
| exemplo observável | domínio do exemplo |
| opções reais com consequências | número de opções |
| recomendação separada | alternativa recomendada |
| alternativa livre do humano | formato do canal |
| registro e ratificação | profundidade técnica mostrada |

Não copiar `D1–D9`, A/B/C, Cockpit, ADR ou termos de DevOps como se fossem
universais. O padrão é a superfície de decisão, não o conteúdo do caso.

## Ajustes derivados para o pack

1. remover a exigência de exatamente três cenários;
2. garantir uma decisão por turno e não produzir um documento em lote;
3. aceitar combinação ou alternativa criada pelo decisor;
4. calibrar profundidade por novidade, centralidade, risco e domínio humano;
5. separar escolha local, persistência, ratificação final e autorização para
   executar;
6. acionar a cadeia tanto por intenção em linguagem natural quanto por comando;
7. triar decisões existentes, itens não bloqueantes e pesquisa antes de
   perguntar ao humano;
8. não transformar governança em quota de ADRs ou outros artefatos.

## Fontes

- vídeo local e link registrado em `arquivos-base/synkra-skills/video-fonte.txt`;
- `arquivos-base/synkra-skills/transcricao-pedro/transcricao-timestamped.txt`;
- `arquivos-base/synkra-skills/transcricao-pedro/pedro-transcricao-completa.md`;
- inspeção visual de frames em 1920×1080 nos marcos citados.
