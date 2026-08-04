"""고객 관리 요청 및 응답 라우터."""

from fastapi import APIRouter

from backend.app.schemas.customer_schemas import (
    CustomerCreate,
    CustomerDeleteResponse,
    CustomerResponse,
    CustomerUpdate,
)
from backend.app.services.customer_service import (
    create_customer,
    delete_customer,
    get_customer,
    get_customers,
    update_customer,
)

router = APIRouter(prefix="/customers", tags=["고객 관리"])


@router.post("", response_model=CustomerResponse, status_code=201, summary="고객 등록")
def register_customer(customer: CustomerCreate) -> CustomerResponse:
    return create_customer(customer)


@router.get("", response_model=list[CustomerResponse], summary="고객 목록 조회")
def read_customers() -> list[CustomerResponse]:
    return get_customers()


@router.get("/{customer_id}", response_model=CustomerResponse, summary="고객 상세조회")
def read_customer(customer_id: str) -> CustomerResponse:
    return get_customer(customer_id)


@router.put("/{customer_id}", response_model=CustomerResponse, summary="고객 수정")
def change_customer(
    customer_id: str,
    customer: CustomerUpdate,
) -> CustomerResponse:
    return update_customer(customer_id, customer)


@router.delete(
    "/{customer_id}",
    response_model=CustomerDeleteResponse,
    summary="회원 삭제",
)
def remove_customer(customer_id: str) -> CustomerDeleteResponse:
    return delete_customer(customer_id)
