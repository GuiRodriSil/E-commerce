import os
from typing import List

import mercadopago
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.auth import (
    auth_middleware,
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.database import Base, engine, get_db

# Cria as tabelas no banco (em produção, prefira Alembic para migrations)
Base.metadata.create_all(bind=engine)

sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_ACCESS_TOKEN", "TEST-0000000000000000-000000-000000000000000000000000000000000000"))

app = FastAPI(
    title="E-commerce API",
    description="API REST para e-commerce com FastAPI + SQLAlchemy + PostgreSQL",
    version="1.0.0",
)

# --------------------------------------------------------------------------
# CORS
# --------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(auth_middleware)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "ecommerce-api"}


# --------------------------------------------------------------------------
# Auth
# --------------------------------------------------------------------------
@app.post("/register", response_model=schemas.TokenOut, status_code=status.HTTP_201_CREATED, tags=["auth"])
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado")

    user = models.User(
        name=user_in.name,
        email=str(user_in.email),
        hashed_password=hash_password(user_in.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/login", response_model=schemas.TokenOut, tags=["auth"])
def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == str(user_in.email)).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


# --------------------------------------------------------------------------
# Products
# --------------------------------------------------------------------------
@app.get("/products", response_model=List[schemas.ProductOut], tags=["products"])
def list_products(
    skip: int = 0,
    limit: int = 20,
    category_id: int | None = None,
    search: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
):
    """Lista produtos ativos com busca textual e filtros opcionais."""
    query = db.query(models.Product).options(joinedload(models.Product.category))
    query = query.filter(models.Product.is_active == True)  # noqa: E712

    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)

    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                models.Product.name.ilike(search_pattern),
                models.Product.description.ilike(search_pattern),
            )
        )

    if category:
        query = query.join(models.Category).filter(models.Category.name.ilike(category.strip()))

    products = query.offset(skip).limit(limit).all()
    return products


@app.get("/products/{product_id}", response_model=schemas.ProductOut, tags=["products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retorna um produto específico pelo ID."""
    product = (
        db.query(models.Product)
        .options(joinedload(models.Product.category))
        .filter(models.Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return product


# --------------------------------------------------------------------------
# Checkout / Orders
# --------------------------------------------------------------------------
@app.post("/checkout", status_code=status.HTTP_201_CREATED, tags=["checkout"])
def checkout(current_user: models.User = Depends(get_current_user)):
    return {"message": "Checkout autorizado", "user_id": current_user.id}


@app.post("/payments/mercadopago/pix", response_model=schemas.PaymentResponse, tags=["payments"])
def create_pix_payment(payment_in: schemas.PaymentCreate):
    if not payment_in.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O carrinho precisa ter pelo menos um item")

    total = sum(item.quantity * item.unit_price for item in payment_in.items)
    if total <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O valor total deve ser maior que zero")

    preference_data = {
        "items": [
            {
                "id": str(item.id),
                "title": item.title,
                "quantity": item.quantity,
                "currency_id": "BRL",
                "unit_price": float(item.unit_price),
            }
            for item in payment_in.items
        ],
        "payer": {"email": payment_in.payer_email},
        "payment_methods": {"excluded_payment_types": [{"id": "ticket"}], "installments": 1},
        "back_urls": {"success": "http://localhost:5173", "failure": "http://localhost:5173", "pending": "http://localhost:5173"},
        "auto_return": "approved",
    }

    try:
        response = sdk.preference().create(preference_data)
        payment = response.get("response", {})
        if not payment:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Erro ao criar pagamento no Mercado Pago")

        qr_code = payment.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code")
        qr_code_base64 = payment.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code_base64")
        transaction_id = payment.get("id") or payment.get("payment_id")

        if not qr_code or not qr_code_base64:
            return {
                "payment_id": str(transaction_id or "mp-preference"),
                "qr_code_base64": "",
                "qr_code": "",
                "transaction_amount": total,
                "status": "pending",
            }

        return {
            "payment_id": str(transaction_id or "mp-preference"),
            "qr_code_base64": qr_code_base64,
            "qr_code": qr_code,
            "transaction_amount": total,
            "status": "pending",
        }
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro no pagamento: {str(exc)}") from exc


@app.post("/orders", response_model=schemas.OrderOut, status_code=status.HTTP_201_CREATED, tags=["orders"])
def create_order(
    order_in: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Cria um pedido para um usuário autenticado, com uma lista de itens (produto + quantidade).
    Valida existência do usuário, existência/estoque dos produtos e calcula o total.
    """
    if order_in.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você só pode criar pedidos para seu próprio usuário")

    user = db.query(models.User).filter(models.User.id == order_in.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    if not order_in.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O pedido precisa ter ao menos um item")

    order = models.Order(user_id=user.id, status=models.OrderStatus.pending, total=0.0)
    db.add(order)
    db.flush()

    total = 0.0
    for item in order_in.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto {item.product_id} não encontrado",
            )
        if item.quantity <= 0:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantidade deve ser maior que zero")
        if product.stock < item.quantity:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estoque insuficiente para o produto '{product.name}'",
            )

        product.stock -= item.quantity
        order_item = models.OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price,
        )
        db.add(order_item)
        total += product.price * item.quantity

    order.total = total
    db.commit()
    db.refresh(order)
    return order