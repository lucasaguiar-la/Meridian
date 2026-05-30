# Backlog Priorizado

## Objetivo

Este documento organiza as proximas evolucoes do projeto Meridian em ordem de prioridade, considerando:

- valor de produto
- reaproveitamento do que ja existe no backend
- custo de implementacao
- reducao de risco tecnico
- capacidade de diferenciar o projeto

---

## Criterios de Priorizacao

### P0

Itens com alto impacto e boa relacao custo/beneficio. Devem entrar primeiro.

### P1

Itens estrategicos que ampliam muito o produto, mas dependem de alguma maturidade adicional.

### P2

Itens valiosos, porem mais avancados, mais caros ou mais adequados para uma fase posterior.

---

## Backlog Priorizado

## P0

### 1. Pagina de relatorios no frontend

**Por que priorizar**

O backend ja possui endpoints de relatorios semanais e mensais, mas o frontend ainda nao expone essa capacidade. Isso gera valor rapido aproveitando estrutura existente.

**Impacto**

Alto

**Esforco**

Baixo a medio

**Valor gerado**

- amplia o uso analitico da plataforma
- melhora a percepcao de maturidade do produto
- transforma dados ja coletados em leitura executiva

**Escopo sugerido**

- pagina de relatorio semanal
- pagina de relatorio mensal
- filtro por linguagem
- blocos visuais com top por estrelas, engajamento e crescimento

**Criterio de pronto**

Usuario consegue consultar relatorios prontos sem depender da Swagger UI.

### 2. Suite minima de testes

**Por que priorizar**

Hoje existe estrutura de testes, mas sem cobertura real. Isso aumenta risco a cada evolucao.

**Impacto**

Alto

**Esforco**

Medio

**Valor gerado**

- reduz regressao
- melhora seguranca para novas features
- facilita CI/CD depois

**Escopo sugerido**

- testes de calculo de `engagement_score`
- testes de delta de estrelas
- testes dos endpoints principais
- testes basicos do pipeline de coleta com mocks

**Criterio de pronto**

Projeto passa a ter uma base automatizada para validar dominio, API e coleta.

### 3. Observabilidade operacional do collector

**Por que priorizar**

Como o produto depende da coleta, a confiabilidade operacional precisa ficar mais clara para quem mantem o sistema.

**Impacto**

Alto

**Esforco**

Baixo a medio

**Valor gerado**

- facilita diagnostico de falhas
- ajuda a entender latencia e volume coletado
- prepara o terreno para alertas futuros

**Escopo sugerido**

- historico de execucoes mais completo
- duracao de cada coleta
- falhas por linguagem
- exposicao do status de rate limit

**Criterio de pronto**

Fica facil responder se o collector esta saudavel, lento ou falhando.

### 4. Melhorias de filtro e navegacao analitica

**Por que priorizar**

O projeto ja permite busca e ranking, mas ainda pode ganhar profundidade de exploracao com pouco aumento de complexidade.

**Impacto**

Medio a alto

**Esforco**

Baixo a medio

**Valor gerado**

- aumenta utilidade pratica da plataforma
- melhora descoberta de repositorios relevantes
- reduz friccao na navegacao

**Escopo sugerido**

- filtro para excluir forks
- filtro por faixa de stars
- filtro por idade do repositorio
- ordenacoes adicionais e preservacao de filtros na URL

**Criterio de pronto**

Usuario consegue refinar melhor os rankings e a busca.

---

## P1

### 5. Watchlists e favoritos

**Por que priorizar**

Esse e o passo mais natural para sair de uma experiencia puramente exploratoria e entrar em acompanhamento recorrente.

**Impacto**

Alto

**Esforco**

Medio

**Valor gerado**

- aumenta retencao
- cria uso personalizado
- abre espaco para alertas e dashboards pessoais

**Escopo sugerido**

- salvar repositorios favoritos
- lista de monitoramento por usuario
- visao consolidada das variacoes recentes

**Criterio de pronto**

Usuario acompanha seu proprio subconjunto de repositorios.

### 6. Alertas por webhook ou e-mail

**Por que priorizar**

Depois de ter watchlists ou boa observabilidade, alertas elevam o produto de consulta para acompanhamento ativo.

**Impacto**

Alto

**Esforco**

Medio

**Valor gerado**

