-- Supabase uses PostgreSQL.
-- Run this file in the Supabase SQL Editor to create the products table
-- and insert sample data.

-- Generate sequential UUID-shaped product IDs.
-- Example: 10000000-0000-4000-8000-000000000011
create sequence if not exists public.products_id_seq;

create or replace function public.next_product_id()
returns uuid
language sql
volatile
set search_path = ''
as $$
  select (
    '10000000-0000-4000-8000-'
    || lpad(nextval('public.products_id_seq')::text, 12, '0')
  )::uuid;
$$;

create table if not exists public.products (
  id uuid primary key default public.next_product_id(),
  product_name text not null,
  price integer not null check (price >= 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Also update the default when the products table already exists.
alter table public.products
  alter column id set default public.next_product_id();

comment on table public.products is 'Product catalog';
comment on column public.products.price is 'Product price in KRW';

-- Automatically update updated_at whenever a row is changed.
create or replace function public.set_products_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists products_set_updated_at on public.products;

create trigger products_set_updated_at
before update on public.products
for each row
execute function public.set_products_updated_at();

-- Fixed UUIDs make this seed section safe to run more than once.
insert into public.products (id, product_name, price)
values
  ('10000000-0000-4000-8000-000000000001', '우리쌀 10kg', 32900),
  ('10000000-0000-4000-8000-000000000002', '유기농 사과 1kg', 12900),
  ('10000000-0000-4000-8000-000000000003', '제주 삼다수 2L 6개', 6900),
  ('10000000-0000-4000-8000-000000000004', '핸드드립 커피 10개입', 8900),
  ('10000000-0000-4000-8000-000000000005', '무선 블루투스 이어폰', 49900),
  ('10000000-0000-4000-8000-000000000006', '휴대용 보조배터리 10000mAh', 25900),
  ('10000000-0000-4000-8000-000000000007', '데스크 오거나이저', 15900),
  ('10000000-0000-4000-8000-000000000008', '코튼 베이직 티셔츠', 19900),
  ('10000000-0000-4000-8000-000000000009', '스테인리스 텀블러 500ml', 17900),
  ('10000000-0000-4000-8000-000000000010', '미니 테이블 스탠드', 23900)
on conflict (id) do nothing;

-- Continue after the largest sequential sample/existing product ID.
select setval(
  'public.products_id_seq',
  greatest(
    10,
    coalesce(
      (
        select max(right(id::text, 12)::bigint)
        from public.products
        where id::text ~ '^10000000-0000-4000-8000-[0-9]{12}$'
      ),
      0
    )
  ),
  true
);
