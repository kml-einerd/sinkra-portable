# Task 07 — Executar e verificar

Executar somente quando o usuário autorizou implementação.

## Executar

1. Selecionar toda a fronteira de tasks permitidas pelo estado, dependências e
   capacidade disponível.
2. Fornecer somente o contexto necessário ao executor.
3. Produzir o output no destino contratado.
4. Verificar acceptance criteria com evidência.
5. Registrar conclusão, não aplicável, falha ou blocker.
6. Atualizar estado antes de avançar.
7. Solicitar gate humano quando risco ou contrato exigir.

Se o host permitir sessões paralelas, propor uma Wave e obter uma aprovação
humana para o conjunto. Acompanhar as sessões pelo recurso nativo do host,
consolidar o fan-in e manter um writer por árvore de trabalho. Não usar o humano
como mensageiro entre sessões.

Não confundir comando executado com output aceito. Não permitir que o executor
seja o único verificador de trabalho crítico.

## Aceitar

Cada task executada possui output encontrável, evidência, estado e próximo
consumidor.
