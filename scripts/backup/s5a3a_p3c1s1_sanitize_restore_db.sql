\set ON_ERROR_STOP on
\set QUIET on
\pset tuples_only on
\pset format unaligned
\pset footer off

BEGIN;

CREATE TEMP TABLE IF NOT EXISTS _s5a3a_sanitize_stats (
  action text NOT NULL,
  table_name text NOT NULL,
  column_name text NOT NULL,
  affected_rows bigint NOT NULL,
  note text
);

DO $$
DECLARE
  t record;
  c record;
  has_id boolean;
  row_key_expr text;
  expr text;
  sql text;
  updated bigint;
BEGIN
  -- 1) Truncate operational/event tables (lower risk of PII leakage).
  --    Keep domain tables (books/libraries/...) intact and sanitize in-place.
  FOR t IN
    SELECT schemaname, tablename
    FROM pg_catalog.pg_tables
    WHERE schemaname = 'public'
      AND (
        tablename = 'audit_log'
        OR tablename ILIKE '%outbox%'
        OR tablename ILIKE 'chronicle%'
        OR tablename = 'projection_status'
      )
  LOOP
    sql := format('TRUNCATE TABLE %I.%I RESTART IDENTITY CASCADE', t.schemaname, t.tablename);
    EXECUTE sql;
    INSERT INTO _s5a3a_sanitize_stats(action, table_name, column_name, affected_rows, note)
    VALUES ('truncate', t.tablename, '*', 0, 'RESTART IDENTITY CASCADE');
  END LOOP;

  -- 2) Sanitize TEXT/VARCHAR columns by name, across all public tables.
  FOR c IN
    SELECT
      table_schema,
      table_name,
      column_name,
      data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND data_type IN ('text', 'character varying')
      AND column_name IN (
        'name',
        'title',
        'filename',
        'storage_key',
        'description',
        'summary',
        'content',
        'text',
        'snippet',
        'manual_maturity_reason',
        'meta',
        'title_snapshot',
        'summary_snapshot'
      )
  LOOP
    SELECT EXISTS (
      SELECT 1
      FROM information_schema.columns
      WHERE table_schema = c.table_schema
        AND table_name = c.table_name
        AND column_name = 'id'
    )
    INTO has_id;

    row_key_expr := CASE WHEN has_id THEN 'id::text' ELSE 'ctid::text' END;

    IF c.column_name IN ('name', 'title', 'filename') THEN
      expr := format('''redacted_'' || substr(md5(%s), 1, 12)', row_key_expr);
    ELSIF c.column_name = 'storage_key' THEN
      expr := format('''redacted/'' || substr(md5(%s), 1, 20)', row_key_expr);
    ELSE
      -- Free-text: keep schema/row counts but eliminate sensitive content.
      -- Use non-empty marker to avoid NOT NULL / check constraints in some tables.
      expr := '''redacted''';
    END IF;

    sql := format(
      'UPDATE %I.%I SET %I = %s WHERE %I IS NOT NULL',
      c.table_schema,
      c.table_name,
      c.column_name,
      expr,
      c.column_name
    );

    EXECUTE sql;
    GET DIAGNOSTICS updated = ROW_COUNT;

    INSERT INTO _s5a3a_sanitize_stats(action, table_name, column_name, affected_rows, note)
    VALUES ('update_text', c.table_name, c.column_name, updated, row_key_expr);
  END LOOP;

  -- 3) Sanitize JSONB columns by name (best-effort).
  FOR c IN
    SELECT
      table_schema,
      table_name,
      column_name,
      data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND data_type IN ('jsonb')
      AND column_name IN (
        'meta_json',
        'data_snapshot',
        'change_details',
        'components',
        'trace_context'
      )
  LOOP
    IF c.column_name = 'components' THEN
      expr := '''[]''::jsonb';
    ELSE
      expr := '''{}''::jsonb';
    END IF;

    sql := format(
      'UPDATE %I.%I SET %I = %s WHERE %I IS NOT NULL',
      c.table_schema,
      c.table_name,
      c.column_name,
      expr,
      c.column_name
    );

    EXECUTE sql;
    GET DIAGNOSTICS updated = ROW_COUNT;

    INSERT INTO _s5a3a_sanitize_stats(action, table_name, column_name, affected_rows, note)
    VALUES ('update_jsonb', c.table_name, c.column_name, updated, expr);
  END LOOP;
END $$;

COMMIT;

SELECT jsonb_build_object(
  'kind', 's5a3a_sanitization_summary',
  'occurred_at', now(),
  'stats', COALESCE((SELECT jsonb_agg(to_jsonb(s) ORDER BY s.action, s.table_name, s.column_name) FROM _s5a3a_sanitize_stats s), '[]'::jsonb)
)::text;
