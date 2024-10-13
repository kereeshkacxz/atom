import uuid
from datetime import timedelta, date
from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import DefaultSettings, getSettings
from app.db.connection import getSession
from app.models import (
    AuthSchema,
    RegistrationAdmin,
    RegistrationForm,
    RegistrationSuccess,
    Token,
    UserSchema,
    UserTable,
)
from app.utils.auth import authenticateUser, createAccessToken, getCurrentUser, isUserSuperAdmin, registerUser


apiRouter = APIRouter(prefix="/user", tags=["User"])


@apiRouter.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Username already exists",
        },
    },
)
async def registration(
    registration_form: Annotated[RegistrationForm, Body()],
    session: AsyncSession = Depends(getSession),
) -> RegistrationSuccess:
    is_success = await registerUser(session, registration_form)
    if is_success:
        return {"message": "Registered!"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email already exists",
    )


@apiRouter.post(
    "/register/admin",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(isUserSuperAdmin)],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Username already exists",
        },
    },
)
async def registration_admin(
    registration_form: Annotated[RegistrationAdmin, Body()],
    session: AsyncSession = Depends(getSession),
) -> RegistrationSuccess:
    registration_form.type = "admin"
    is_success = await registerUser(session, registration_form)
    if is_success:
        return {"message": "Registered!"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email already exists",
    )


@apiRouter.post(
    "/token",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect username or password",
        },
    },
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(getSession)],
    settings: Annotated[DefaultSettings, Depends(getSettings)],
) -> Token:
    user = await authenticateUser(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = createAccessToken(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@apiRouter.post(
    "/auth",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect username or password",
        },
    },
)
async def auth_for_access_token(
    form_data: AuthSchema,
    session: Annotated[AsyncSession, Depends(getSession)],
    settings: Annotated[DefaultSettings, Depends(getSettings)],
) -> Token:
    user = await authenticateUser(session, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = createAccessToken(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@apiRouter.get(
    "/me",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect username or password",
        },
    },
    summary="Get active user information",
)
async def read_users_me(
    current_user: Annotated[UserTable, Depends(getCurrentUser)],
) -> UserSchema:
    return current_user


@apiRouter.put(
    "/me_update",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
    },
    summary="Update user information",
)
async def update_user(
    current_user: Annotated[UserTable, Depends(getCurrentUser)],
    username: str | None = None,
    old_password: str | None = None,
    password: str | None = None,
    api_key: str | None = None,
    session: AsyncSession = Depends(getSession),
) -> UserSchema:

    if old_password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide old password",
        )

    if username is not None:
        current_user.username = username

    if api_key is not None:
        current_user.api_key = api_key

    if old_password is not None and password is not None:
        if not await authenticateUser(session, current_user.email, old_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect old password",
            )
        current_user.password = getSettings().PWD_CONTEXT.hash(password)

    session.add(current_user)
    await session.commit()

    return current_user