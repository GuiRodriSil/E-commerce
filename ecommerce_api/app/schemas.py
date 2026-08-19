from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models import OrderStatus


# ---------- Auth ----------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None


class PaymentItem(BaseModel):
    id: int
    title: str
    quantity: int
    unit_price: float


class PaymentCreate(BaseModel):
    payer_email: str
    items: List[PaymentItem]
    payment_method: str = "pix"


class PaymentResponse(BaseModel):
    payment_id: str
    qr_code_base64: str
    qr_code: str
    transaction_amount: float
    status: str
    checkout_url: Optional[str] = None


# ---------- Support ----------
class SupportTicketCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


class SupportTicketResponse(BaseModel):
    message: str
    protocol: str
    created_at: datetime


# ---------- Category ----------
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryOut(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Product ----------
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    image_url: Optional[str] = None
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    created_at: datetime
    category: Optional[CategoryOut] = None


# ---------- User (referência simples usada em Order) ----------
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr


class UserMeOut(UserOut):
    orders: List["OrderOut"] = []


# ---------- Order ----------
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int
    quantity: int
    unit_price: float


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    status: OrderStatus
    total: float
    created_at: datetime
    items: List[OrderItemOut] = []