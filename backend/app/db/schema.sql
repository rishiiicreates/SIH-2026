create extension if not exists vector;

create table if not exists standards (
  standard_id text primary key,
  title text not null,
  scope text,
  embedding vector(768),
  latest_version text,
  amendment_date text,
  is_mandatory_qco boolean default false
);

create table if not exists standard_references (
  standard_id text references standards(standard_id),
  referenced_id text,
  referenced_title text,
  relationship_type text,
  primary key (standard_id, referenced_id)
);

create or replace function match_standards(query_embedding vector(768), match_count int)
returns table (standard_id text, title text, similarity float)
language sql stable
as $$
  select standard_id, title, 1 - (embedding <=> query_embedding) as similarity
  from standards
  order by embedding <=> query_embedding
  limit match_count;
$$;
