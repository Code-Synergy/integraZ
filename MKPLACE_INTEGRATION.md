# Integração MkPlace - Autenticação SSO

Integração com MkPlace usando autenticação SSO via JWT (RS256).

## Fluxo de Autenticação

![Fluxo MkPlace](FluxoMkPlace.png)

1. **Geração do Token JWT** - Sistema gera token com informações do cliente
2. **Navegação na Loja** - Cliente usa JWT para gerenciar carrinho, endereços e pedidos
3. **Consulta de Dados** - Endpoint para buscar perfil do cliente
4. **Atualização de Dados** - Endpoint para atualizar informações cadastrais

## Configuração

### Variáveis de Ambiente

```bash
MKPLACE_STORE_ID=advsQsfHwk
MKPLACE_ACCOUNT_ID=advsQsfHwk
MKPLACE_CLIENT_ID=customer-services
MKPLACE_KID=_QGOZ-lCvCnKd0Mvi3d6lKIjHsC51uhfte7EzJfIPmA
MKPLACE_API_URL=https://api.mkplace.com.br
MKPLACE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_HERE
-----END PRIVATE KEY-----
```

### Chave Privada RSA

A chave privada deve ser no formato PEM (RS256). Para gerar um par de chaves:

```bash
# Gerar chave privada
openssl genrsa -out private_key.pem 2048

# Extrair chave pública
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

A chave pública deve ser compartilhada com a MkPlace.

## Endpoints

### `POST /mkplace/auth/token`

Gera um JWT para autenticação SSO do cliente.

**Body:**
```json
{
  "customer_id": "12345",
  "expires_in_days": 365
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9RR09aLWxDdkNuS2QwTXZpM2Q2bEtJakhzQzUxdWhmdGU3RXpKZklQbUEifQ...",
  "token_type": "Bearer",
  "expires_in": 31536000,
  "customer_id": "12345"
}
```

### `GET /mkplace/customer/profile`

Consulta dados cadastrais do cliente na MkPlace.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "customerId": "12345",
  "email": "cliente@email.com",
  "firstName": "João",
  "lastName": "Silva",
  "phone": "11999999999",
  "cpf": "12345678900"
}
```

### `PUT /mkplace/customer/profile`

Atualiza dados cadastrais do cliente.

**Headers:**
```
Authorization: Bearer <token>
```

**Body:**
```json
{
  "email": "novoemail@email.com",
  "firstName": "João",
  "lastName": "Silva",
  "phone": "11999999999"
}
```

## Estrutura do JWT

### Header
```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "_QGOZ-lCvCnKd0Mvi3d6lKIjHsC51uhfte7EzJfIPmA"
}
```

### Payload
```json
{
  "exp": 1775733513,
  "iat": 1744197513,
  "sub": "12345",
  "typ": "Bearer",
  "azp": "customer-services",
  "realm_access": {
    "roles": [
      "oauth/user/read",
      "customer/customer/get",
      "customer/shoppingCart/create",
      "sales/order/checkout",
      "profile:storeId=advsQsfHwk",
      "profile:customerId=12345"
    ]
  },
  "scope": "email openid profile",
  "email_verified": true,
  "clientId": "customer-services",
  "customerId": "12345",
  "storeId": "advsQsfHwk"
}
```

## Roles Incluídas

O token JWT inclui todas as permissões necessárias para:
- Gerenciar carrinho de compras
- Visualizar e atualizar perfil
- Gerenciar endereços
- Realizar checkout e pedidos
- Gerenciar cartões de crédito
- Visualizar histórico de transações
- Participar de programas de fidelidade

## Documentação MkPlace

- API Customer Profile: https://mkplace.stoplight.io/docs/customer/8c46607fd6463-get-customer-profile

## Exemplo de Uso

```python
import httpx

# 1. Gerar token
response = httpx.post("http://localhost:8000/mkplace/auth/token", json={
    "customer_id": "12345",
    "expires_in_days": 365
})
token = response.json()["access_token"]

# 2. Consultar perfil
profile = httpx.get(
    "http://localhost:8000/mkplace/customer/profile",
    headers={"Authorization": f"Bearer {token}"}
)

# 3. Atualizar perfil
httpx.put(
    "http://localhost:8000/mkplace/customer/profile",
    headers={"Authorization": f"Bearer {token}"},
    json={"email": "novoemail@email.com"}
)
```

## Segurança

- Tokens assinados com RS256 (chave privada RSA)
- Validade configurável (padrão: 365 dias)
- Chave privada deve ser mantida em segredo
- Chave pública compartilhada com MkPlace para validação
