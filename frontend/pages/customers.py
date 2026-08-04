import streamlit as st

from core.api_client import BackendAPIError, request


st.title("회원조회 및 회원가입")
st.caption("회원 목록·상세조회·가입·수정·삭제를 관리합니다.")

list_tab, signup_tab, manage_tab = st.tabs(["조회", "가입", "수정·삭제"])

with list_tab:
    st.subheader("전체 회원")

    if "customers" not in st.session_state:
        try:
            customers = request("GET", "/customers")
            st.session_state["customers"] = customers
        except BackendAPIError as error:
            st.error(str(error))

    if st.button("회원 목록 새로고침", use_container_width=True):
        try:
            st.session_state["customers"] = request("GET", "/customers")
            st.rerun()
        except BackendAPIError as error:
            st.error(str(error))

    customers = st.session_state.get("customers", [])
    if customers:
        st.dataframe(
            customers,
            column_order=["id", "name", "created_at", "updated_at"],
            column_config={
                "id": "아이디",
                "name": "이름",
                "created_at": "가입일",
                "updated_at": "수정일",
            },
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("새로고침 버튼을 눌러 회원 목록을 조회하세요.")

    st.divider()
    st.subheader("회원 상세조회")
    detail_id = st.text_input("조회할 아이디", key="detail_customer_id")

    if st.button("상세조회", use_container_width=True):
        if not detail_id.strip():
            st.warning("조회할 아이디를 입력하세요.")
        else:
            try:
                customer = request("GET", f"/customers/{detail_id.strip()}")
                st.success("회원을 조회했습니다.")
                st.json(customer)
            except BackendAPIError as error:
                st.error(str(error))

with manage_tab:
    st.subheader("회원 정보 수정")

    with st.form("customer_update_form"):
        update_id = st.text_input("수정할 아이디")
        update_name = st.text_input("새 이름")
        update_pwd = st.text_input("새 비밀번호", type="password")
        update_submit = st.form_submit_button("회원 정보 수정", use_container_width=True)

    if update_submit:
        update_data = {}
        if update_name.strip():
            update_data["name"] = update_name.strip()
        if update_pwd:
            update_data["pwd"] = update_pwd

        if not update_id.strip():
            st.warning("수정할 아이디를 입력하세요.")
        elif not update_data:
            st.warning("새 이름 또는 새 비밀번호를 입력하세요.")
        else:
            try:
                customer = request(
                    "PUT",
                    f"/customers/{update_id.strip()}",
                    json=update_data,
                )
                st.success(f"{customer['id']} 회원 정보가 수정되었습니다.")
                st.session_state["customers"] = request("GET", "/customers")
            except BackendAPIError as error:
                st.error(str(error))

    st.divider()
    st.subheader("회원 삭제")
    delete_id = st.text_input("삭제할 아이디")
    delete_confirm = st.checkbox("삭제하면 복구할 수 없음을 확인했습니다.")

    if st.button("회원 삭제", type="primary", use_container_width=True):
        if not delete_id.strip():
            st.warning("삭제할 아이디를 입력하세요.")
        elif not delete_confirm:
            st.warning("삭제 확인 항목을 선택하세요.")
        else:
            try:
                result = request("DELETE", f"/customers/{delete_id.strip()}")
                st.success(result["message"])
                st.session_state["customers"] = request("GET", "/customers")
                current_user = st.session_state.get("current_user", {})
                if current_user.get("id") == delete_id.strip():
                    st.session_state.pop("current_user", None)
                    st.session_state["logged_in"] = False
            except BackendAPIError as error:
                st.error(str(error))

with signup_tab:
    st.subheader("신규 회원가입")

    with st.form("signup_form", clear_on_submit=True):
        signup_id = st.text_input("아이디")
        signup_pwd = st.text_input("비밀번호", type="password")
        signup_name = st.text_input("이름")
        signup_submit = st.form_submit_button("회원가입", use_container_width=True)

    if signup_submit:
        if not signup_id.strip() or not signup_pwd or not signup_name.strip():
            st.warning("아이디, 비밀번호, 이름을 모두 입력하세요.")
        else:
            try:
                customer = request(
                    "POST",
                    "/customers",
                    json={
                        "id": signup_id.strip(),
                        "pwd": signup_pwd,
                        "name": signup_name.strip(),
                    },
                )
                st.success(f"{customer['name']} 회원이 가입되었습니다.")
                st.session_state["customers"] = request("GET", "/customers")
            except BackendAPIError as error:
                st.error(str(error))
