
"""Login Logout service."""

from fastapi import HTTPException

from backend.app.core.password import verify_password
from backend.app.schemas.auth_schemas import (
    LoginRequest,
    LoginResponse,
    LogoutResponse,
)
from backend.app.services.customer_service import get_customer_by_id


def sign_in_process(auth: LoginRequest) -> LoginResponse:
    """회원 로그인을 처리합니다."""

    db_customer = get_customer_by_id(auth.id)

    if db_customer is None:
        raise HTTPException(
            status_code=401,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
        )

    if not verify_password(
        password=auth.pwd,
        saved_password=db_customer["pwd"],
    ):
        raise HTTPException(
            status_code=401,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
        )

    return LoginResponse(
        id=db_customer["id"],
        name=db_customer["name"],
        message="로그인되었습니다.",
    )


def sign_out_process() -> LogoutResponse:
    """회원 로그아웃 결과를 반환합니다."""

    return LogoutResponse(
        message="로그아웃되었습니다.",
    )
