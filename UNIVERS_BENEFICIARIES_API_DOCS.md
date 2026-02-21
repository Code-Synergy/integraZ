# API Univers Beneficiários - Documentação

Base URL: `http://seu-servidor:8000`

## 1. Criar Beneficiário

**Endpoint:** `POST /beneficiaries`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "individualRegistration": "0423",
  "name": "Marco Aurélio Siqueira",
  "benefits": [
    {
      "status": 1,
      "kinshipMode": 1,
      "ownershipMode": 1,
      "operatorContractCodes": [31903],
      "identificationNumber": "1750751000002011",
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

**Exemplo cURL:**
```bash
curl -X POST "http://localhost:8000/beneficiaries" \
  -H "Content-Type: application/json" \
  -d '{
    "individualRegistration": "0423",
    "name": "Marco Aurélio Siqueira",
    "benefits": [
      {
        "status": 1,
        "kinshipMode": 1,
        "ownershipMode": 1,
        "operatorContractCodes": [31903],
        "identificationNumber": "1750751000002011",
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
  }'
```

---

## 2. Buscar Beneficiário

**Endpoint:** `GET /beneficiaries/queries`

**Query Parameters:**
- `individualRegistration` (required): CPF do beneficiário

**Exemplo cURL:**
```bash
curl "http://localhost:8000/beneficiaries/queries?individualRegistration=05455037790"
```

---

## 3. Atualizar Beneficiário

**Endpoint:** `PUT /beneficiaries/{beneficiary_id}`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "individualRegistration": "1234",
  "name": "Marco Aurelio Siqueira Filho",
  "benefits": [
    {
      "status": 1,
      "kinshipMode": 1,
      "ownershipMode": 1,
      "operatorContractCodes": [31903],
      "identificationNumber": "1750751000002011",
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

**Exemplo cURL:**
```bash
curl -X PUT "http://localhost:8000/beneficiaries/68ed1d83c20c6e357e266165" \
  -H "Content-Type: application/json" \
  -d '{
    "individualRegistration": "1234",
    "name": "Marco Aurelio Siqueira Filho",
    "benefits": [
      {
        "status": 1,
        "kinshipMode": 1,
        "ownershipMode": 1,
        "operatorContractCodes": [31903],
        "identificationNumber": "1750751000002011",
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
  }'
```

---

## 4. Atualizar Status do Beneficiário

**Endpoint:** `PATCH /beneficiaries/{beneficiary_id}/status`

**Headers:**
```
Content-Type: application/json
```

**Body:**
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
curl -X PATCH "http://localhost:8000/beneficiaries/339290647/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "TEMPORARY_BLOCKED",
    "policyLegacyId": 20021,
    "contractLegacyId": 17001,
    "blockOperatorCode": 31903
  }'
```

---

## Observações

- ✅ **OAuth2 automático**: Token obtido e renovado automaticamente
- ✅ **Retry**: 3 tentativas automáticas em caso de erro transitório
- ✅ **Correlation-ID**: Adicionado automaticamente para rastreamento
- ✅ **Validação**: Payload validado antes de enviar para Univers
- ✅ **Logs estruturados**: Todas as requisições são logadas

---

## Exemplo JavaScript

```javascript
// Criar beneficiário
const criarBeneficiario = async (dados) => {
  const response = await fetch('http://localhost:8000/beneficiaries', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados),
  });
  return response.json();
};

// Buscar beneficiário
const buscarBeneficiario = async (cpf) => {
  const response = await fetch(
    `http://localhost:8000/beneficiaries/queries?individualRegistration=${cpf}`
  );
  return response.json();
};

// Atualizar beneficiário
const atualizarBeneficiario = async (id, dados) => {
  const response = await fetch(`http://localhost:8000/beneficiaries/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados),
  });
  return response.json();
};

// Atualizar status
const atualizarStatus = async (id, status) => {
  const response = await fetch(`http://localhost:8000/beneficiaries/${id}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(status),
  });
  return response.json();
};
```
