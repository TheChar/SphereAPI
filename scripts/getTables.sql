-- -- List all tables in the current schema
SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname = 'public'