"""공지사항 등록, 조회, 수정, 삭제 화면입니다."""

import streamlit as st

from core.api_client import BackendAPIError, request


def _request(method: str, path: str, json: dict | None = None):
    """공통 API 클라이언트가 반환한 오류 응답을 화면용 예외로 바꿉니다."""

    result = request(method, path, json=json)
    if isinstance(result, dict) and "detail" in result:
        detail = result["detail"]
        if isinstance(detail, list):
            detail = "입력값을 확인해 주세요."
        raise BackendAPIError(str(detail))
    return result


def _is_modified(notice: dict) -> bool:
    """등록 시각과 수정 시각이 다르면 수정된 공지로 표시합니다."""

    return str(notice.get("created_at")) != str(notice.get("updated_at"))


def _show_feedback() -> None:
    """화면 새로고침 뒤에도 한 번만 성공 메시지를 보여 줍니다."""

    message = st.session_state.pop("notice_feedback", None)
    if message:
        st.success(message)


st.title("공지사항 관리")
_show_feedback()

st.subheader("공지 등록")
with st.form("notice_create_form", clear_on_submit=True):
    create_title = st.text_input("제목", max_chars=200)
    create_content = st.text_area("본문", height=160)
    create_submitted = st.form_submit_button("등록")

if create_submitted:
    if not create_title.strip() or not create_content.strip():
        st.error("제목과 본문을 모두 입력해 주세요.")
    else:
        try:
            _request(
                "POST",
                "/notices",
                {"title": create_title, "content": create_content},
            )
        except BackendAPIError as error:
            st.error(str(error))
        else:
            st.session_state["notice_feedback"] = "등록 되었습니다"
            st.rerun()

st.divider()
st.subheader("공지 목록")

try:
    notices = _request("GET", "/notices")
except BackendAPIError as error:
    st.error(str(error))
    notices = []

if not notices:
    st.info("등록된 공지사항이 없습니다.")
else:
    for notice in notices:
        left, right = st.columns([5, 1])
        left.write(notice["title"])
        if right.button("상세보기", key=f"notice_detail_{notice['id']}"):
            st.session_state["selected_notice_id"] = notice["id"]
            st.rerun()

selected_notice_id = st.session_state.get("selected_notice_id")
if selected_notice_id is not None:
    st.divider()
    st.subheader("공지 상세")
    try:
        selected_notice = _request("GET", f"/notices/{selected_notice_id}")
    except BackendAPIError as error:
        st.error(str(error))
        st.session_state.pop("selected_notice_id", None)
    else:
        modified_label = " (수정됨)" if _is_modified(selected_notice) else ""
        st.markdown(f"### {selected_notice['title']}{modified_label}")
        st.write(selected_notice["content"])

        with st.expander("공지 수정"):
            with st.form(f"notice_update_form_{selected_notice_id}"):
                update_title = st.text_input(
                    "수정할 제목",
                    value=selected_notice["title"],
                    max_chars=200,
                    key=f"notice_update_title_{selected_notice_id}",
                )
                update_content = st.text_area(
                    "수정할 본문",
                    value=selected_notice["content"],
                    height=160,
                    key=f"notice_update_content_{selected_notice_id}",
                )
                update_submitted = st.form_submit_button("수정")

            if update_submitted:
                if not update_title.strip() or not update_content.strip():
                    st.error("제목과 본문을 모두 입력해 주세요.")
                else:
                    try:
                        _request(
                            "PUT",
                            f"/notices/{selected_notice_id}",
                            {"title": update_title, "content": update_content},
                        )
                    except BackendAPIError as error:
                        st.error(str(error))
                    else:
                        st.session_state["notice_feedback"] = "수정 되었습니다"
                        st.rerun()

        if st.button("삭제", key=f"notice_delete_{selected_notice_id}", type="secondary"):
            try:
                _request("DELETE", f"/notices/{selected_notice_id}")
            except BackendAPIError as error:
                st.error(str(error))
            else:
                st.session_state.pop("selected_notice_id", None)
                st.session_state["notice_feedback"] = "삭제 되었습니다"
                st.rerun()
