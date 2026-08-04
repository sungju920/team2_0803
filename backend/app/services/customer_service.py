"""고객 관리 서비스"""

from datetime import datetime, timezone

from fastapi import HTTPException

from app.core.password import hash_password
from app.core.supabase_client import get_supabase_client
from app.schemas.customer_schemas import (
    CustomerCreate,
    CustomerDeleteResponse,
    CustomerResponse,
    CustomerUpdate,
)


def get_customer_by_id(customer_id: str) -> dict | None:
    """아이디로 고객 한 명을 조회합니다."""

    response = (
        get_supabase_client()
        .table("customers")
        .select("id, pwd, name, created_at, updated_at")
        .eq("id", customer_id)
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None


def create_customer(customer: CustomerCreate) -> CustomerResponse:
    """비밀번호를 해시하여 고객을 등록합니다."""

    if get_customer_by_id(customer.id) is not None:
        raise HTTPException(status_code=409, detail="이미 사용 중인 아이디입니다.")

    response = (
        get_supabase_client()
        .table("customers")
        .insert(
            {
                "id": customer.id,
                "pwd": hash_password(customer.pwd),
                "name": customer.name,
            }
        )
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=500, detail="고객 등록에 실패했습니다.")

    return CustomerResponse.model_validate(response.data[0])


def get_customers() -> list[CustomerResponse]:
    """고객 목록을 최신 등록 순으로 조회합니다."""

    response = (
        get_supabase_client()
        .table("customers")
        .select("id, name, created_at, updated_at")
        .order("created_at", desc=True)
        .execute()
    )

    return [CustomerResponse.model_validate(row) for row in response.data]


def get_customer(customer_id: str) -> CustomerResponse:
    """고객 ID로 상세 정보를 조회합니다."""

    response = (
        get_supabase_client()
        .table("customers")
        .select("id, name, created_at, updated_at")
        .eq("id", customer_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="고객을 찾을 수 없습니다.")

    return CustomerResponse.model_validate(response.data[0])


def update_customer(
    customer_id: str,
    customer: CustomerUpdate,
) -> CustomerResponse:
    """고객 이름 또는 비밀번호를 수정합니다."""

    update_data: dict[str, str] = {}
    if customer.name is not None:
        update_data["name"] = customer.name
    if customer.pwd is not None:
        update_data["pwd"] = hash_password(customer.pwd)

    if not update_data:
        raise HTTPException(status_code=400, detail="수정할 값이 없습니다.")

    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    response = (
        get_supabase_client()
        .table("customers")
        .update(update_data)
        .eq("id", customer_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="고객을 찾을 수 없습니다.")

    return CustomerResponse.model_validate(response.data[0])


def delete_customer(customer_id: str) -> CustomerDeleteResponse:
    """고객을 삭제합니다."""

    response = (
        get_supabase_client()
        .table("customers")
        .delete()
        .eq("id", customer_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="고객을 찾을 수 없습니다.")

    return CustomerDeleteResponse(message="고객이 삭제되었습니다.")
