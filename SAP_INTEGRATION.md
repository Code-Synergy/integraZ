# Integração SAP Business One

Integração com SAP Business One Service Layer para gerenciamento de parceiros de negócios (clientes e fornecedores).

## Configuração

Adicione as variáveis de ambiente no `.env`:

```bash
SAP_BASE_URL=https://odontohdb:50000
SAP_COMPANY_DB=SBO_SMZTO_TST
SAP_USERNAME=Plugz
SAP_PASSWORD=Ramo01
SAP_CLIENT_SERIES=71        # Série para clientes
SAP_SUPPLIER_SERIES=72      # Série para fornecedores
SAP_GROUP_CODE=106          # Código do grupo padrão
```

## Endpoints

### `GET /sap/business-partners`

Lista todos os parceiros de negócios cadastrados no SAP.

**Exemplo:**
```bash
curl http://localhost:8000/sap/business-partners
```

### `POST /sap/business-partners`

Cria um novo parceiro de negócios (cliente ou fornecedor).

**Body (Cliente):**
```json
{
  "CardName": "JANE DOE",
  "CardType": "C",
  "CardForeignName": "JANE DOE",
  "AliasName": "JANE DOE",
  "Phone1": "11",
  "Phone2": "998980000",
  "EmailAddress": "emailadress@email.com",
  "GroupCode": 106,
  "Series": "71",
  "BPAddresses": [
    {
      "AddressName": "Cobrança",
      "Street": "CONDE DE PORTO ALEGRE",
      "Block": "Floresta",
      "ZipCode": "90220-211",
      "City": "Porto Alegre",
      "County": "4240",
      "Country": "BR",
      "State": "RS",
      "BuildingFloorRoom": "sala 704",
      "AddressType": "bo_BillTo",
      "TypeOfAddress": "Rua",
      "StreetNo": "545"
    },
    {
      "AddressName": "Entrega",
      "Street": "CONDE DE PORTO ALEGRE",
      "Block": "Floresta",
      "ZipCode": "90220-211",
      "City": "Porto Alegre",
      "County": "4240",
      "Country": "BR",
      "State": "RS",
      "BuildingFloorRoom": "sala 704",
      "AddressType": "bo_ShipTo",
      "TypeOfAddress": "Rua",
      "StreetNo": "545"
    }
  ],
  "BPFiscalTaxIDCollection": [
    {
      "Address": "",
      "TaxId0": null,
      "TaxId4": "12345678900"
    }
  ]
}
```

**Body (Fornecedor):**
```json
{
  "CardName": "JANE DOE",
  "CardType": "S",
  "CardForeignName": "JANE DOE",
  "AliasName": "JANE DOE",
  "Phone1": "11",
  "Phone2": "998980000",
  "EmailAddress": "emailadress@email.com",
  "GroupCode": 106,
  "Series": "72",
  "BPAddresses": [...]
}
```

## Tipos de Dados

### CardType
- `C` - Cliente
- `S` - Fornecedor (Supplier)

### AddressType
- `bo_BillTo` - Endereço de cobrança (fixo: "Cobrança")
- `bo_ShipTo` - Endereço de entrega (fixo: "Entrega")

### BPFiscalTaxIDCollection
- `TaxId0` - CNPJ
- `TaxId4` - CPF

## Autenticação

O cliente SAP gerencia automaticamente a autenticação via session cookies. O login é feito automaticamente na primeira requisição e o session ID é reutilizado nas requisições subsequentes.

## Observações

- A série (`Series`) é definida automaticamente baseada no tipo:
  - Cliente (`C`) → usa `SAP_CLIENT_SERIES` (71)
  - Fornecedor (`S`) → usa `SAP_SUPPLIER_SERIES` (72)
- O `GroupCode` usa o valor padrão de `SAP_GROUP_CODE` (106) se não informado
- Endereços de cobrança e entrega são obrigatórios
- O campo `County` deve conter o código IBGE da cidade
