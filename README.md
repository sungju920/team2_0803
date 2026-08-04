# Team 02 Shopping Mall CRUD

Streamlit, FastAPI, Supabase를 이용한 수업 복습용 쇼핑몰 CRUD 미니 프로젝트입니다.

고객 및 인증, 상품, 장바구니, 공지사항 기능을 FastAPI로 제공하고 Streamlit 화면에서 API를 호출합니다. 프론트엔드가 Supabase에 직접 접근하지 않고 백엔드를 통해서만 데이터를 처리하도록 구성했습니다.

## 기술 스택

- Frontend: Streamlit
- Backend: FastAPI, Uvicorn
- Database: Supabase(PostgreSQL)
- Validation: Pydantic
- HTTP Client: Requests
- Password: PBKDF2-SHA256
- Language: Python 3.12

## 주요 기능

| 구분 | 현재 구현 기능 |
| --- | --- |
| 고객 | 회원가입, 전체 조회, 상세 조회, 수정, 삭제 |
| 인증 | 로그인, 로그아웃, 비밀번호 해시 검증 |
| 상품 | 등록, 전체 조회, 상세 조회, 수정, 삭제 |
| 장바구니 | 등록, 전체 조회, 상세 조회 |
| 공지사항 | 등록, 전체 조회, 상세 조회, 수정, 삭제 |

> 장바구니 수정과 삭제는 계획서에는 포함되어 있지만 현재 라우터에는 아직 구현되지 않았습니다.

## 프로젝트 구조

```text
team2_0803/
├── backend/
│   ├── app/
│   │   ├── core/                 # Supabase, 비밀번호, 공통 응답
│   │   ├── routers/              # FastAPI 엔드포인트
│   │   ├── schemas/              # Pydantic 요청·응답 모델
│   │   ├── services/             # 비즈니스 로직 및 Supabase 연동
│   │   └── main.py               # FastAPI 애플리케이션
│   ├── SQL/
│   │   ├── customer.sql
│   │   └── products.sql
│   ├── .gitignore
│   └── requirements.txt          # 백엔드 패키지 목록
├── frontend/
│   ├── clients/                  # 상품·장바구니 API 호출
│   ├── core/
│   │   └── api_client.py         # 백엔드 공통 요청 함수
│   ├── pages/
│   │   ├── product_tab_pages/    # 상품 관리 내부 탭
│   │   ├── cart_items.py
│   │   ├── customers.py
│   │   ├── login.py
│   │   ├── notices.py
│   │   └── products.py
│   ├── app.py                    # Streamlit 진입점
│   ├── .gitignore
│   └── requirements.txt          # 프론트엔드 패키지 목록
├── TEAM02_0803_PLAN.md
└── README.md
```

## 최종 실행 기준

현재 저장소는 백엔드와 프론트엔드 환경을 분리해서 관리합니다.

- 백엔드 가상환경: `backend/.venv`
- 프론트엔드 가상환경: `frontend/.venv`
- 백엔드 패키지 목록: `backend/requirements.txt`
- 프론트엔드 패키지 목록: `frontend/requirements.txt`
- Git 제외 설정: `backend/.gitignore`, `frontend/.gitignore`
- Supabase 환경변수: `backend/.env`
- 서버 실행 위치: 프로젝트 루트 `C:\mini\team2_0803`

루트에는 현재 `.gitignore`가 없으므로 루트 `.venv`를 새로 만들거나 Git에 추가하지 않습니다. 가상환경은 반드시 백엔드와 프론트엔드 폴더 안에 생성합니다.

## 설치

프로젝트 최상위 폴더에서 진행합니다.

```powershell
cd C:\mini\team2_0803
```

```powershell
python -m venv backend\.venv
.\backend\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

설치가 끝나면 새 터미널을 열고 프론트엔드 환경을 설치합니다.

```powershell
cd C:\mini\team2_0803
python -m venv frontend\.venv
.\frontend\.venv\Scripts\Activate.ps1
pip install -r frontend\requirements.txt
```

이미 각 `.venv`가 만들어져 있다면 가상환경 생성 명령은 생략합니다.

## 환경변수 설정

백엔드는 실제 코드 기준으로 `backend/.env`를 읽습니다. 다음 파일을 생성합니다.

```text
backend/.env
```

내용:

```dotenv
SUPABASE_URL=https://프로젝트-ID.supabase.co
SUPABASE_SERVICE_ROLE_KEY=Supabase-service-role-key
```

- `SUPABASE_URL`: Supabase 프로젝트 URL
- `SUPABASE_SERVICE_ROLE_KEY`: 백엔드 전용 service role 키
- service role 키는 Streamlit 코드, GitHub, 화면 또는 로그에 노출하면 안 됩니다.
- `.env` 파일은 Git에 커밋하지 않습니다.

현재 백엔드 코드는 `SUPABASE_KEY`가 아니라 `SUPABASE_SERVICE_ROLE_KEY`를 사용합니다.

## 실행

### 1. 백엔드 실행

```powershell
cd C:\mini\team2_0803
.\backend\.venv\Scripts\Activate.ps1
python -m uvicorn backend.app.main:app --reload --port 8001
```

프로젝트 최상위 폴더에서 `backend.app.main:app`으로 실행해야 합니다. `backend` 폴더 안에서 `uvicorn app.main:app`으로 실행하면 현재 import 구조와 맞지 않습니다.

- Swagger: http://127.0.0.1:8001/docs
- OpenAPI JSON: http://127.0.0.1:8001/openapi.json
- 상태 확인: http://127.0.0.1:8001/health

### 2. 프론트엔드 실행

백엔드 터미널은 종료하지 않고 새 터미널을 엽니다.

```powershell
cd C:\mini\team2_0803
.\frontend\.venv\Scripts\Activate.ps1
$env:BACKEND_URL="http://127.0.0.1:8001"
streamlit run frontend/app.py --server.port 8502
```

- Streamlit: http://localhost:8502

`BACKEND_URL`을 설정하지 않으면 프론트엔드는 기본값인 `http://127.0.0.1:8000`으로 요청합니다. 8000번에서 다른 서버가 실행 중이라면 반드시 현재 백엔드 주소를 지정해야 합니다.

