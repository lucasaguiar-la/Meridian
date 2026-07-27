# Meridian

Plataforma de insights sobre repositórios do GitHub por linguagem. Coleta dados em tempo real via API do GitHub, armazena histórico de métricas e disponibiliza rankings, tendências e análises via API REST e interface web.

## Stack

| Camada | Tecnologia |
|---|---|
| Frontend | React 18 + Vite + Tailwind CSS |
| API | FastAPI + Uvicorn |
| Banco de dados | PostgreSQL 16 |
| ORM / Migrations | SQLAlchemy 2 + Alembic |
| Collector | Python + APScheduler |
| Containers | Docker + Docker Compose |

## Funcionalidades

- Coleta automatizada dos top repositórios por linguagem (Python, JavaScript, TypeScript, Go, Rust e mais)
- Histórico de métricas com snapshots diários (estrelas, forks, issues, engagement score)
- Rankings por linguagem com ordenação por estrelas, engajamento ou crescimento
- Trending: repositórios com maior crescimento de estrelas nos últimos 7 ou 30 dias
- Busca por nome ou descrição com filtro de linguagem
- Detalhe do repositório com gráfico histórico de estrelas
- API REST documentada com Swagger UI
- Logs estruturados (JSON), health checks e registro de cada execução do collector

---

## Subir tudo com Docker Compose

Esta é a forma recomendada. Sobe o banco, a API, o collector e o frontend com um único comando.

### 1. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Editar `.env` e preencher:

```
POSTGRES_PASSWORD=sua_senha_aqui
GITHUB_TOKEN=ghp_seu_token_aqui
```

O `GITHUB_TOKEN` aumenta o rate limit de 60 para 5.000 requests/hora.
Crie um em [github.com/settings/tokens](https://github.com/settings/tokens) (escopo `public_repo` é suficiente).

### 2. Subir os containers

```bash
docker compose up -d
```

Aguarde alguns segundos para o banco inicializar e as migrations rodarem. Depois:

| Serviço | URL |
|---|---|
| Frontend | http://localhost:3000 |
| API (Swagger UI) | http://localhost:8000/docs |
| API (health check) | http://localhost:8000/health |

### 3. Verificar status

```bash
docker compose ps
docker compose logs api
docker compose logs collector
```

---

## Desenvolvimento local (sem Docker)

### Backend

Pré-requisito: PostgreSQL rodando localmente.

```bash
# Criar e ativar ambiente virtual
python -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # Linux / macOS

# Instalar dependências
pip install -r requirements.txt

# Copiar e configurar variáveis
cp .env.example .env
# Editar .env: DATABASE_URL, GITHUB_TOKEN

# Rodar migrations
alembic upgrade head

# Iniciar a API (modo reload para desenvolvimento)
uvicorn api.main:app --reload --port 8000
```

Rodar o collector manualmente (uma única coleta):

```bash
python -c "from collector.pipeline import run_full_collection; run_full_collection()"
```

### Frontend

Pré-requisito: Node.js 20+. A API deve estar rodando em `localhost:8000`.

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

Abre em `http://localhost:5173`. O Vite faz proxy automático de `/api` para `localhost:8000`, sem CORS.

```bash
# Build de produção
npm run build
npm run preview   # visualizar o build localmente
```

---

## Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Status da API e conexão com banco |
| GET | `/collector/status` | Última execução do collector |
| GET | `/languages` | Lista de linguagens coletadas com contagem |
| GET | `/languages/{lang}/ranking` | Top repos por linguagem (`metric`: stars, engagement, growth) |
| GET | `/languages/{lang}/market` | Vagas de emprego abertas por linguagem (fonte: Adzuna, requer `ADZUNA_APP_ID`/`ADZUNA_APP_KEY`) |
| GET | `/repositories/{id}` | Repositório com último snapshot de métricas |
| GET | `/repositories/{id}/history` | Série temporal de snapshots (`days`: 1-365) |
| GET | `/repositories/search/` | Busca por nome ou descrição |
| GET | `/reports/trending` | Repos com maior crescimento (`days`: 7 ou 30) |
| GET | `/reports/weekly` | Relatório semanal por linguagem |
| GET | `/reports/monthly` | Relatório mensal por linguagem |

Documentação interativa completa em `http://localhost:8000/docs`.

---

## Estrutura do projeto

```
meridian/
├── api/                  # FastAPI: routers, schemas, dependencias
├── collector/            # ETL: github_client, pipeline, scheduler
├── core/                 # Logica de dominio pura (transformer, metrics)
├── db/                   # Models SQLAlchemy, session, migrations Alembic
├── ai/                   # Integracao Gemini (Fase 2)
├── config/               # Settings (Pydantic BaseSettings), logger
├── frontend/             # React + Vite + Tailwind CSS
│   ├── src/
│   │   ├── api/          # client.js: funções fetch para a API
│   │   ├── components/   # Navbar, RepoCard, HistoryChart, badges...
│   │   └── pages/        # Home, Ranking, Trending, RepoDetail, Search
│   ├── Dockerfile
│   └── nginx.conf
├── tests/
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
└── .env.example
```

---

## Roadmap

- **Fase 1 (atual):** MVP com coleta, API REST, frontend React, Docker, migrations, logs
- **Fase 2:** Integração Gemini para resumos de IA, CI/CD com GitHub Actions
- **Fase 3:** Redis cache, Celery workers, alertas por webhook, relatórios em PDF
- **Fase 4:** Dashboard avançado, autenticação, Prometheus + Grafana, multiusuário

---

## Licença

MIT. Veja [LICENSE](./LICENSE).
