"""Product business logic and data access."""

# product_service.py
from uuid import UUID

from backend.app.schemas.product_schemas import ProductCreate, ProductPublic, ProductUpdate
from backend.app.core.supabase_client import get_supabase

# 1. 입력
def product_create(product: ProductCreate) -> ProductPublic | None:
    supabase = get_supabase()

    result = (
        supabase.table("products")
         .insert(
            {
                "product_name": product.product_name,
                "price": product.price,
            }
        )
        .execute()
    )
    if not result.data:
        return None
    return ProductPublic.model_validate(result.data[0])

# 2. 전체조회
def product_get_all() -> list[ProductPublic]:
    supabase = get_supabase()
    result = (
        supabase.table("products")
        .select("*")
        .execute()
    )
    return [ProductPublic.model_validate(item) for item in result.data]

# 3. 한개조회
def product_get(product_id: UUID) -> ProductPublic | None:
    supabase = get_supabase()

    result = (
        supabase.table("products")
        .select("*")
        .eq("id", str(product_id))
        .execute()
    )
    if not result.data:
        return None
    return ProductPublic.model_validate(result.data[0])


# 4. 삭제
def product_delete(product_id: UUID) -> ProductPublic | None:
    supabase = get_supabase()
    result = (
        supabase.table("products")
        .delete()
        .eq("id", str(product_id))
        .execute()
    )
    if not result.data:
        return None
    return ProductPublic.model_validate(result.data[0])


# 5. 수정
def product_update(
    product_id: UUID,
    product: ProductUpdate,
) -> ProductPublic | None:
    supabase = get_supabase()

    result = (
        supabase.table("products")
        .update(
                {
                    "product_name": product.product_name,
                    "price": product.price,
                }
            )
            .eq("id", str(product_id))
            .execute()
    )
    if not result.data:
        return None
    return ProductPublic.model_validate(result.data[0])
