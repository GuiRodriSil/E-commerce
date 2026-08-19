# E-commerce API (FastAPI + SQLAlchemy + PostgreSQL)

## Estrutura
```
ecommerce_api/
├── app/
│   ├── __init__.py
│   ├── database.py    # conexão com o PostgreSQL
│   ├── models.py       # models: User, Category, Product, Order, OrderItem
│   ├── schemas.py       # schemas Pydantic (validação/serialização)
│   └── main.py          # app FastAPI, CORS e rotas
├── requirements.txt
├── .env.example
└── README.md
```

## Como rodar

1. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o banco PostgreSQL. Copie `.env.example` para `.env` e ajuste a URL:
   ```
   DATABASE_URL=postgresql://usuario:senha@host:5432/ecommerce_db
   ```
   (Crie o banco `ecommerce_db` antes, ex: `createdb ecommerce_db`.)

4. Rode a aplicação:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Acesse a documentação interativa (Swagger) em:
   ```
   http://localhost:8000/docs
   ```

## Rotas implementadas

| Método | Rota              | Descrição                                   |
|--------|-------------------|----------------------------------------------|
| GET    | `/products`       | Lista produtos (paginação + filtro categoria) |
| GET    | `/products/{id}`  | Detalhe de um produto                        |
| POST   | `/orders`         | Cria um pedido com itens (produto + qtd)     |

### Exemplo de payload — `POST /orders`
```json
{
  "user_id": 1,
  "items": [
    { "product_id": 3, "quantity": 2 },
    { "product_id": 5, "quantity": 1 }
  ]
}
```

## Observações
- As tabelas são criadas automaticamente na inicialização (`Base.metadata.create_all`).
  Para produção, considere usar **Alembic** para migrations versionadas.
- `POST /orders` valida existência de usuário e produtos, checa estoque e calcula
  o total do pedido automaticamente, decrementando o estoque de cada produto.
- O CORS está liberado para `*` por padrão — restrinja `allow_origins` para os
  domínios reais do seu front-end antes de ir para produção.
- Não há rotas de criação de `User`/`Category`/`Product` neste escopo (apenas as
  solicitadas). Posso adicionar CRUD completo para essas entidades se precisar.
