# Docker - Guia Rápido

## Build e Run

### Usando Docker
```bash
# Build
docker build -t integraz-api .

# Run
docker run -p 8000:8000 --env-file .env integraz-api
```

### Usando Docker Compose (Recomendado)
```bash
# Subir
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down

# Rebuild
docker-compose up -d --build
```

## Testar

```bash
# Health check
curl http://localhost:8000/health

# Docs
open http://localhost:8000/docs

# Criar lead AGREGA
curl -X POST http://localhost:8000/agrega/leads \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Empresa Teste",
    "cnpj": "00000000000100",
    "sede": "Rua Exemplo",
    "id_plataforma": "sandbox",
    "representante_legal": "João Silva",
    "email": "teste@teste.com",
    "whatsapp": "11999999999"
  }'
```

## Configuração

1. Copie `.env.example` para `.env`
2. Ajuste as variáveis de ambiente
3. Execute `docker-compose up -d`

## Deploy

### AWS ECS/Fargate
```bash
# Build para ECR
docker build -t integraz-api .
docker tag integraz-api:latest <account>.dkr.ecr.<region>.amazonaws.com/integraz-api:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/integraz-api:latest
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: integraz-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: integraz-api
  template:
    metadata:
      labels:
        app: integraz-api
    spec:
      containers:
      - name: api
        image: integraz-api:latest
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: integraz-secrets
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```
