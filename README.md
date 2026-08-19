# Pulse Market

Aplicação de e-commerce com frontend em Vue 3 e Tailwind CSS, API em FastAPI, persistência em PostgreSQL e autenticação por JWT.

## Visão geral

O projeto está dividido em duas aplicações:

```text
E-commerce/
├── ecommerce_api/       # API FastAPI + SQLAlchemy + PostgreSQL
└── ecommerce_frontend/  # Vue 3 + Vite + Pinia + Tailwind CSS
```

### Funcionalidades

- Catálogo com 50 produtos e 10 produtos por categoria
- Busca com autocomplete em tempo real
- Filtros por categoria em botões/pílulas
- Produtos em oferta com preço original riscado e preço promocional
- Página de detalhes com zoom da imagem principal
- Breadcrumbs com navegação para a categoria filtrada
- Produtos relacionados por categoria
- Histórico dos 6 últimos produtos visitados, persistido no `localStorage`
- Wishlist persistida no `localStorage`
- Carrinho persistido por usuário e limitado ao estoque disponível
- Drawer do carrinho e modal de confirmação após adicionar um produto
- Alternância entre Dark Mode e Light Mode, persistida no `localStorage`
- Checkout e integração com Mercado Pago
- Chat de suporte com Gemini

## Pré-requisitos

- Python 3.11 ou superior
- Node.js 18 ou superior e npm
- PostgreSQL 14 ou superior
- Banco PostgreSQL criado, por exemplo `ecommerce_db`

## Configuração da API

No Windows, abra um terminal na raiz do projeto:

```powershell
cd ecommerce_api
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

No Linux/macOS:

```bash
cd ecommerce_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edite o arquivo `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ecommerce_db
JWT_SECRET_KEY=troque-por-uma-chave-segura
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
GEMINI_API_KEY=sua-chave-do-gemini
GEMINI_MODEL=gemini-3.6-flash
GEMINI_FALLBACK_MODEL=gemini-3.5-flash
MERCADO_PAGO_ACCESS_TOKEN=seu-token-do-mercado-pago
```

`DATABASE_URL` é a única configuração necessária para catálogo, autenticação e pedidos. `GEMINI_API_KEY` é necessária para o chat e o token do Mercado Pago para pagamentos reais.

As tabelas são criadas automaticamente ao importar a aplicação. Para ambientes de produção, use migrations versionadas com Alembic.

## Popular o catálogo

Com o ambiente virtual ativo e o PostgreSQL disponível:

```powershell
python seed_products.py
```

O script é idempotente: produtos existentes não são duplicados. Ele cria as categorias e os produtos ausentes.

## Executar a API

Dentro de `ecommerce_api`:

```powershell
uvicorn app.main:app --reload
```

A API ficará disponível em `http://localhost:8000`.

Documentação interativa:

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/`

## Executar o frontend

Em outro terminal:

```powershell
cd ecommerce_frontend
npm install
npm run dev
```

O frontend ficará disponível em `http://localhost:5173`.

Para gerar e testar o build de produção:

```powershell
npm run build
npm run preview
```

O frontend espera a API em `http://localhost:8000`. Se a API estiver indisponível, a Home usa o catálogo local como fallback para a listagem e os filtros.

## Rotas da API

### Saúde, autenticação e usuário

| Método | Rota | Descrição | Auth |
| --- | --- | --- | --- |
| GET | `/` | Health check | Não |
| POST | `/register` | Cria uma conta e retorna JWT | Não |
| POST | `/login` | Autentica o usuário e retorna JWT | Não |
| GET | `/users/me` | Retorna perfil e pedidos | Bearer |
| PUT | `/users/me` | Atualiza nome e/ou senha | Bearer |

### Produtos

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/products` | Lista produtos ativos com busca, categoria, paginação e limite |
| GET | `/products/{product_id}` | Retorna o detalhe de um produto |
| GET | `/products/{product_id}/related` | Retorna até 4 produtos ativos da mesma categoria, excluindo o produto atual |

Exemplos:

```text
GET /products?search=notebook&limit=20
GET /products?category=Audio
GET /products/1/related
```

### Pedidos, checkout e pagamentos

| Método | Rota | Descrição | Auth |
| --- | --- | --- | --- |
| POST | `/orders` | Cria um pedido, valida estoque e calcula o total | Bearer |
| POST | `/checkout` | Valida checkout do usuário autenticado | Bearer |
| POST | `/payments/mercadopago` | Cria pagamento no Mercado Pago | Bearer |

Exemplo de `POST /orders`:

```json
{
  "user_id": 1,
  "items": [
    { "product_id": 3, "quantity": 2 },
    { "product_id": 5, "quantity": 1 }
  ]
}
```

### Suporte

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/support/tickets` | Cria um chamado e retorna um protocolo |
| POST | `/api/chat` | Envia uma pergunta ao atendente Gemini |

## Testes

Com o ambiente virtual ativo:

```powershell
cd ecommerce_api
python -m pytest tests -q
```

Os testes cobrem autenticação, proteção de checkout/pagamentos, suporte e chat.

Também é possível validar a sintaxe dos scripts:

```powershell
python -m py_compile app/main.py seed_products.py
```

## Estrutura principal

```text
ecommerce_api/
├── app/
│   ├── auth.py       # JWT, hash de senha e middleware de proteção
│   ├── database.py   # conexão e sessões SQLAlchemy
│   ├── main.py       # aplicação FastAPI e endpoints
│   ├── models.py     # User, Category, Product, Order e suporte
│   └── schemas.py    # contratos Pydantic da API
├── tests/
├── requirements.txt
├── seed_products.py
└── .env.example

ecommerce_frontend/
├── src/
│   ├── components/   # Navbar, carrinho, breadcrumbs e UI reutilizável
│   ├── data/         # catálogo local de fallback
│   ├── pages/        # Home, detalhes, carrinho, checkout e conta
│   ├── stores/       # auth, carrinho, wishlist e histórico
│   └── utils/        # normalização da busca
├── package.json
├── tailwind.config.js
└── vite.config.js
```

## Solução de problemas

### A API não conecta ao PostgreSQL

Confirme se o serviço está em execução, se o banco existe e se `DATABASE_URL` contém usuário, senha, host, porta e nome corretos.

### O frontend exibe produtos, mas não carrega dados da API

Verifique se o backend está rodando em `http://localhost:8000`. A Home possui fallback para o catálogo local, mas detalhes relacionados e operações de conta dependem da API.

### O PowerShell bloqueia a ativação da virtualenv

Execute o PowerShell como usuário e, se necessário, permita scripts para a sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## Notas de produção

- Troque `JWT_SECRET_KEY` por uma chave longa e aleatória.
- Restrinja o CORS aos domínios reais do frontend.
- Não versionar `.env` nem tokens de serviços externos.
- Use Alembic para migrations e um PostgreSQL gerenciado.
- Configure HTTPS, logs, monitoramento e limites de requisição antes do deploy.
