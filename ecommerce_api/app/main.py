import os
import uuid
from typing import List

import mercadopago
from google import genai
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

CHAT_SYSTEM_PROMPT = """
Você é o atendente virtual da nossa loja de e-commerce.
Responda sempre em português do Brasil, de forma cordial, objetiva e útil.
Tire dúvidas apenas sobre produtos da loja, disponibilidade, preços, entregas,
pagamentos e políticas de troca/devolução. Não invente informações específicas
como estoque, prazo ou status de pedido; quando não tiver dados suficientes,
explique a limitação e oriente o cliente a consultar o Perfil ou falar com o
suporte humano em /support. Nunca solicite ou revele senhas, tokens ou dados
completos de cartão. Para assuntos fora do escopo, diga que pode ajudar apenas
com dúvidas relacionadas à loja.
""".strip()


def _is_gemini_unavailable(error: Exception) -> bool:
    error_text = str(error).upper()
    return "503" in error_text or "UNAVAILABLE" in error_text or "HIGH DEMAND" in error_text


def _generate_chat_response(client, message: str) -> str:
    models_to_try = [os.getenv("GEMINI_MODEL", "gemini-3.6-flash")]
    fallback_model = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.5-flash")
    if fallback_model and fallback_model not in models_to_try:
        models_to_try.append(fallback_model)

    last_error = None
    for model in models_to_try:
        for _ in range(2):
            try:
                result = client.models.generate_content(
                    model=model,
                    contents=message,
                    config={"system_instruction": CHAT_SYSTEM_PROMPT},
                )
                response_text = (result.text or "").strip()
                if response_text:
                    return response_text
                last_error = RuntimeError("O Gemini não retornou uma resposta")
            except Exception as exc:
                last_error = exc
                if not _is_gemini_unavailable(exc):
                    raise

    raise last_error or RuntimeError("O Gemini não retornou uma resposta")

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


@app.post("/api/chat", response_model=schemas.ChatResponse, tags=["chat"])
def chat(chat_in: schemas.ChatRequest):
    """Envia uma dúvida ao atendente virtual baseado em Gemini."""
    message = chat_in.message.strip()
    if not message:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A mensagem não pode ficar vazia")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="GEMINI_API_KEY não configurada")

    try:
        client = genai.Client(api_key=api_key)
        return {"response": _generate_chat_response(client, message)}
    except HTTPException:
        raise
    except Exception as exc:
        if _is_gemini_unavailable(exc):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="O atendente está temporariamente sobrecarregado. Tente novamente em alguns instantes ou use a página /support.",
            ) from exc
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Erro ao consultar o Gemini: {str(exc)}") from exc


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


@app.post("/support/tickets", response_model=schemas.SupportTicketResponse, status_code=status.HTTP_201_CREATED, tags=["support"])
def create_support_ticket(ticket_in: schemas.SupportTicketCreate, db: Session = Depends(get_db)):
    """Salva uma solicitação de suporte e retorna seu número de protocolo."""
    values = {
        "name": ticket_in.name.strip(),
        "email": str(ticket_in.email),
        "subject": ticket_in.subject.strip(),
        "message": ticket_in.message.strip(),
    }
    if not values["name"] or not values["subject"] or not values["message"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome, assunto e mensagem são obrigatórios")

    ticket = models.SupportTicket(
        protocol=f"SUP-{uuid.uuid4().hex[:10].upper()}",
        **values,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return {
        "message": "Solicitação recebida com sucesso",
        "protocol": ticket.protocol,
        "created_at": ticket.created_at,
    }


@app.get("/users/me", response_model=schemas.UserMeOut, tags=["users"])
def get_my_profile(current_user: models.User = Depends(get_current_user)):
    """Retorna os dados e o histórico de pedidos do usuário autenticado."""
    return current_user


@app.put("/users/me", response_model=schemas.UserMeOut, tags=["users"])
def update_my_profile(
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Atualiza nome e/ou senha do usuário autenticado."""
    if user_in.name is not None:
        name = user_in.name.strip()
        if not name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O nome não pode ficar vazio")
        current_user.name = name

    if user_in.password is not None:
        if len(user_in.password) < 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A senha deve ter pelo menos 6 caracteres")
        current_user.hashed_password = hash_password(user_in.password)

    db.commit()
    db.refresh(current_user)
    return current_user


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


@app.post("/payments/mercadopago", response_model=schemas.PaymentResponse, tags=["payments"])
def create_payment(
    payment_in: schemas.PaymentCreate,
    current_user: models.User = Depends(get_current_user),
):
    if payment_in.payment_method not in {"pix", "card", "boleto"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Forma de pagamento inválida")
    if not payment_in.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O carrinho precisa ter pelo menos um item")

    total = sum(item.quantity * item.unit_price for item in payment_in.items)
    if total <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O valor total deve ser maior que zero")

    if any(item.quantity <= 0 or item.unit_price <= 0 for item in payment_in.items):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Itens do pagamento devem ter quantidade e preço positivos")

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
        "payer": {"email": current_user.email},
        "payment_methods": {"excluded_payment_types": [{"id": "ticket"}], "installments": 1},
        "back_urls": {"success": "http://localhost:5173", "failure": "http://localhost:5173", "pending": "http://localhost:5173"},
        "auto_return": "approved",
    }

    try:
        if payment_in.payment_method == "boleto":
            preference_data["payment_methods"] = {"excluded_payment_types": [{"id": "credit_card"}, {"id": "debit_card"}, {"id": "bank_transfer"}]}
        elif payment_in.payment_method == "card":
            preference_data["payment_methods"] = {"excluded_payment_types": [{"id": "ticket"}, {"id": "bank_transfer"}]}

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
                "checkout_url": payment.get("init_point"),
            }

        return {
            "payment_id": str(transaction_id or "mp-preference"),
            "qr_code_base64": qr_code_base64,
            "qr_code": qr_code,
            "transaction_amount": total,
            "status": "pending",
            "checkout_url": payment.get("init_point"),
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