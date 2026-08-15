# Mecanismo reconstruído do vídeo

## Núcleo sustentado pela fonte

```text
capturar intenção e execução a destravar
→ resolver contexto e saber o que não usar
→ aplicar reuse > adapt > create
→ separar resolvido, não bloqueante, pesquisa, decisão humana e conflito
→ levar somente gaps irredutíveis ao gate humano
→ perguntar se o humano domina cada dimensão restante
→ humano vira fonte primária ou companion pesquisa
→ decompor o conjunto em decisões atômicas
→ mostrar uma decisão por turno
→ traduzir por consequência e exemplo prático
→ apresentar opções reais e recomendação explícita
→ aceitar escolha, combinação, nova opção ou adiamento
→ registrar cada escolha
→ ratificar o conjunto
→ executar sob controle
→ observar correções antes de retirar gates
```

O objetivo não é obter uma resposta elegante. É controlar como conhecimento,
intenção, código e responsabilidade participam da decisão.

## Início real da interação

O processo começa às `02:58:29`, quando Alan pede para descobrir quais decisões
humanas e ADRs são necessários antes de continuar uma grande fila de mudanças.
Ele procura lacunas reais que precisam ser formalizadas para destravar execução
posterior automática e governada.

Antes disso, Alan omite o nome da skill para testar se a intenção basta. Às
`03:29:19`, ele invoca `/governance-pipeline` explicitamente. As duas entradas
devem convergir para a mesma cadeia.

Às `03:45:36`, o primeiro gate mostra várias decisões técnicas de uma vez. Às
`03:46:27`, Pedro afirma que não sabia responder sem ler os épicos e compreender
o projeto. Esse trecho demonstra o anti-padrão.

Às `04:06:15`, Pedro calibra a superfície: cada decisão em linguagem não
técnica e com exemplo prático real. Às `04:07:14`, explicita uma decisão por
vez. Às `04:29:45`, o sistema resume as escolhas e pede ratificação.

## Triagem anterior ao diálogo

O relatório anterior ao gate distingue:

- decisão já tomada, que deve ser reaproveitada;
- item futuro ou não bloqueante;
- lacuna que exige pesquisa;
- decisão irredutivelmente humana;
- conflito que impede avanço.

Somente as duas últimas classes chegam ao decisor, quando pertencem à sua
autoridade. “Sem novo ADR” não significa “sem governança”: gates, evidência,
rastreabilidade e execução controlada continuam válidos. ADR, Epic, política ou
processo são destinos possíveis da decisão, não quotas de produção.

## Contrato de cada turno

Exibir somente:

```markdown
## D<n> de <total> — <pergunta em linguagem comum>

<situação atual e por que ela exige decisão>

### Exemplo prático
<efeito observável para uma pessoa afetada>

### Opções
**A — <caminho>**
<consequência, ganho, perda, risco e reversibilidade>

**B — <caminho> — recomendada**
<consequência, ganho, perda, risco e motivo da recomendação>

Qual caminho você escolhe? Você pode combinar opções, propor outra ou adiar.
```

Não avançar até registrar a resposta. Não transformar o conjunto em documento
com várias escolhas simultâneas. Detalhes técnicos ficam disponíveis sob
demanda ou quando forem necessários para compreender risco e consequência.

## Ratificação

Depois da última decisão, mostrar:

- mapa compacto `D1=A · D2=B · D3=alternativa do decisor`;
- mudanças em relação ao draft;
- riscos aceitos e pendências;
- pedido explícito `ratifico` ou `ajustar: ...`.

Escolher uma opção e ratificar o conjunto são gates diferentes. Atualizar ADR,
contrato ou plano com as escolhas, mas só liberar execução após a ratificação
exigida.

## Cardinalidade das opções

O vídeo anterior sustenta o uso de três grandes cenários em certas decisões. A
execução observada não sustenta uma quota universal. Às `04:20:40`, Pedro
rejeita A/B/C e cria D, combinando compatibilidade automática com falha segura.

Logo:

- apresentar somente caminhos reais;
- não inventar uma terceira opção;
- não limitar o humano às opções propostas;
- agrupar ou dividir quando a quantidade prejudicar compreensão.

## Profundidade e canal

- Ler mais quando o objeto for novo, central ou arriscado; revisar somente as
  decisões quando o sistema estiver maduro e operacional.
- Centralizar interação na sessão principal ou no registro de decisões. Não
  exigir conversa com sessões-filhas.
- Tela, terminal ou notificação podem mudar; o contrato da decisão permanece.

## Aprendizagem

- Registrar escolhas, alternativas e overrides.
- Manter gate humano até existir amostra real de alta concordância em muitas
  execuções.
- Usar heurística externa e revisão adversarial para revelar conformismo,
  memória ruim e decisões locais frágeis.
- Rotear decision trees para skills, scores para quality gates, heurísticas
  contextuais para agentes e axiomas para governança.

## Implementações do pack

Estas peças são extensões nossas:

- resposta `parcial` e rota híbrida;
- eixos padronizados de comparação das opções;
- arquivos `sinkra-work/runs/`;
- contrato de construção e handoff;
- schemas YAML;
- divisão em tasks e checklists portáveis.

Não atribuir essas escolhas a Pedro como se fossem formato original.

## Fronteira

Esta skill é geral porque o mecanismo atua antes de qualquer domínio. A skill
`sinkra-arquitetar-sistema` a reutiliza dentro da ontologia Sínkra; não duplica
o protocolo.