## API

### 고객 및 인증

| Method | Path | 설명 |
| --- | --- | --- |
| POST | `/customers` | 회원가입 |
| GET | `/customers` | 고객 전체 조회 |
| GET | `/customers/{customer_id}` | 고객 상세 조회 |
| PUT | `/customers/{customer_id}` | 고객 정보 수정 |
| DELETE | `/customers/{customer_id}` | 고객 삭제 |
| POST | `/auth/login` | 로그인 |
| POST | `/auth/logout` | 로그아웃 |

### 상품

| Method | Path | 설명 |
| --- | --- | --- |
| POST | `/products/product/create` | 상품 등록 |
| GET | `/products/product/getall` | 상품 전체 조회 |
| GET | `/products/product/get/{product_id}` | 상품 상세 조회 |
| PUT | `/products/product/{product_id}` | 상품 수정 |
| DELETE | `/products/product/delete/{product_id}` | 상품 삭제 |

### 장바구니

| Method | Path | 설명 |
| --- | --- | --- |
| POST | `/cart-items` | 장바구니 항목 등록 |
| GET | `/cart-items` | 장바구니 전체 조회 |
| GET | `/cart-items/{cart_item_id}` | 장바구니 상세 조회 |

### 공지사항

| Method | Path | 설명 |
| --- | --- | --- |
| POST | `/notices` | 공지사항 등록 |
| GET | `/notices` | 공지사항 전체 조회 |
| GET | `/notices/{notice_id}` | 공지사항 상세 조회 |
| PUT | `/notices/{notice_id}` | 공지사항 수정 |
| DELETE | `/notices/{notice_id}` | 공지사항 삭제 |

## 프론트엔드 메뉴

- 로그인 / 로그아웃
- 회원 조회 및 회원가입·수정·삭제
- 상품 관리
  - 상품 등록
  - 상품 전체 조회
  - 상품 상세 조회
  - 목록에서 상품 수정·삭제
- 공지사항
- 장바구니

## 테스트 순서

1. `backend/.env`의 Supabase URL과 service role 키를 확인합니다.
2. 백엔드를 실행하고 `/health`가 `{"status": "ok"}`를 반환하는지 확인합니다.
3. Swagger에서 고객, 인증, 상품, 장바구니, 공지사항 그룹이 표시되는지 확인합니다.
4. Swagger에서 테스트 데이터를 등록하고 Supabase 테이블에 반영되는지 확인합니다.
5. `BACKEND_URL`을 현재 백엔드 주소로 지정한 뒤 Streamlit을 실행합니다.
6. Streamlit의 각 메뉴가 열리고 API 오류 메시지가 정상적으로 표시되는지 확인합니다.

## 자주 발생하는 오류

### `ModuleNotFoundError: No module named 'backend'`

프로젝트 최상위 폴더에서 실행합니다.

```powershell
cd C:\mini\team2_0803
python -m uvicorn backend.app.main:app --reload --port 8001
```

### `ModuleNotFoundError: No module named 'app'`

백엔드 import 경로를 `from backend.app...` 형식으로 통일하고 위의 최상위 실행 명령을 사용합니다.

### Swagger에 최신 API가 보이지 않음

기존 서버가 다른 포트에서 실행 중인지 확인하고 현재 서버의 포트로 접속합니다. 브라우저에서 `Ctrl + F5`로 새로고침합니다.

### Streamlit에서 다른 프로젝트가 표시됨

기존 Streamlit 서버와 포트가 겹친 상태입니다. 현재 프로젝트를 다른 포트에서 실행합니다.

```powershell
streamlit run frontend/app.py --server.port 8502
```

## 보안 주의사항

- 비밀번호는 평문으로 저장하지 않고 PBKDF2-SHA256 해시로 저장합니다.
- 고객 API 응답에 비밀번호와 비밀번호 해시를 포함하지 않습니다.
- Supabase service role 키는 백엔드에서만 사용합니다.
- 현재 로그인/로그아웃은 수업용 세션 흐름이며 JWT 또는 서버 세션 기반 인증은 구현되어 있지 않습니다.
- 실제 운영 환경에서는 백엔드 인증·권한 검사, Supabase RLS, CORS 제한을 추가해야 합니다.

## Git 협업 흐름

```powershell
git fetch origin
git merge origin/팀원브랜치
```

머