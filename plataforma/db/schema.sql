-- ProspectaRadar MVP — schema Postgres (compatível com Supabase)
create extension if not exists "pgcrypto";

create table users (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  email text unique not null,
  email_verificado boolean not null default false,
  plano text not null default 'free',              -- free | assinante
  leads_gratis_liberados int not null default 25,  -- cota total
  leads_gratis_usados int not null default 0,
  criado_em timestamptz not null default now()
);

create table lead_requests (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id),
  tipo_comercio text not null,
  cidade text not null,
  uf text not null,
  quantidade int not null,
  status text not null default 'pendente',          -- pendente | processando | entregue
  criado_em timestamptz not null default now(),
  entregue_em timestamptz
);

create table leads (
  id uuid primary key default gen_random_uuid(),
  request_id uuid not null references lead_requests(id),
  user_id uuid not null references users(id),
  empresa text, cidade text, telefone text, celular boolean,
  email text, canal text, website text, situacao text, porte text,
  nota_google numeric, avaliacoes int, instagram text
);

create table lead_feedback (
  id uuid primary key default gen_random_uuid(),
  lead_id uuid unique not null references leads(id),
  user_id uuid not null references users(id),
  status text not null default 'nao_contatado',
  -- nao_contatado|contatado|respondeu|em_negociacao|fechou|sem_interesse|contato_errado
  observacao text,
  atualizado_em timestamptz not null default now()
);

create table grants (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id),
  quantidade int not null,
  motivo text,
  criado_em timestamptz not null default now()
);

create index on lead_requests(user_id);
create index on leads(request_id);
create index on leads(user_id);
