import streamlit as st
from clients.product_client import product_insert
from core.api_client import BackendAPIError

def product_create() -> None:
    """상품명과 가격을 입력받아 상품을 등록합니다."""

    st.subheader("상품 등록")
    st.caption("상품을 등록합니다. 상품명과 가격을 입력하세요.")
    try:
        with st.form("product_form", clear_on_submit=True):
            product_name = st.text_input("상품명", placeholder="품명 입력", max_chars=50)
            product_price = st.number_input("가격", min_value=0, step=100)

            submitted = st.form_submit_button("등록")

        if submitted:
            product_name = product_name.strip()
            if not product_name:
                st.warning("상품명을 입력하세요")
                return
            
            payload = {"product_name": product_name, "price": int(product_price)}
            with st.spinner("상품을 등록하고 있습니다."):
                result = product_insert(payload)

            if result:
                st.success("상품이 등록되었습니다.")
                st.write(f"ID: {result['id']}")
                st.write(f"상품명: {result['product_name']}")
                st.write(f"가격: {result['price']:,}원")

    except BackendAPIError as error:
        st.error(str(error))
       
      