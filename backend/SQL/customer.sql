-- customers 테이블 SQL--

drop table if exists public.customers;

create table public.customers (
    id varchar(100) primary key,
    pwd text not null,
    name varchar(100) not null,
    created_at timestamp not null default now(),
    updated_at timestamp not null default now()
);

comment on table public.customers is '고객 정보';
comment on column public.customers.id is '로그인 아이디';
comment on column public.customers.pwd is 'PBKDF2로 해시한 비밀번호';
comment on column public.customers.name is '고객 이름';

insert into public.customers (id, pwd, name)
values
    (
        'test01',
        'pbkdf2_sha256$200000$00112233445566778899aabbccddeeff$12e842ab693e94a1b8932dd3300b3ef8ca560b9a5abc06a4417a9c96c0ebb415',
        '테스트사용자'
    ),
    (
        'user02',
        'pbkdf2_sha256$200000$11223344556677889900aabbccddeeff$fcb82278334242fd0e97a04d7dc8f90e7ce8a980450e06e4807a4a8a3a8a0c52',
        '일반사용자'
    ),
    (
        'admin03',
        'pbkdf2_sha256$200000$22334455667788990011aabbccddeeff$55bd41cd4dc8d78ad74710ca2e72b450b92aa18598b66c02be10cd6ba05ed8c9',
        '관리자테스트'
    );

select id, name, created_at, updated_at
from public.customers
order by id;
