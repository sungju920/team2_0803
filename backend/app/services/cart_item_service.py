"""Cart item business logic and data access."""
from datetime import datetime
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from fastapi import HTTPException
# from app.core.supabase_client import get_supabase
from app.core.supabase_client import get_supabase
from app.schemas.cart_item_schemas import CartItemsCreate, CartItemsPublic, CartItemsUpdate

def cart_add_process(item : CartItemsCreate):
    supabase = get_supabase()

    #product 정보를 가져오기위한..
    product = (
        supabase.table("products")
        .select("id, product_name, price")
        .eq("id", item.product_id)
        .execute()
        .data
    )

    if product is None:
        raise HTTPException(status_code=404, detail="해당 상품을 찾을수가 없습니다.")

    existing = (
        supabase.table("cart_items")
        .select("*")
        .eq("id", item.id)
        .eq("product_id", item.product_id)
        .execute()
        .data
    )

    # 이미 같은 상품이 있다면 수량 누적 및 업데이트 날짜에 기록
    if existing:
        cart = existing[0]
        return (
            supabase.table("cart_items")
            .update({
                "quantity": cart["quantity"] + item.quantity,
                "updated_at": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
            })
            .eq("id", cart["id"])
            .eq("product_id", cart["product_id"])
            .execute()
            .data[0]
        )

    result = (
        supabase.table("cart_items")
        .insert(
            {
                "id": str(uuid4()),
                "product_id": product[0]['id'],
                "product_name": product[0]['product_name'],
                "quantity": item.quantity,
                "created_at": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
            }
        )
        .execute()
    )
    return result.data[0]

def cart_select_process(cart_id : str):
    supabase = get_supabase()

    cart_response = (
        supabase.table("cart_items")
        .select("*")
        .eq("id", cart_id)
        .execute()
    )
    
    if cart_response.data is None:
        raise HTTPException(status_code=404, detail="해당 장바구니를 찾을수가 없습니다.")

    return cart_response.data

def cart_select_all_process():
    supabase = get_supabase()

    cart_response = (
        supabase.table("cart_items")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    
    if cart_response.data is None:
        raise HTTPException(status_code=404, detail="장바구니 조회가 되지 않습니다.")

    return cart_response.data

def cart_update_process(cart_id : str) :
    return
