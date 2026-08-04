import streamlit as st

from core.api_client import BackendAPIError, request


st.title("로그인 / 로그아웃")
st.caption("회원 아이디와 비밀번호로 로그인 상태를 관리합니다.")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    with st.form("login_form"):
        login_id = st.text_input("아이디")
        login_pwd = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("로그인", use_container_width=True)

    if submitted:
        if not login_id.strip() or not login_pwd:
            st.warning("아이디와 비밀번호를 모두 입력해 주세요.")
        else:
            try:
                user = request("POST", "/auth/login", json={"id": login_id.strip(), "pwd": login_pwd})
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = user
                st.rerun()
            except BackendAPIError as error:
                st.error(str(error))
else:
    user = st.session_state.get("current_user", {})
    st.success(f"{user.get('name', '')}님이 로그인 중입니다.")
    id_col, name_col = st.columns(2)
    id_col.metric("아이디", user.get("id", "-"))
    name_col.metric("이름", user.get("name", "-"))

    if st.button("로그아웃", type="primary", use_container_width=True):
        try:
            request("POST", "/auth/logout")
            st.session_state.pop("current_user", None)
            st.session_state["logged_in"] = False
            st.rerun()
        except BackendAPIError as error:
            st.error(str(error))