- cria rotina de uso
- gera valor mesmo sem o usuario abrir a plataforma
- ajuda tanto casos de produto quanto operacao

**Escopo sugerido**

- alerta de crescimento acima de limite
- alerta de novo repo em destaque
- alerta de falha do collector

**Criterio de pronto**

Eventos relevantes passam a ser comunicados automaticamente.

### 7. Cache com Redis para endpoints mais consultados

**Por que priorizar**

Trending, ranking e relatorios sao leituras repetitivas e previsiveis. Cache reduz custo e melhora responsividade.

**Impacto**

Medio a alto

**Esforco**

Medio

**Valor gerado**

- melhora performance percebida
- reduz carga no banco
- prepara crescimento de uso

**Escopo sugerido**

- cache para `languages`
- cache para ranking por linguagem
- cache para trending
- invalidacao simples apos coleta

**Criterio de pronto**

Consultas populares ficam mais rapidas e estaveis.

### 8. Resumos com IA

**Por que priorizar**

O projeto ja antecipa uma camada de IA. Esse recurso pode virar diferencial se for usado para explicar, resumir e priorizar insights.

**Impacto**

Alto

**Esforco**

Medio a alto

**Valor gerado**

- adiciona interpretacao aos dados
- melhora leitura para publico menos tecnico
- diferencia o projeto de um dashboard comum

**Escopo sugerido**

- resumo semanal por linguagem
- resumo mensal por linguagem
- explicacao curta de porque um repositorio esta em alta

**Criterio de pronto**

Usuario passa a receber contexto, e nao apenas numeros.

---

## P2

### 9. Comparacao entre linguagens e repositorios

**Por que priorizar**

Tem alto valor analitico, mas faz mais sentido depois que as visoes principais estiverem maduras.

**Impacto**

Medio a alto

**Esforco**

Medio

**Valor gerado**

- aprofunda a proposta analitica
- ajuda em benchmarking

**Escopo sugerido**

- comparativo de crescimento entre linguagens
- comparativo historico entre repositorios
- indicadores lado a lado

### 10. Exportacao de relatorios

**Por que priorizar**

Bom para compartilhamento, apresentacao e uso externo, mas nao e o primeiro gargalo do produto.

**Impacto**

Medio

**Esforco**

Medio

**Escopo sugerido**

- exportar CSV
- exportar PDF
- gerar links compartilhaveis

### 11. Autenticacao e multiusuario

**Por que priorizar**

Necessario para personalizacao robusta, mas adiciona complexidade estrutural.

**Impacto**

Alto

**Esforco**

Alto

**Escopo sugerido**

- login
- perfil de usuario
- preferencias
- watchlists por conta

### 12. Stack avancada de operacao

**Por que priorizar**

Prometheus, Grafana, filas e workers sao evolucoes fortes, mas valem mais quando houver uso maior ou carga operacional mais intensa.

**Impacto**

Medio a alto

**Esforco**

Alto

**Escopo sugerido**

- Prometheus
- Grafana
- Celery ou workers dedicados
- separacao mais forte entre coleta e processamento

---

## Ordem Recomendada de Execucao

### Trilha recomendada

1. Pagina de relatorios no frontend
2. Suite minima de testes
3. Observabilidade do collector
4. Melhorias de filtro e navegacao
5. Watchlists e favoritos
6. Alertas
7. Cache com Redis
8. Resumos com IA

Essa sequencia entrega valor visivel cedo, reduz risco tecnico e prepara bem os recursos mais avancados.

---

## Backlog de Curto Prazo

Se a ideia for escolher apenas os proximos passos imediatos, eu recomendaria este recorte:

1. Expor relatorios no frontend
2. Implementar testes essenciais
3. Fortalecer monitoramento do collector

Esse trio melhora produto, confiabilidade e sustentacao ao mesmo tempo.

---

## Conclusao

O Meridian ja tem um nucleo forte. O melhor caminho agora nao e expandir em muitas frentes ao mesmo tempo, e sim transformar a base atual em algo mais:

- visivel para o usuario
- seguro para evoluir
- observavel na operacao
- inteligente na leitura dos dados

Se houver uma unica aposta para comecar, a melhor relacao entre impacto e custo esta em **relatorios no frontend + testes basicos + observabilidade do collector**.
