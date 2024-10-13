from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import DefaultSettings, getSettings
from app.db.connection import getSession
from app.models import RegistrationAdmin, RegistrationForm, TokenData, UserTable


def verifyPassword(plain_password: str, hashed_password: str) -> bool:
    return getSettings().PWD_CONTEXT.verify(plain_password, hashed_password)


async def getUser(session: AsyncSession, email: str) -> UserTable | None:
    query = select(UserTable).where(UserTable.email == email)
    return await session.scalar(query)


async def registerUser(session: AsyncSession, user_data: RegistrationForm | RegistrationAdmin) -> bool:
    user = UserTable(**user_data.model_dump(exclude_unset=True))
    session.add(user)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False
    return True


async def authenticateUser(session: AsyncSession, email: str, password: str):
    user = await getUser(session, email)
    if not user:
        return False
    print(user)
    if not verifyPassword(password, user.password):
        return False
    return user


def createAccessToken(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=7 * 24 * 60)
    settings = getSettings()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def getCurrentUser(
    token: Annotated[str, Depends(getSettings().OAUTH2_SCHEME)],
    session: Annotated[AsyncSession, Depends(getSession)],
    settings: Annotated[DefaultSettings, Depends(getSettings)],
) -> UserTable:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = await getUser(session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def isUserAdmin(
    token: Annotated[str, Depends(getSettings().OAUTH2_SCHEME)],
    session: Annotated[AsyncSession, Depends(getSession)],
    settings: Annotated[DefaultSettings, Depends(getSettings)],
) -> UserTable:
    user = await getCurrentUser(token, session, settings)
    if user.type not in ("admin", "superadmin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )
    return user


async def isUserSuperAdmin(
    token: Annotated[str, Depends(getSettings().OAUTH2_SCHEME)],
    session: Annotated[AsyncSession, Depends(getSession)],
    settings: Annotated[DefaultSettings, Depends(getSettings)],
) -> UserTable:
    user = await getCurrentUser(token, session, settings)
    if user.type != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )
    return user
