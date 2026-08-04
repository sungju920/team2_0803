# Team 01 CRUD 프로젝트 개발 계획서

## 1. 프로젝트 목표

Streamlit, FastAPI, Supabase를 활용하여 고객·상품·장바구니·공지사항을 관리하는 CRUD 서비스를 개발한다.

- Streamlit 기반 사용자 화면 제공
- FastAPI 기반 REST API 제공
- Supabase를 이용한 데이터 저장 및 관리
- 고객 회원가입 및 로그인 기능 제공
- 고객·상품·장바구니·공지사항별 등록, 조회, 수정, 삭제 기능 제공

개발 환경에서는 FastAPI API 문서(`/docs`)와 자동화 테스트를 통해 기능을 검증한다. 운영 환경에서는 환경변수를 통한 비밀값 관리, 비밀번호 암호화, 인증 및 권한 검사를 적용한다.

## 2. 범위와 완료 기준

| 구분          | 완료 기준                                                                                            |
| ------------- | ---------------------------------------------------------------------------------------------------- |
| 고객 관리     | 회원가입, 단건 조회, 수정, 삭제가 Supabase `customers` 테이블과 정상 연동된다.                       |
| 인증          | 올바른 아이디와 비밀번호로 로그인할 수 있으며, 잘못된 인증 요청은 구분된 오류를 반환한다.            |
| 상품 관리     | 상품 생성, 목록 조회, 단건 조회, 수정, 삭제가 Supabase `products` 테이블과 정상 연동된다.            |
| 장바구니 관리 | 장바구니 항목 생성, 목록 조회, 단건 조회, 수정, 삭제가 Supabase `cart_items` 테이블과 정상 연동된다. |
| 공지사항 관리 | 공지사항 생성, 목록 조회, 단건 조회, 수정, 삭제가 Supabase `notices` 테이블과 정상 연동된다.         |
| 프론트엔드    | Streamlit의 각 관리 페이지에서 FastAPI를 호출하고 처리 결과와 오류를 사용자에게 표시한다.            |
| 입력값 검증   | 필수값, 문자열 길이, 가격, 수량 등을 Pydantic 스키마에서 검증한다.                                   |
| 보안          | Supabase 키와 인증 관련 비밀값은 `.env`로 관리하고 Git에 포함하지 않는다.                            |

## 3. 업무 분담

| 담당자 | 담당 기능            | 테이블 및 모듈                                        |
| ------ | -------------------- | ----------------------------------------------------- |
| 성엽   | 고객 관리            | `customers`                                           |
| 병훈   | 상품 관리            | `products`                                            |
| 지혜   | 장바구니 관리        | `cart_items`                                          |
| 환석   | 공지사항 관리        | `notices`                                             |
| 성주   | 로그인 및 인증       | `auth`                                                |
| 공통   | 앱 설정 및 공통 통신 | FastAPI 앱, Supabase 클라이언트, Streamlit API 서비스 |

각 담당자는 자신의 기능에 해당하는 router, schema, service, Streamlit 페이지를 구현한다.

## 4. 목표 디렉터리 구조

```
.
├── backend/
│   └── app/
│       ├── main.py                       # FastAPI 앱 및 라우터 등록
│       ├── core/
│       │   └── supabase_client.py        # Supabase 클라이언트 생성
│       ├── routers/
│       │   ├── customers_routers.py      # 고객 API
│       │   ├── products_routers.py       # 상품 API
│       │   ├── cart_items_routers.py     # 장바구니 API
│       │   ├── notices_routers.py        # 공지사항 API
│       │   └── auth_routers.py           # 인증 API
│       ├── schemas/
│       │   ├── customer_schemas.py
│       │   ├── product_schemas.py
│       │   ├── cart_item_schemas.py
│       │   ├── notice_schemas.py
│       │   └── auth_schemas.py
│       └── services/
│           ├── customer_service.py
│           ├── product_service.py
│           ├── cart_item_service.py
│           ├── notice_service.py
│           └── auth_service.py
├── frontend/
│   ├── app.py                            # Streamlit 메인 화면
│   ├── pages/
│   │   ├── 01_customers.py
│   │   ├── 02_products.py
│   │   ├── 03_cart_items.py
│   │   ├── 04_notices.py
│   │   └── 05_login.py
│   └── core/
│       └── api_client.py              # FastAPI 호출 공통 모듈
├── docs/
│   └── schema.sql                        # Supabase 테이블 생성 SQL
├── .env.example
├── .gitignore
├── PLAN.md
├── README.md
└── requirements.txt
```

## 5. 데이터베이스 계획

