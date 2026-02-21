# Guia de Integração - API IntegráZ (Sandbox)

**Ambiente:** Sandbox  
**Base URL:** http://integra.sandbox.plugz.com.br  
**Versão:** 0.1.0  
**Documentação Interativa:** http://integra.sandbox.plugz.com.br/docs

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Autenticação](#autenticação)
3. [Endpoints Disponíveis](#endpoints-disponíveis)
4. [Integração AGREGA](#integração-agrega)
5. [Integração Univers](#integração-univers)
6. [Exemplos de Código](#exemplos-de-código)
7. [Tratamento de Erros](#tratamento-de-erros)
8. [Migração para Produção](#migração-para-produção)

---

## 1. Visão Geral

A API IntegráZ é um proxy/adapter que centraliza integrações com:
- **AGREGA** - Gestão de leads de energia
- **Univers** - Gestão de beneficiários

### Características:
- ✅ OAuth2 automático (Univers)
- ✅ Retry automático em caso de falha
- ✅ Validação de payload
- ✅ Correlation-ID para rastreamento
- ✅ Logs estruturados

---

## 2. Autenticação

### AGREGA
❌ **Não requer autenticação do cliente**  
A API key é gerenciada internamente pelo backend.

### Univers
❌ **Não requer autenticação do cliente**  
O token OAuth2 é obtido e renovado automaticamente.

---

## 3. Endpoints Disponíveis

### Health Check
```
GET /health
GET /ready
```

### AGREGA
```
POST /agrega/leads
POST /agrega/leads/status
```

### Univers
```
POST /beneficiaries
GET  /beneficiaries/queries?individualRegistration={cpf}
PUT  /beneficiaries/{id}
PATCH /beneficiaries/{id}/status
GET  /store/{store}/customize/configuration
```

---

## 4. Integração AGREGA

### 4.1 Criar Lead

**Endpoint:** `POST /agrega/leads`

**Request:**
```json
{
  "nome": "Razão Social da Empresa",
  "cnpj": "12345678000190",
  "sede": "Rua Exemplo, 123 - São Paulo, SP",
  "id_plataforma": "plugz_user_12345",
  "representante_legal": "João Silva",
  "email": "contato@empresa.com",
  "whatsapp": "11999999999"
}
```

**Validações:**
- `cnpj`: 14 dígitos (apenas números, sem formatação)
- `whatsapp`: 10 ou 11 dígitos (apenas números)
- Todos os campos são obrigatórios

**Response (200 OK):**
```json
{
  "status": "ok",
  "message": "Lead recebido (exemplo)",
  "received": {
    "nome": "Razão Social da Empresa",
    "cnpj": "12345678000190",
    ...
  }
}
```

**Exemplo cURL:**
```bash
curl -X POST "http://integra.sandbox.plugz.com.br/agrega/leads" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Empresa Teste LTDA",
    "cnpj": "12345678000190",
    "sede": "Rua Exemplo, 123",
    "id_plataforma": "plugz_user_001",
    "representante_legal": "João Silva",
    "email": "contato@empresa.com",
    "whatsapp": "11999999999"
  }'
```

---

### 4.2 Atualizar Status do Lead

**Endpoint:** `POST /agrega/leads/status`

**Request:**
```json
{
  "id_plataforma": "plugz_user_12345",
  "status": "inativo"
}
```

**Validações:**
- `status`: Apenas "ativo" ou "inativo"

**Response (200 OK):**
```json
{
  "status": "ok",
  "message": "Status atualizado (exemplo)",
  "received": {
    "id_plataforma": "plugz_user_12345",
    "status": "inativo"
  }
}
```

**Exemplo cURL:**
```bash
curl -X POST "http://integra.sandbox.plugz.com.br/agrega/leads/status" \
  -H "Content-Type: application/json" \
  -d '{
    "id_plataforma": "plugz_user_001",
    "status": "inativo"
  }'
```

---

## 5. Integração Univers

### 5.1 Criar Beneficiário

**Endpoint:** `POST /beneficiaries`

**Request:**
```json
{
  "individualRegistration": "12345678909",
  "name": "João Silva",
  "benefits": [
    {
      "status": 1,
      "kinshipMode": 1,
      "ownershipMode": 1,
      "operatorContractCodes": [31903],
      "identificationNumber": "12345678909",
      "account": {
        "contractLegacyId": 17001,
        "policyLegacyId": 20021,
        "active": 1,
        "limit": 0.0
      }
    }
  ],
  "dependents": [],
  "addresses": [],
  "phones": []
}
```

**Validações:**
- `individualRegistration`: CPF válido (11 dígitos)
- `identificationNumber`: Deve ser igual ao CPF
- `benefits`: Array com pelo menos 1 item

**Response (200 OK):**
```json
{
  "id": "698e1fcc4d06ba0ef951bfbf"
}
```

**Exemplo cURL:**
```bash
curl -X POST "http://integra.sandbox.plugz.com.br/beneficiaries" \
  -H "Content-Type: application/json" \
  -d '{
    "individualRegistration": "12345678909",
    "name": "João Silva",
    "benefits": [{
      "status": 1,
      "kinshipMode": 1,
      "ownershipMode": 1,
      "operatorContractCodes": [31903],
      "identificationNumber": "12345678909",
      "account": {
        "contractLegacyId": 17001,
        "policyLegacyId": 20021,
        "active": 1,
        "limit": 0.0
      }
    }],
    "dependents": [],
    "addresses": [],
    "phones": []
  }'
```

---

### 5.2 Buscar Beneficiário

**Endpoint:** `GET /beneficiaries/queries?individualRegistration={cpf}`

**Query Parameters:**
- `individualRegistration` (required): CPF do beneficiário (11 dígitos)

**Response (200 OK):**
```json
{
  "content": [
    {
      "id": "698e1b944d06ba0ef951bfb1",
      "name": "João Silva",
      "individualRegistration": "12345678909",
      "createdAt": "2026-02-12T15:27:32",
      "benefits": [...],
      "addresses": [],
      "phones": []
    }
  ],
  "totalElements": 1,
  "totalPages": 1
}
```

**Exemplo cURL:**
```bash
curl "http://integra.sandbox.plugz.com.br/beneficiaries/queries?individualRegistration=12345678909"
```

---

### 5.3 Atualizar Beneficiário

**Endpoint:** `PUT /beneficiaries/{id}`

**Request:** (mesmo formato do POST)

**Exemplo cURL:**
```bash
curl -X PUT "http://integra.sandbox.plugz.com.br/beneficiaries/698e1fcc4d06ba0ef951bfbf" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

---

### 5.4 Atualizar Status do Beneficiário

**Endpoint:** `PATCH /beneficiaries/{id}/status`

**Request:**
```json
{
  "status": "TEMPORARY_BLOCKED",
  "policyLegacyId": 20021,
  "contractLegacyId": 17001,
  "blockOperatorCode": 31903
}
```

**Exemplo cURL:**
```bash
curl -X PATCH "http://integra.sandbox.plugz.com.br/beneficiaries/698e1fcc4d06ba0ef951bfbf/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "TEMPORARY_BLOCKED",
    "policyLegacyId": 20021,
    "contractLegacyId": 17001,
    "blockOperatorCode": 31903
  }'
```

---

## 6. Exemplos de Código

### JavaScript/TypeScript (fetch)

```javascript
// Criar Lead AGREGA
async function criarLead(dados) {
  const response = await fetch('http://integra.sandbox.plugz.com.br/agrega/leads', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      nome: dados.razaoSocial,
      cnpj: dados.cnpj.replace(/\D/g, ''), // Remove formatação
      sede: dados.endereco,
      id_plataforma: dados.userId,
      representante_legal: dados.representante,
      email: dados.email,
      whatsapp: dados.telefone.replace(/\D/g, ''), // Remove formatação
    }),
  });
  
  if (!response.ok) {
    throw new Error(`Erro: ${response.status}`);
  }
  
  return response.json();
}

// Buscar Beneficiário Univers
async function buscarBeneficiario(cpf) {
  const cpfLimpo = cpf.replace(/\D/g, '');
  const response = await fetch(
    `http://integra.sandbox.plugz.com.br/beneficiaries/queries?individualRegistration=${cpfLimpo}`
  );
  
  if (!response.ok) {
    throw new Error(`Erro: ${response.status}`);
  }
  
  return response.json();
}
```

---

### Python (requests)

```python
import requests

# Criar Lead AGREGA
def criar_lead(dados):
    url = "http://integra.sandbox.plugz.com.br/agrega/leads"
    payload = {
        "nome": dados["razao_social"],
        "cnpj": dados["cnpj"].replace(".", "").replace("/", "").replace("-", ""),
        "sede": dados["endereco"],
        "id_plataforma": dados["user_id"],
        "representante_legal": dados["representante"],
        "email": dados["email"],
        "whatsapp": dados["telefone"].replace("(", "").replace(")", "").replace("-", "").replace(" ", ""),
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

# Buscar Beneficiário Univers
def buscar_beneficiario(cpf):
    cpf_limpo = cpf.replace(".", "").replace("-", "")
    url = f"http://integra.sandbox.plugz.com.br/beneficiaries/queries?individualRegistration={cpf_limpo}"
    
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

---

## 7. Tratamento de Erros

### Códigos HTTP

| Código | Descrição | Ação |
|--------|-----------|------|
| 200 | Sucesso | Processar resposta |
| 400 | Erro de validação | Verificar payload |
| 404 | Não encontrado | Recurso não existe |
| 422 | Validação falhou | Corrigir campos inválidos |
| 500 | Erro interno | Tentar novamente ou contatar suporte |

### Exemplo de Erro (422)

```json
{
  "detail": [
    {
      "type": "string_pattern_mismatch",
      "loc": ["body", "cnpj"],
      "msg": "String should match pattern '^\\d{14}$'",
      "input": "123",
      "ctx": {
        "pattern": "^\\d{14}$"
      }
    }
  ]
}
```

### Exemplo de Erro (404)

```json
{
  "detail": {
    "message": "Erro ao buscar beneficiário: Beneficiário não encontrado",
    "upstream": {
      "message": "Beneficiário não encontrado",
      "description": "Verifique os dados e tente novamente"
    },
    "correlationId": "b609d91a-c399-4846-8571-bf46233a63ec"
  }
}
```

### Tratamento Recomendado

```javascript
try {
  const result = await criarLead(dados);
  console.log('Lead criado:', result);
} catch (error) {
  if (error.response?.status === 422) {
    // Erro de validação - mostrar para usuário
    console.error('Dados inválidos:', error.response.data.detail);
  } else if (error.response?.status === 500) {
    // Erro interno - tentar novamente
    console.error('Erro no servidor, tente novamente');
  } else {
    console.error('Erro desconhecido:', error);
  }
}
```

---

## 8. Migração para Produção

### Checklist

- [ ] Atualizar Base URL para produção
- [ ] Configurar timeout adequado (recomendado: 30s)
- [ ] Implementar retry no cliente (3 tentativas)
- [ ] Adicionar logging de erros
- [ ] Configurar monitoramento
- [ ] Testar todos os endpoints em produção
- [ ] Validar Correlation-ID nos logs

### URLs por Ambiente

| Ambiente | Base URL |
|----------|----------|
| Sandbox | http://integra.sandbox.plugz.com.br |
| Produção | *A definir* |

### Variáveis de Ambiente Recomendadas

```javascript
// .env
INTEGRAZ_API_URL=http://integra.sandbox.plugz.com.br
INTEGRAZ_TIMEOUT=30000
INTEGRAZ_RETRY_ATTEMPTS=3
```

---

## 9. Suporte

### Documentação Interativa
- Swagger UI: http://integra.sandbox.plugz.com.br/docs
- ReDoc: http://integra.sandbox.plugz.com.br/redoc

### Health Check
Antes de fazer chamadas, verifique se a API está online:
```bash
curl http://integra.sandbox.plugz.com.br/health
```

### Correlation-ID
Todas as respostas incluem um `X-Correlation-Id` no header. Use-o para rastrear requisições nos logs.

---

## 10. Boas Práticas

✅ **Sempre remover formatação** de CNPJ e telefone antes de enviar  
✅ **Validar CPF** no frontend antes de enviar  
✅ **Implementar retry** para erros 5xx  
✅ **Usar timeout** de 30 segundos  
✅ **Logar Correlation-ID** para debug  
✅ **Tratar erros** de forma amigável para o usuário  
✅ **Testar em sandbox** antes de produção  

---

**Documento gerado em:** 2026-02-12  
**Versão:** 1.0  
**Contato:** Time de Backend
