# Meridian

Plataforma de insights sobre repositórios do GitHub. Coleta dados em tempo real via API do GitHub, armazena histórico de métricas e expõe uma API REST com rankings, tendências e relatórios por linguagem de programação.

## Funcionalidades

- Coleta automatizada dos top repositórios por linguagem (Python, JavaScript, TypeScript, Go, Rust e mais)
- Histórico de métricas com snapshots diários (estrelas, forks, issues, engagement score)
- API REST com rankings, trending repos, busca e relatórios
- Score de engajamento calculado com normalização logarítmica e pesos configuráveis
- Observabilidade: logs estruturados (JSON), health check, registro de cada execução do collector
- Arquitetura preparada para integração futura com IA (Gemini) e cache (Redis)

## Stack

| Camada | Tecnologia |
|---|---|
| API | FastAPI + Uvicorn |
| Banco de dados | PostgreSQL 16 |
| ORM / Migrations | SQLAlchemy 2 + Alembic |
| Collector / Scheduler | Python + APScheduler |
| Containers | Docker + Docker Compose |
| Linguagem | Python 3.12 |

## Estrutura do projeto

```
meridian/
├── api/                  # FastAPI: routers, schemas, dependencias
├── collector/            # ETL: github_client, pipeline, scheduler
├── core/                 # Logica de dominio pura (transformer, metrics)
├── db/                   # Models SQLAlchemy, session, migrations Alembic
├── ai/                   # Integracao Gemini (Fase 2)
├── config/               # Settings (Pydantic BaseSettings), logger
├── tests/                # Testes unitarios e de integracao
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
└── .env.example
```

## Comecar em 3 passos

### 1. Copiar e preencher o arquivo de variaveis

```bash
cp .env.example .env
# Edite .env e preencha POSTGRES_PASSWORD e GITHUB_TOKEN
```

O `GITHUB_TOKEN` aumenta o rate limit de 60 para 5.000 requests/hora.
Crie um em [github.com/settings/tokens](https://github.com/settings/tokens) (escopo `public_repo`).

### 2. Subir os containers

```bash
docker compose up -d
```

Isso sobe o PostgreSQL, roda as migrations automaticamente e inicia a API e o collector.

### 3. Testar a API

```bash
# Health check
curl http://localhost:8000/health

# Linguagens disponiveis
curl http://localhost:8000/languages

# Top repositorios Python por estrelas
curl "http://localhost:8000/languages/python/ranking?metric=stars&limit=10"

# Repositorios em trending (ultimos 7 dias)
curl "http://localhost:8000/reports/trending?language=go&days=7"
```

Documentacao interativa disponivel em `http://localhost:8000/docs`.

## Endpoints principais

| Metodo | Rota | Descricao |
|---|---|---|
| GET | `/health` | Status da API e conexao com banco |
| GET | `/collector/status` | Ultima execucao do collector |
| GET | `/languages` | Lista linguagens coletadas com contagem |
| GET | `/languages/{lang}/ranking` | Top repos por linguagem (stars, engagement, growth) |
| GET | `/repositories/{id}` | Repositorio com ultimo snapshot de metricas |
| GET | `/repositories/{id}/history` | Serie temporal de snapshots |
| GET | `/repositories/search/` | Busca por nome ou descricao |
| GET | `/reports/trending` | Repos com maior crescimento de estrelas |
| GET | `/reports/weekly` | Relatorio semanal por linguagem |
| GET | `/reports/monthly` | Relatorio mensal por linguagem |

## Configuracao

Todas as variaveis de ambiente estao documentadas em `.env.example`.

Principais:

| Variavel | Default | Descricao |
|---|---|---|
| `GITHUB_TOKEN` | (vazio) | Token GitHub para rate limit elevado |
| `LANGUAGES` | `python,javascript,typescript,go,rust` | Linguagens a coletar |
| `COLLECT_INTERVAL_HOURS` | `6` | Frequencia de coleta em horas |
| `REPOS_PER_LANGUAGE` | `100` | Quantidade de repos por linguagem |
| `AI_ENABLED` | `false` | Ativa integracao com Gemini (Fase 2) |

## Desenvolvimento local (sem Docker)

```bash
# 1. Criar ambiente virtual
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Copiar .env e configurar DATABASE_URL para um Postgres local
cp .env.example .env

# 4. Rodar migrations
alembic upgrade head

# 5. Iniciar a API
uvicorn api.main:app --reload

# 6. Rodar o collector manualmente (coleta uma vez e encerra)
python -c "from collector.pipeline import run_full_collection; run_full_collection()"
```

## Roadmap

- **Fase 1 (atual):** MVP com coleta, API REST, Docker, migrations, logs
- **Fase 2:** Integracao Gemini para resumos de IA, CI/CD com GitHub Actions
- **Fase 3:** Redis cache, Celery workers, alertas por webhook, relatorios em PDF
- **Fase 4:** Dashboard web, autenticacao, Prometheus + Grafana, multiusuario

## Licenca

MIT. Veja [LICENSE](./LICENSE).
