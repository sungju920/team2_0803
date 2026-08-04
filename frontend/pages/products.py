import streamlit as st

from pages.product_tab_pages.product_create import product_create
from pages.product_tab_pages.product_select import product_select
from pages.product_tab_pages.product_select_all import product_select_all_page


st.title("상품 관리")

create_tab, list_tab, detail_tab = st.tabs(
    ["상품 등록", "상품 전체 조회", "상품 상세 조회"]
)

with create_tab:
    product_create()

with list_tab:
    product_select_all_page()

with detail_tab:
    product_select()
