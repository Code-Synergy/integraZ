# Univers FastAPI Starter (Proxy/Adapter)

Starter robusto para construir uma API FastAPI que atua como **adapter/proxy** para uma API upstream (ex.: Univers).
Inclui:
- FastAPI async + httpx
- OAuth2 client_credentials com cache de token
- Retry/backoff (tenacity) para erros transitórios
- Timeouts configuráveis
- Correlation-ID (X-Correlation-Id) em request/response + logs
- Rotas: health/ready + primeiro endpoint **Customize**
- Testes: pytest + respx (mock httpx)

> ⚠️ Segredos: use `.env`/variáveis de ambiente. Não comite secrets.

## Requisitos
- Python 3.11+ (recomendado)

## Setup rápido (venv + pip)
```bash
python -m venv .venv
# mac/linux:
source .venv/bin/activate
# windows (powershell):
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
cp .env.example .env
```

## Rodar local
```bash
uvicorn app.main:app --reload
```

Abra:
- Health: http://127.0.0.1:8000/health
- Ready:  http://127.0.0.1:8000/ready
- Docs:   http://127.0.0.1:8000/docs

## Variáveis de ambiente
Ajuste no `.env`:
- `UNIVERS_BASE_URL`
- `UNIVERS_TOKEN_URL`
- `UNIVERS_CLIENT_ID`
- `UNIVERS_CLIENT_SECRET`

## Testes
```bash
pytest -q
```

## Próximos passos sugeridos
1) Implementar `GET /beneficiaries/queries?individualRegistration=...`  
2) Implementar POST/PUT/PATCH de Beneficiary  
3) Implementar import multipart  
4) Padronizar erros e adicionar observabilidade (Prometheus/OpenTelemetry) se necessário
