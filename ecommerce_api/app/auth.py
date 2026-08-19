import os
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ecommerce-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str | int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(subject), "exp": expire, "type": "access"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido") from exc


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> models.User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de autenticação ausente")

    payload = decode_access_token(credentials.credentials)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    return user


async def auth_middleware(request: Request, call_next):
    if not (
        request.url.path == "/orders"
        or request.url.path.startswith("/orders/")
        or request.url.path.startswith("/checkout")
    ):
        return await call_next(request)

    auth_header = request.headers.get("authorization")
    if not auth_header:
        return Response(
            content='{"detail":"Token de autenticação ausente"}',
            status_code=status.HTTP_401_UNAUTHORIZED,
            media_type="application/json",
        )

    try:
        scheme, token = auth_header.split(" ", 1)
    except ValueError:
        return Response(
            content='{"detail":"Formato do cabeçalho Authorization inválido"}',
            status_code=status.HTTP_401_UNAUTHORIZED,
            media_type="application/json",
        )

    if scheme.lower() != "bearer":
        return Response(
            content='{"detail":"Cabeçalho Authorization deve usar Bearer"}',
            status_code=status.HTTP_401_UNAUTHORIZED,
            media_type="application/json",
        )

    try:
        payload = decode_access_token(token)
    except HTTPException as exc:
        return Response(
            content=f'{{"detail":"{exc.detail}"}}',
            status_code=exc.status_code,
            media_type="application/json",
        )

    request.state.user_id = int(payload["sub"])
    return await call_next(request)
