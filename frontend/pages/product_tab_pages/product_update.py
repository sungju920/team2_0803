import streamlit as st

from clients.product_client import product_update
from core.api_client import BackendAPIError


@st.dialog("상품 수정")
def show_up(product: dict) -> None:
    st.info(f"{product['id']} 상품을 수정합니다.")

    try:
        with st.form(f"update_form_{product['id']}"):
            product_name = st.text_input(
                "상품명",
                value=product["product_name"],
                max_chars=50,
            )
            product_price = st.number_input(
                "가격",
                min_value=0,
                value=int(product["price"]),
                step=100,
            )
            submitted = st.form_submit_button("수정")

        if submitted:
            product_name = product_name.strip()

            if not product_name:
                st.warning("상품명을 입력하세요.")
                return

            payload = {
                "product_name": product_name,
                "price": int(product_price),
            }

            with st.spinner("상품을 수정하고 있습니다."):
                result = product_update(product["id"], payload)

            if result:
                st.success("상품이 수정되었습니다.")
                st.rerun()

    except BackendAPIError as error:
        st.error(str(error))