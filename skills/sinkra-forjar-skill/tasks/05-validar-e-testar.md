# Task 05 — Validar e forward-testar

## Estrutural

- validar frontmatter, nome e links;
- verificar arquivos referenciados e paths relativos;
- verificar ausência de placeholder;
- garantir que a skill é autocontida no pack.
- executar um caso mínimo para cada script adicionado.

## Comportamental

Testar em sessão limpa:

1. pedido direto que deve ativar;
2. pedido indireto equivalente;
3. input incompleto que deve perguntar ou bloquear;
4. pedido que não deve ativar;
5. falha ou exceção crítica;
6. resume a partir de estado persistido;
7. execução no modo portátil e em um segundo host quando disponível.

Passar artefatos brutos ao teste; não revelar a resposta esperada.

## Aceitar

O output atende ao contrato e uma sessão nova consegue continuar.