### 5.1 공통 규칙

- 테이블 간 Foreign Key는 사용하지 않는다.
- 각 테이블은 독립적으로 관리한다.
- 모든 테이블은 `id`, `created_at`, `updated_at` 컬럼을 가진다.
- 가격과 수량은 정수형으로 저장한다.
- 생성일과 수정일은 timezone이 포함된 timestamp 타입을 사용한다.
- 테이블 생성 SQL은 `docs/schema.sql`에서 관리한다.

### 5.2 고객 테이블

테이블명: `customers`

| 컬럼명        | 타입         | 제약 및 설명                   |
| ------------- | ------------ | ------------------------------ |
| id            | varchar(100) | 로그인 아이디, 필수, 중복 불가 |
| pwd           | text         | 암호화된 비밀번호, 필수        |
| name          | varchar(100) | 고객 이름, 필수                |
| created_at    | timestamptz  | 생성 시각                      |
| updated_at    | timestamptz  | 수정 시각                      |

비밀번호는 평문으로 저장하지 않고 bcrypt 등의 단방향 해시를 적용한다.

### 5.3 상품 테이블

테이블명: `products`

| 컬럼명       | 타입         | 제약 및 설명           |
| ------------ | ------------ | ---------------------- |
| id           | auto         | Primary Key, 자동 증가 |
| product_name | varchar(200) | 상품명, 필수           |
| price        | integer      | 가격, 0 이상의 정수    |
| created_at   | timestamp  | 생성 시각              |
| updated_at   | timestamp  | 수정 시각              |

### 5.4 장바구니 테이블

테이블명: `cart_items`

| 컬럼명       | 타입         | 제약 및 설명           |
| ------------ | ------------ | ---------------------- |
| id           | auto         | Primary Key, 자동 증가 |
| product_id   | str          | 상품 식별자            |
| product_name | varchar(200) | 상품명                 |
| quantity     | integer      | 수량, 1 이상의 정수    |
| created_at   | timestamptz  | 생성 시각              |
| updated_at   | timestamptz  | 수정 시각              |

Foreign Key를 사용하지 않으므로 상품 삭제 시 장바구니 데이터가 자동 삭제되지 않는다. 필요한 경우 서비스 계층에서 별도로 처리한다.

### 5.5 공지사항 테이블

테이블명: `notices`

| 컬럼명     | 타입         | 제약 및 설명           |
| ---------- | ------------ | ---------------------- |
| id         | auto         | Primary Key, 자동 증가 |
| title      | varchar(200) | 제목, 필수             |
| content    | text         | 내용, 필수             |
| writer     | varchar(100) | 작성자, 필수           |
| created_at | timestamptz  | 생성 시각              |
| updated_at | timestamptz  | 수정 시각              |

## 6. API 계획

### 6.1 공통 및 인증 API

| 기능           | 메서드 | 경로           | 성공 응답        |
| -------------- | ------ | -------------- | ---------------- |
| 서버 상태 확인 | GET    | `/health`      | 서버 상태        |
| 회원가입       | POST   | `/customers`   | 생성된 고객 정보 |
| 로그인         | POST   | `/auth/login`  | 인증 정보        |
| 로그아웃       | POST   | `/auth/logout` | 로그아웃 결과    |

### 6.2 고객 API

| 기능           | 메서드 | 경로                       | 성공 응답   |
| -------------- | ------ | -------------------------- | ----------- |
| 고객 목록 조회 | GET    | `/customers`               | 고객 목록   |
| 고객 단건 조회 | GET    | `/customers/{customer_id}` | 고객 한 건  |
| 고객 정보 수정 | PUT    | `/customers/{customer_id}` | 수정된 고객 |
| 고객 삭제      | DELETE | `/customers/{customer_id}` | 삭제 결과   |

고객 API 응답에는 비밀번호 또는 비밀번호 해시를 포함하지 않는다.

### 6.3 상품 API

| 기능           | 메서드 | 경로                     | 성공 응답   |
| -------------- | ------ | ------------------------ | ----------- |
| 상품 생성      | POST   | `/products`              | 생성된 상품 |
| 상품 목록 조회 | GET    | `/products`              | 상품 목록   |
| 상품 단건 조회 | GET    | `/products/{product_id}` | 상품 한 건  |
| 상품 수정      | PUT    | `/products/{product_id}` | 수정된 상품 |
| 상품 삭제      | DELETE | `/products/{product_id}` | 삭제 결과   |

### 6.4 장바구니 API

