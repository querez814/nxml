-- Raw financial statement JSON from Alpha Vantage pipelines (one row per symbol + dataset).
CREATE TABLE IF NOT EXISTS financial_statement_cache (
  symbol              text        NOT NULL,
  dataset             text        NOT NULL,
  payload             jsonb       NOT NULL,
  fetched_at          timestamptz NOT NULL DEFAULT now(),
  latest_fiscal_date  date,
  source_note         text,
  PRIMARY KEY (symbol, dataset)
);

CREATE INDEX IF NOT EXISTS idx_fsc_symbol ON financial_statement_cache (symbol);
CREATE INDEX IF NOT EXISTS idx_fsc_fetched ON financial_statement_cache (fetched_at);

-- LLM / news recap responses (persistent across deploys).
CREATE TABLE IF NOT EXISTS llm_cache (
  cache_kind   text        NOT NULL,
  symbol       text        NOT NULL DEFAULT '',
  context_key  text        NOT NULL,
  payload      jsonb       NOT NULL,
  model        text,
  created_at   timestamptz NOT NULL DEFAULT now(),
  expires_at   timestamptz,
  PRIMARY KEY (cache_kind, symbol, context_key)
);

CREATE INDEX IF NOT EXISTS idx_llm_created ON llm_cache (created_at);
CREATE INDEX IF NOT EXISTS idx_llm_expires ON llm_cache (expires_at);
