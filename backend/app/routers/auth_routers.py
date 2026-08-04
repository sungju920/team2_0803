""" Login Logout routers."""

from fastapi import APIRouter

from app.schemas.auth_schemas import (
    LoginRequest,
    LoginResponse,
    LogoutResponse,
)
from app.services.auth_service import (
    sign_in_process,
    sign_out_process,
)


router = APIRouter(
    prefix="/auth",
    tags=["로그인/로그아웃"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="로그인",
)
def sign_in(auth: LoginRequest) -> LoginResponse:
    """아이디와 비밀번호를 확인하고 로그인합니다."""

    return sign_in_process(auth)


@router.post(
    "/logout",
    response_model=LogoutResponse,
    summary="로그아웃",
)
def sign_out() -> LogoutResponse:
    """로그아웃 성공 메시지를 반환합니다."""

    return sign_out_process()