| 기능               | 메서드 | 경로                         | 성공 응답     |
| ------------------ | ------ | ---------------------------- | ------------- |
| 장바구니 항목 생성 | POST   | `/cart-items`                | 생성된 항목   |
| 장바구니 목록 조회 | GET    | `/cart-items`                | 장바구니 목록 |
| 장바구니 단건 조회 | GET    | `/cart-items/{cart_item_id}` | 장바구니 항목 |
| 장바구니 항목 수정 | PUT    | `/cart-items/{cart_item_id}` | 수정된 항목   |
| 장바구니 항목 삭제 | DELETE | `/cart-items/{cart_item_id}` | 삭제 결과     |

### 6.5 공지사항 API

| 기능               | 메서드 | 경로                   | 성공 응답       |
| ------------------ | ------ | ---------------------- | --------------- |
| 공지사항 생성      | POST   | `/notices`             | 생성된 공지사항 |
| 공지사항 목록 조회 | GET    | `/notices`             | 공지사항 목록   |
| 공지사항 단건 조회 | GET    | `/notices/{notice_id}` | 공지사항 한 건  |
| 공지사항 수정      | PUT    | `/notices/{notice_id}` | 수정된 공지사항 |
| 공지사항 삭제      | DELETE | `/notices/{notice_id}` | 삭제 결과       |

## 7. 진행 순서

1. 프로젝트 디렉터리와 기본 실행 파일을 구성한다.
2. `.env.example`에 Supabase URL, API 키, 백엔드 URL을 문서화한다.
3. `docs/schema.sql`을 작성하고 Supabase SQL Editor에서 실행한다.
4. 공통 Supabase 클라이언트와 오류 처리 방식을 구현한다.
5. 각 담당자가 자신의 schema, service, router를 구현한다.
6. FastAPI `/docs`에서 각 API의 정상 흐름과 오류 응답을 확인한다.
7. Streamlit 페이지에서 FastAPI API를 호출하도록 연동한다.
8. 로그인, 비밀번호 암호화, 인증 및 권한 검사를 구현한다.
9. 정상 흐름과 예외 상황에 대한 자동화 테스트를 작성한다.
10. README에 설치, 환경설정, 실행, 테스트 방법을 작성한다.

## 8. 테스트 체크리스트

### 고객 및 인증

- 정상 회원가입
- 아이디 중복 가입
- 빈 아이디, 비밀번호, 고객 이름
- 올바른 아이디와 비밀번호 로그인
- 존재하지 않는 아이디 로그인
- 잘못된 비밀번호 로그인
- 존재하는 고객 조회·수정·삭제
- 존재하지 않는 고객 조회·수정·삭제
- 고객 응답에서 비밀번호 제외 여부

### 상품

- 정상 상품 생성
- 빈 상품명
- 음수 가격
- 상품 목록 및 단건 조회
- 존재하지 않는 상품 조회
- 정상 수정 및 삭제
- 데이터베이스 요청 실패

### 장바구니

- 정상 장바구니 항목 생성
- 0 이하의 수량
- 장바구니 목록 및 단건 조회
- 존재하지 않는 항목 조회
- 정상 수정 및 삭제
- 존재하지 않는 상품 ID 입력 처리

### 공지사항

- 정상 공지사항 생성
- 빈 제목, 내용, 작성자
- 공지사항 목록 및 단건 조회
- 존재하지 않는 공지사항 조회
- 정상 수정 및 삭제

### 공통

- 잘못된 입력에 대한 422 응답
- 존재하지 않는 데이터에 대한 404 응답
- Supabase 연결 실패에 대한 일관된 오류 응답
- Streamlit에서 API 오류 메시지 표시
- 생성일과 수정일 처리
- 목록 조회 결과의 정렬 기준

## 9. 보안 및 운영 원칙

- `.env`는 저장소에 커밋하지 않는다.
- Supabase URL과 키는 환경변수로만 관리한다.
- Supabase service-role 키는 FastAPI 백엔드에서만 사용한다.
- 비밀번호는 평문으로 저장하거나 로그에 출력하지 않는다.
- API 응답에 비밀번호 및 비밀번호 해시를 포함하지 않는다.
- 로그에 사용자 비밀번호, 인증 토큰, Supabase 키를 기록하지 않는다.
- Streamlit이 Supabase에 직접 접근하지 않고 FastAPI를 통해 접근하도록 구성한다.
- 운영 환경에서는 CORS 허용 주소를 실제 Streamlit 서비스 주소로 제한한다.
- 데이터 생성·수정·삭제 API에는 인증과 권한 검사를 적용한다.
- Supabase 테이블에는 운영 환경에 맞는 RLS 정책을 적용한다.