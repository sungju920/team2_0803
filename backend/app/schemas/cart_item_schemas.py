"""Cart item request and response schemas."""
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class CartItemsPublic(BaseModel):
    # DB에서 조회한 상품을 API 응답으로 보낼 때 사용하는 형식입니다. 
    id : UUID = Field(default_factory=uuid4)
    product_id : int
    product_name :str
    quantity :  int = Field(ge=1, examples=[1])
    created_at : datetime
    updated_at : datetime

class CartItemsCreate(BaseModel):
    # 장바구니 생성 요청에서 반드시 받아야 하는 값입니다. 
    id : UUID = Field(default_factory=uuid4)
    product_id : int
    product_name :str
    quantity :  int = Field(ge=1, examples=[1])
    created_at : datetime

class CartItemsUpdate(BaseModel):
    # 장바구니 수정 요청에서 받을 값입니다. 
    id : UUID = Field(default_factory=uuid4)
    product_id : int
    product_name :str
    quantity :  int = Field(ge=1, examples=[1])
    updated_at : datetime