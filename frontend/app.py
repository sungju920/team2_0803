import streamlit as st

from pages.product_tab_pages.product_create import product_create
from pages.product_tab_pages.product_select import product_select
from pages.product_tab_pages.product_select_all import (
    product_select_all_page as product_select_all,
)

st.set_page_config(
    page_title="Team 01 CRUD",
    page_icon="🗂️",
    layout="wide",
)

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("상품 관리")

create_tab, select_tab, select_all_tab = st.tabs(
    ["상품 등록", "상품 조회", "상품 목록"]
)

with create_tab:
    product_create()

with select_tab:
    product_select()

with select_all_tab:
    product_select_all()