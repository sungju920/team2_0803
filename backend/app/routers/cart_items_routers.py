from fastapi import APIRouter, HTTPException

from backend.app.core.api_response import ApiResponse
from backend.app.schemas.cart_item_schemas import CartItemsCreate, CartItemsUpdate,CartItemsPublic
from backend.app.services.cart_item_service import cart_add_process, cart_select_process, cart_select_all_process

# router = APIRouter(prefix="/cart-items", tags=["cart_items"])
router = APIRouter(tags=["cart_items"])

@router.post("/cart-items")
def add_to_cart(item: CartItemsCreate) -> ApiResponse:
    """상품 장바구니 담기"""
    cart = cart_add_process(item)

    if cart is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    return ApiResponse(success=True, message="장바구니에 상품을 추가했습니다.", data=cart)

@router.get("/cart-items/{cart_item_id}")
def select_to_cart(cart_item_id : str) -> ApiResponse:
    """장바구니 단건 조회"""
    cart = cart_select_process(cart_item_id)

    if cart is None:
        raise HTTPException(status_code=404, detail="해당 장바구니를 찾을 수 없습니다.")

    return ApiResponse(success=True, message="해당 장바구니 상품을 조회했습니다.", data=cart)

@router.get("/cart-items")
def select_to_cart() -> ApiResponse:
    """장바구니 전체 조회"""
    cart = cart_select_all_process()

    if cart is None:
        raise HTTPException(status_code=404, detail="해당 장바구니를 찾을 수 없습니다.")

    return ApiResponse(success=True, message="해당 장바구니 상품을 조회했습니다.", data=cart)
