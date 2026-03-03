\set ON_ERROR_STOP on
\set QUIET on
\pset tuples_only on
\pset format unaligned

CREATE TEMP TABLE IF NOT EXISTS _s5a3a_verify_stats (
  table_name text NOT NULL,
  column_name text NOT NULL,
  non_redacted_count bigint NOT NULL,
  non_null_count bigint NOT NULL
);

DO $$
DECLARE
  c record;
  sql text;
  non_redacted bigint;
  non_null bigint;
BEGIN
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
    sql := format(
      'SELECT '
      '  count(*) FILTER (WHERE %1$I IS NOT NULL AND %1$I NOT LIKE ''redacted%%''),'
      '  count(*) FILTER (WHERE %1$I IS NOT NULL)'
      'FROM %2$I.%3$I',
      c.column_name,
      c.table_schema,
      c.table_name
    );

    EXECUTE sql INTO non_redacted, non_null;

    INSERT INTO _s5a3a_verify_stats(table_name, column_name, non_redacted_count, non_null_count)
    VALUES (c.table_name, c.column_name, COALESCE(non_redacted, 0), COALESCE(non_null, 0));
  END LOOP;
END $$;

SELECT jsonb_build_object(
  'kind', 's5a3a_sanitization_verify',
  'occurred_at', now(),
  'failures', COALESCE(
    (
      SELECT jsonb_agg(to_jsonb(v) ORDER BY v.table_name, v.column_name)
      FROM _s5a3a_verify_stats v
      WHERE v.non_redacted_count > 0
    ),
    '[]'::jsonb
  ),
  'stats', COALESCE((SELECT jsonb_agg(to_jsonb(v) ORDER BY v.table_name, v.column_name) FROM _s5a3a_verify_stats v), '[]'::jsonb)
)::text;
