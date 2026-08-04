import streamlit as st


st.set_page_config(
    page_title="Team 02 shopping mall",
    page_icon="🛒",
    layout="wide",
)

st.markdown(
    """
    <style>
        .block-container { padding-top: 3.75rem; }
        .shopping-mall-banner {
            padding: 0.65rem 1rem;
            margin: 0 0 1rem 0;
            border-radius: 10px;
            color: white;
            background: #5FACD3;
            box-shadow: 0 4px 12px rgba(95, 172, 211, 0.22);
        }
        .shopping-mall-banner h1 {
            margin: 0;
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .shopping-mall-icon {
            width: 1.35rem;
            height: 1.35rem;
            flex-shrink: 0;
        }
        .shopping-mall-banner p {
            margin: 0.15rem 0 0 0;
            font-size: 0.8rem;
            opacity: 0.9;
        }
    </style>
    <div class="shopping-mall-banner">
        <h1>
            <svg class="shopping-mall-icon" viewBox="0 0 24 24" fill="none"
                 xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path d="M3 3H5L7.4 14.2C7.5 14.7 7.8 15.1 8.2 15.4C8.6 15.7 9.1 15.8 9.6 15.8H18.5C19 15.8 19.5 15.6 19.9 15.3C20.3 15 20.6 14.5 20.7 14L22 7H6"
                      stroke="white" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round"/>
                <circle cx="10" cy="20" r="1.4" fill="white"/>
                <circle cx="19" cy="20" r="1.4" fill="white"/>
            </svg>
            TEAM 02 SHOPPING MALL
        </h1>
        <p>고객과 상품을 한곳에서 관리하는 쇼핑몰 서비스</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("Team 02")
    current_user = st.session_state.get("current_user")
    if st.session_state.get("logged_in") and current_user:
        st.success(f"{current_user.get('name', '')}님 로그인 중")
    else:
        st.caption("로그인이 필요합니다.")

pages = [
    st.Page("pages/login.py", title="로그인 / 로그아웃", icon="🔐"),
    st.Page("pages/customers.py", title="회원 조회", icon="👤"),
    st.Page("pages/products.py", title="상품 관리", icon="📦"),
    st.Page("pages/notices.py", title="공지사항", icon="🏫"),
]

pages.append(
    st.Page("pages/cart_items.py", title="장바구니", icon="🛒")
)

page = st.navigation(pages)
page.run()
