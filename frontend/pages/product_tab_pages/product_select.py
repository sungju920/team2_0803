import streamlit as st

from clients.product_client import product_select as fetch_product
from core.api_client import BackendAPIError


def product_select() -> None:
    st.subheader("상품 조회")
    st.caption("상품 ID를 입력하면 해당 상품의 정보를 조회합니다.")

    with st.form("product_select_form"):
        product_id = st.text_input(
            "상품 ID",
            placeholder="10000000-0000-4000-8000-000000000011",
        )
        submitted = st.form_submit_button("조회")

    if not submitted:
        return

    product_id = product_id.strip()

    if not product_id:
        st.warning("상품 ID를 입력하세요.")
        return

    try:
        with st.spinner("상품 정보를 조회하고 있습니다."):
            product = fetch_product(product_id)

        if not product:
            st.info("상품을 찾을 수 없습니다.")
            return

        st.success("상품을 조회했습니다.")

        with st.container(border=True):
            st.write(f"**상품 ID:** {product['id']}")
            st.write(f"**상품명:** {product['product_name']}")
            st.write(f"**가격:** {product['price']:,}원")
            st.write(f"**등록일:** {product['created_at']}")
            st.write(f"**수정일:** {product['updated_at']}")

    except BackendAPIError as error:
        st.error(str(error))