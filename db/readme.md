# Vector Store (PostgreSQL + PgVector)

Stores API metadata and endpoint embeddings in a relational and vector-aware format. Supports efficient similarity search.


## Starting docker

The docker compose in this directory only starts PostgreSQL + pgvector for canary test purposes.

```bash
docker compose up
```

## Connectivity test

```bash
psql -h localhost -U testuser -d vectordb -p 5432 
```

## Verify installation

```bash
SELECT * FROM pg_extension;
```

Expected output

```text
  oid  | extname | extowner | extnamespace | extrelocatable | extversion | extconfig | extcondition 
-------+---------+----------+--------------+----------------+------------+-----------+--------------
 13561 | plpgsql |       10 |           11 | f              | 1.0        |           | 
 16385 | vector  |       10 |         2200 | t              | 0.5.1      |           | 
(2 rows)
```

## Listing tables

```bash
select * from pg_catalog.pg_tables where schemaname='public';
```

Expected output

```text
vectordb=# select * from pg_catalog.pg_tables where schemaname='public';
 schemaname |   tablename   | tableowner | tablespace | hasindexes | hasrules | hastriggers | rowsecurity 
------------+---------------+------------+------------+------------+----------+-------------+-------------
 public     | apis          | testuser   |            | t          | f        | t           | f
 public     | api_endpoints | testuser   |            | t          | f        | t           | f
 public     | embeddings    | testuser   |            | t          | f        | t           | f
(3 rows)
```
