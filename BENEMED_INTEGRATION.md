# Integração Benemed

Integração com o sistema de checkout da Benemed para planos de saúde PlugZ.

## Configuração

Adicione as variáveis de ambiente no `.env`:

```bash
BENEMED_ENV=hml  # hml para homologação, prod para produção
BENEMED_PARTNER_ID=157
```

## Planos Disponíveis

| Código | Descrição | Valor |
|--------|-----------|-------|
| `26d876219db04110881153441ad585d8` | Plano Essencial PlugZ | R$ 29,90 |
| `720d68006f5f489eb8458d788710b451` | Plano Essencial PlugZ com saúde mental | R$ 49,90 |

## Endpoint

### `GET /benemed/checkout`

Redireciona (302) para o checkout da Benemed com o plano selecionado.

**Query Parameters:**
- `plan_id` (required): ID do plano (um dos códigos acima)

**Exemplo:**
```bash
# Homologação (BENEMED_ENV=hml)
curl -L "http://localhost:8000/benemed/checkout?plan_id=26d876219db04110881153441ad585d8"
# Redireciona para: https://hml.benemedsaude.com.br/checkout?id_plan=26d876219db04110881153441ad585d8&type=Individual&id_parceiro=157

# Produção (BENEMED_ENV=prod)
curl -L "http://localhost:8000/benemed/checkout?plan_id=26d876219db04110881153441ad585d8"
# Redireciona para: https://benemedsaude.com.br/checkout?id_plan=26d876219db04110881153441ad585d8&type=Individual&id_parceiro=157
```

**Resposta:**
- `302 Found` - Redirect para o checkout da Benemed
- `400 Bad Request` - Plano inválido

## URLs Completas

### Homologação (BENEMED_ENV=hml)

**Plano Essencial:**
```
https://hml.benemedsaude.com.br/checkout?id_plan=26d876219db04110881153441ad585d8&type=Individual&id_parceiro=157
```

**Plano Essencial com Saúde Mental:**
```
https://hml.benemedsaude.com.br/checkout?id_plan=720d68006f5f489eb8458d788710b451&type=Individual&id_parceiro=157
```

### Produção (BENEMED_ENV=prod)

**Plano Essencial:**
```
https://benemedsaude.com.br/checkout?id_plan=26d876219db04110881153441ad585d8&type=Individual&id_parceiro=157
```

**Plano Essencial com Saúde Mental:**
```
https://benemedsaude.com.br/checkout?id_plan=720d68006f5f489eb8458d788710b451&type=Individual&id_parceiro=157
```

## Alternar Ambiente

Para alternar entre homologação e produção, basta mudar a variável `BENEMED_ENV` no `.env`:

```bash
# Homologação
BENEMED_ENV=hml

# Produção
BENEMED_ENV=prod
```

Reinicie a aplicação após a mudança.
