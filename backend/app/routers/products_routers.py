# product_router.py

from fastapi import APIRouter, HTTPException

from backend.app.schemas.product_schemas import ProductCreate, ProductUpdate
from backend.app.services.product_service import (
    product_create,
    product_delete,
    product_get,
    product_get_all,
    product_update,
)
from uuid import UUID
from backend.app.core.api_response import ApiResponse

router = APIRouter(prefix="/products", tags=["products"])

# 1. create
@router.post("/product/create")
def create(product: ProductCreate) -> ApiResponse:
    created_product = product_create(product)
    if created_product is None:
        raise HTTPException(
            status_code=500,
            detail="상품 등록에 실패했습니다.",
        )
    response = ApiResponse(
        success = True,
        message="상품이 등록되었습니다.",
        data = created_product
    )
    return response

# 2. 한개 조회
@router.get("/product/get/{product_id}")
def get(product_id: UUID) -> ApiResponse:

    product = product_get(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"상품 ID {product_id}를 찾을 수 없습니다."
        )
    response = ApiResponse(
        success = True,
        message="상품 조회에 성공했습니다.",
        data = product
    )
    return response

# 3. 전체 조회
@router.get("/product/getall")
def get_all() -> ApiResponse:
    products = product_get_all()
    response = ApiResponse(
        success = True,
        message="상품 목록 조회에 성공했습니다.",
        data = products
    )
    return response

# 4. 한개 삭제
@router.delete("/product/delete/{product_id}")
def delete(product_id: UUID) -> ApiResponse:
    product = product_delete(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"상품 ID {product_id}를 찾을 수 없습니다."
        )
    response = ApiResponse(
        success = True,
        message="상품이 삭제되었습니다.",
        data = product
    )
    return response

# 5. 수정
@router.put("/product/{product_id}")
def update(product_id: UUID, product: ProductUpdate) -> ApiResponse:
    updated_product = product_update(product_id, product)
    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail=f"상품 ID {product_id}를 찾을 수 없습니다."
        )
    response = ApiResponse(
        success = True,
        message="상품이 수정되었습니다.",
        data = updated_product
    )
    return response
