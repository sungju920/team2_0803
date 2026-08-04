# product_client.py
# product CRUD

from typing import Any
from core.api_client import request

def _get_data(payload: dict[str, Any]):
    return payload.get("data", None)

def product_insert(product: dict):
    return _get_data(request("POST", f"/products/product/create", json=product))

def product_select(product_id: str):
    return _get_data(request("GET", f"/products/product/get/{product_id}"))

def product_update(product_id: str, product: dict):
    return _get_data(request("PUT", f"/products/product/{product_id}", json=product))

def product_delete(product_id: str):
    return _get_data(request("DELETE", f"/products/product/delete/{product_id}"))

def product_select_all():
    return _get_data(request("GET", f"/products/product/getall"))