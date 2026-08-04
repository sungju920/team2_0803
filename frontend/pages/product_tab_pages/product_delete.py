import streamlit as st
from clients.product_client import product_delete
from core.api_client import BackendAPIError

@st.dialog("상품 삭제")
def show_del(p:dict) -> None:
    st.info("삭제")
    st.write(f"{p['product_name']} 상품을 삭제하시겠습니까")
    try:
        if st.button("삭제 확인", type="primary"):
            with st.spinner("상품을 삭제하고 있습니다."):
                result = product_delete(p["id"])

            if result:
                st.success("상품이 삭제되었습니다.")
                st.rerun()

    except BackendAPIError as error:
        st.error(str(error))
        