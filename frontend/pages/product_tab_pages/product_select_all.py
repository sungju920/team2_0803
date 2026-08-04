import streamlit as st

from clients.product_client import product_select_all
from pages.product_tab_pages.product_delete import show_del
from pages.product_tab_pages.product_update import show_up
from core.api_client import BackendAPIError

def product_select_all_page() -> None:
    """데이터를 확인합니다."""

    st.subheader("상품 목록")

    try:
        with st.spinner("상품 목록을 불러오고 있습니다."):
            result = product_select_all()

        if not result:
            st.info("상품이 없습니다.")
            return
        for p in result:
            with st.container(border=True):
                product_col, button_col = st.columns([3,1])
                with product_col:
                    st.write(f"ID: {p['id']}")
                    st.write(f"상품명: {p['product_name']}")
                    st.write(f"가격: {p['price']:,}원")
                with button_col:
                    if st.button(
                        "수정",
                        key=f"update_{p['id']}",
                    ):
                        show_up(p)

                    if st.button(
                        "삭제",
                        key=f"delete_{p['id']}",
                    ):
                        show_del(p)
    except BackendAPIError as error:
        st.error(str(error))