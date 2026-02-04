# API AGREGA - Documentação para Frontend

Base URL: `http://seu-servidor:8000`

## 1. Criar Lead

**Endpoint:** `POST /agrega/leads`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "nome": "Empresa Exemplo LTDA",
  "cnpj": "12345678000190",
  "sede": "Rua Exemplo, 123 - São Paulo, SP",
  "id_plataforma": "plugz_user_12345",
  "representante_legal": "João Silva",
  "email": "joao.silva@empresa.com",
  "whatsapp": "11999999999"
}
```

**Validações:**
- `cnpj`: Apenas números, 14 dígitos (sem pontos, barras ou traços)
- `whatsapp`: Apenas números, 10 ou 11 dígitos (sem parênteses, espaços ou traços)
- Todos os campos são obrigatórios

**Resposta de Sucesso (200):**
```json
{
  "status": "ok",
  "message": "Lead recebido (exemplo)",
  "received": {
    "nome": "Empresa Exemplo LTDA",
    "cnpj": "12345678000190",
    "sede": "Rua Exemplo, 123 - São Paulo, SP",
    "id_plataforma": "plugz_user_12345",
    "representante_legal": "João Silva",
    "email": "joao.silva@empresa.com",
    "whatsapp": "11999999999"
  }
}
```

**Resposta de Erro (400 - Validação):**
```json
{
  "detail": [
    {
      "type": "string_pattern_mismatch",
      "loc": ["body", "cnpj"],
      "msg": "String should match pattern '^\\d{14}$'",
      "input": "12.345.678/0001-90"
    }
  ]
}
```

**Exemplo cURL:**
```bash
curl -X POST "http://seu-servidor:8000/agrega/leads" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Empresa Exemplo LTDA",
    "cnpj": "12345678000190",
    "sede": "Rua Exemplo, 123 - São Paulo, SP",
    "id_plataforma": "plugz_user_12345",
    "representante_legal": "João Silva",
    "email": "joao.silva@empresa.com",
    "whatsapp": "11999999999"
  }'
```

**Exemplo JavaScript (fetch):**
```javascript
const criarLead = async (dadosLead) => {
  try {
    const response = await fetch('http://seu-servidor:8000/agrega/leads', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        nome: dadosLead.razaoSocial,
        cnpj: dadosLead.cnpj.replace(/\D/g, ''), // Remove formatação
        sede: dadosLead.endereco,
        id_plataforma: dadosLead.userId,
        representante_legal: dadosLead.representante,
        email: dadosLead.email,
        whatsapp: dadosLead.telefone.replace(/\D/g, ''), // Remove formatação
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail?.message || 'Erro ao criar lead');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao criar lead:', error);
    throw error;
  }
};

// Uso:
criarLead({
  razaoSocial: 'Empresa Exemplo LTDA',
  cnpj: '12.345.678/0001-90', // Pode vir formatado
  endereco: 'Rua Exemplo, 123 - São Paulo, SP',
  userId: 'plugz_user_12345',
  representante: 'João Silva',
  email: 'joao.silva@empresa.com',
  telefone: '(11) 99999-9999', // Pode vir formatado
})
  .then(response => console.log('Lead criado:', response))
  .catch(error => console.error('Erro:', error));
```

---

## 2. Atualizar Status do Lead

**Endpoint:** `POST /agrega/leads/status`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "id_plataforma": "plugz_user_12345",
  "status": "inativo"
}
```

**Validações:**
- `status`: Apenas `"ativo"` ou `"inativo"`
- Ambos os campos são obrigatórios

**Resposta de Sucesso (200):**
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

**Resposta de Erro (400 - Status inválido):**
```json
{
  "detail": [
    {
      "type": "literal_error",
      "loc": ["body", "status"],
      "msg": "Input should be 'ativo' or 'inativo'",
      "input": "pendente"
    }
  ]
}
```

**Exemplo cURL:**
```bash
curl -X POST "http://seu-servidor:8000/agrega/leads/status" \
  -H "Content-Type: application/json" \
  -d '{
    "id_plataforma": "plugz_user_12345",
    "status": "inativo"
  }'
```

**Exemplo JavaScript (fetch):**
```javascript
const atualizarStatusLead = async (userId, novoStatus) => {
  try {
    const response = await fetch('http://seu-servidor:8000/agrega/leads/status', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id_plataforma: userId,
        status: novoStatus, // 'ativo' ou 'inativo'
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail?.message || 'Erro ao atualizar status');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao atualizar status:', error);
    throw error;
  }
};

// Uso:
atualizarStatusLead('plugz_user_12345', 'inativo')
  .then(response => console.log('Status atualizado:', response))
  .catch(error => console.error('Erro:', error));
```

---

## Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200    | Sucesso |
| 400    | Erro de validação (campos inválidos) |
| 500    | Erro interno do servidor |

---

## Observações Importantes

1. **CNPJ e Whatsapp**: Sempre enviar apenas números (sem formatação)
2. **id_plataforma**: Usar identificador único do usuário no sistema PlugZ
3. **Correlation-ID**: A API adiciona automaticamente para rastreamento
4. **Retry**: A API já possui retry automático para erros transitórios
5. **Documentação Interativa**: Disponível em `http://seu-servidor:8000/docs`

---

## Health Check

**Endpoint:** `GET /health`

**Resposta:**
```json
{
  "status": "ok"
}
```

Use para verificar se a API está disponível antes de fazer chamadas.
