from core.api_client import request

def cart_items_select(cart_item_id : str):
    """사용자의 장바구니만 가져오기"""
    return request("GET", f"/cart-items/{cart_item_id}")