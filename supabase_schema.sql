-- ==========================================================
--  AI-Driven Education Assistant — Supabase Schema
-- ==========================================================

--  Enable Row Level Security
alter database postgres set row_security = on;

-- ==========================================================
--  USERS TABLE
-- Stores basic user info (linked to Supabase Auth)
-- ==========================================================
create table if not exists public.users (
  id uuid primary key default uuid_generate_v4(),
  auth_user_id uuid references auth.users(id) on delete cascade,
  full_name text,
  email text unique not null,
  created_at timestamp with time zone default now()
);

-- Enable Row Level Security
alter table public.users enable row level security;

create policy "Users can read their own data"
  on public.users
  for select
  using (auth.uid() = auth_user_id);

create policy "Users can update their own data"
  on public.users
  for update
  using (auth.uid() = auth_user_id);

-- ==========================================================
--  MATERIALS TABLE
-- Tracks files uploaded to Supabase Storage
-- ==========================================================
create table if not exists public.materials (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references public.users(id) on delete cascade,
  filename text not null,
  storage_path text not null,
  file_type text,
  upload_date timestamp with time zone default now()
);

alter table public.materials enable row level security;

create policy "Users can read their own materials"
  on public.materials
  for select
  using (exists (
    select 1 from public.users
    where users.id = materials.user_id and users.auth_user_id = auth.uid()
  ));

create policy "Users can insert their own materials"
  on public.materials
  for insert
  with check (exists (
    select 1 from public.users
    where users.id = materials.user_id and users.auth_user_id = auth.uid()
  ));

-- ==========================================================
--  PROGRESS TABLE
-- Tracks learning progress, quiz results, and activity
-- ==========================================================
create table if not exists public.progress (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references public.users(id) on delete cascade,
  topic text,
  score int check (score >= 0 and score <= 100),
  attempts int default 1,
  last_reviewed timestamp with time zone default now()
);

alter table public.progress enable row level security;

create policy "Users can read their own progress"
  on public.progress
  for select
  using (exists (
    select 1 from public.users
    where users.id = progress.user_id and users.auth_user_id = auth.uid()
  ));

create policy "Users can insert or update their own progress"
  on public.progress
  for all
  using (exists (
    select 1 from public.users
    where users.id = progress.user_id and users.auth_user_id = auth.uid()
  ))
  with check (exists (
    select 1 from public.users
    where users.id = progress.user_id and users.auth_user_id = auth.uid()
  ));

-- ==========================================================
--  LOGS TABLE
-- Tracks question/answer sessions for analytics
-- ==========================================================
create table if not exists public.logs (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references public.users(id) on delete cascade,
  question text,
  answer text,
  created_at timestamp with time zone default now()
);

alter table public.logs enable row level security;

create policy "Users can view their own logs"
  on public.logs
  for select
  using (exists (
    select 1 from public.users
    where users.id = logs.user_id and users.auth_user_id = auth.uid()
  ));

create policy "Users can insert their own logs"
  on public.logs
  for insert
  with check (exists (
    select 1 from public.users
    where users.id = logs.user_id and users.auth_user_id = auth.uid()
  ));

-- ==========================================================
--  SUPABASE STORAGE CONFIGURATION
-- ==========================================================
-- Create a storage bucket for study materials
insert into storage.buckets (id, name, public)
values ('materials', 'materials', false)
on conflict (id) do nothing;

-- Grant authenticated users access to their files
create policy "Users can upload to their folder"
  on storage.objects
  for insert
  with check (
    bucket_id = 'materials'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

create policy "Users can read their own files"
  on storage.objects
  for select
  using (
    bucket_id = 'materials'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

-- ==========================================================
--  Done!
-- ==========================================================
