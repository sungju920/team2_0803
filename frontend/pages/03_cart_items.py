"""장바구니 관련 화면"""
import streamlit as st
from clients.cart_items_client import cart_items_select
import pandas as pd

st.title("장바구니")

with st.container(border=True) : 
    st.subheader("장바구니 조회", divider="rainbow")
    with st.spinner("cart Selecting.....") :
        # response = cart_items_select(cart_id)
        response = cart_items_select("0ee8f346-204b-431e-97b0-957302399041")
        # response = httpx.get(f"{server_URL}/product/getall", timeout=5.0)
        if response is not None :
            st.write("data 잇음")
            st.write(response["data"][0]["id"])
            
            # result_data = response.json()
            # data = response["data"][0]
            # print(data)
            # df = pd.DataFrame(data)
            # select_event = st.dataframe(data, use_container_width=True, selection_mode="single-row", on_select="rerun")
            # if select_event.selection.rows :
            #     row_index = select_event.selection.rows[0]
            #     selected_row = df.iloc[row_index].to_dict()
            #     # st.write("선택된 상품:", selected_row)
            #     update_col, delete_col = st.columns(2)
            #     # with update_col :
            #     #     if st.button("update", use_container_width=True):
            #     #         update_product(selected_row)
            #     # with delete_col :
            #     #     if st.button("delete", use_container_width=True) :
            #     #         delete_product(selected_row)
            # # else :
            # #     if st.button("create", use_container_width=True) :
            # #         create_product()