# Integração  Partner Hub

## Informações necessárias para solicitar à 

Para viabilizar a implementação da integração com o Partner Hub da , você precisará solicitar as seguintes informações:

### 1. Credenciais de Acesso (OBRIGATÓRIO)
- **API Key / Bearer Token**: Token de autenticação para acessar a API Partner Hub
- **Ambiente**: 
  - URL base de produção: `https://partnerhubapi..com.br`
  - URL base de sandbox/homologação (se disponível)

### 2. Documentação Técnica
- Acesso completo à documentação da API: https://partnerhubapi..com.br/reference
- Exemplos de payloads para criação de lojista
- Códigos de erro e suas descrições
- Rate limits da API

### 3. Informações de Negócio
- **MCC (Merchant Category Code)**: Código de categoria do estabelecimento que será usado
- **Ofertas disponíveis**: Quais produtos/ofertas podem ser associados aos lojistas
- **Fluxo de aprovação**: Como funciona o processo de aprovação de lojistas
- **Webhooks**: Se há notificações de mudança de status (aprovado, rejeitado, etc)

### 4. Dados Bancários
- Quais bancos são aceitos (códigos bancários válidos)
- Tipos de conta aceitos (corrente, poupança)
- Validações específicas para dados bancários

### 5. Ambiente de Testes
- Credenciais de sandbox para testes
- Dados fictícios que podem ser usados para testes (CNPJs, etc)
- Como simular diferentes cenários (aprovação, rejeição, etc)

### 6. Suporte Técnico
- Canal de suporte para dúvidas técnicas durante a integração
- SLA de resposta
- Contato técnico da 

---

## Estrutura Implementada

A integração foi criada no módulo `app//` com:

### Arquivos criados:
- `app/clients/.py` - Cliente HTTP para Partner Hub API
- `app//schemas.py` - Modelos Pydantic para request/response
- `app//routes.py` - Endpoints FastAPI

### Endpoints disponíveis:
- `POST //merchants` - Criar novo lojista
- `GET //merchants` - Listar lojistas (com paginação)
- `GET //merchants/{_code}` - Obter detalhes de um lojista

### Variáveis de ambiente necessárias:
```bash
_BASE_URL=https://partnerhubapi..com.br
_API_KEY=seu_token_aqui
```

### Próximos passos após receber as credenciais:
1. Adicionar as variáveis no arquivo `.env`
2. Validar os schemas com exemplos reais da documentação 
3. Implementar testes com dados de sandbox
4. Ajustar campos obrigatórios/opcionais conforme documentação
5. Implementar tratamento de erros específicos da 
6. Adicionar webhooks se disponível
