-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create standards table with 768-dim vector embedding (gemini-embedding-001)
create table if not exists standards (
  standard_id text primary key,
  title text not null,
  scope text,
  embedding vector(768),
  latest_version text,
  amendment_date text,
  is_mandatory_qco boolean default false
);

-- Create standard_references join table for normative & allied lookups
create table if not exists standard_references (
  standard_id text references standards(standard_id) on delete cascade,
  referenced_id text,
  referenced_title text,
  relationship_type text,
  primary key (standard_id, referenced_id)
);

-- Create the match_standards vector search function
create or replace function match_standards(query_embedding vector(768), match_count int)
returns table (standard_id text, title text, similarity float)
language sql stable
as $$
  select standard_id, title, 1 - (embedding <=> query_embedding) as similarity
  from standards
  order by embedding <=> query_embedding
  limit match_count;
$$;

-- Enable Row Level Security (RLS)
alter table standards enable row level security;
alter table standard_references enable row level security;

-- Policies for standards table
create policy "Allow public read access to standards" on standards for select using (true);
create policy "Allow public insert/update to standards" on standards for all using (true) with check (true);

-- Policies for standard_references table
create policy "Allow public read access to standard_references" on standard_references for select using (true);
create policy "Allow public insert/update to standard_references" on standard_references for all using (true) with check (true);
