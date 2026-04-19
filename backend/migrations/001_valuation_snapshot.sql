-- Point-in-time snapshot of every ratio for a ticker, one row per fiscal quarter.
CREATE TABLE IF NOT EXISTS valuation_snapshot (
  symbol                      text        NOT NULL,
  fiscal_date_ending          date        NOT NULL,
  as_of_date                  timestamptz NOT NULL DEFAULT now(),
  sector                      text,
  industry                    text,

  -- capital structure
  shares_outstanding          numeric,
  market_cap                  numeric,
  enterprise_value            numeric,
  adjusted_price              numeric,
  latest_closing_price        numeric,
  latest_market_cap           numeric,
  latest_enterprise_value     numeric,

  -- price multiples
  pe_ratio                    numeric,
  pe_fwd                      numeric,
  pe_fwd_nongaap              numeric,
  peg_ratio                   numeric,
  peg_nongaap_fwd             numeric,
  ps_ttm                      numeric,
  ps_fwd                      numeric,
  pb_ratio                    numeric,
  price_to_cash_flow_ttm      numeric,
  price_to_fcf_ttm            numeric,

  -- EV multiples
  ev_to_revenue               numeric,
  ev_to_sales_fwd             numeric,
  ev_to_ebitda                numeric,
  ev_to_ebit                  numeric,
  ev_to_gross_profit          numeric,
  ev_to_fcf_ttm               numeric,
  ev_to_net_income            numeric,

  -- yield / payout
  dividend_yield              numeric,
  dividend_yield_ttm          numeric,
  dividend_per_share          numeric,
  payout_ratio                numeric,

  -- profitability / fundamentals
  profit_margin               numeric,
  operating_margin_ttm        numeric,
  roa_ttm                     numeric,
  roe_ttm                     numeric,
  book_value_per_share        numeric,
  diluted_eps_ttm             numeric,
  revenue_per_share_ttm       numeric,
  rev_growth_yoy              numeric,
  eps_growth_yoy              numeric,

  -- price context
  beta                        numeric,
  week52_high                 numeric,
  week52_low                  numeric,
  ma_50d                      numeric,
  ma_200d                     numeric,

  -- analyst
  analyst_target_price        numeric,
  analyst_rating_strong_buy   int,
  analyst_rating_buy          int,
  analyst_rating_hold         int,
  analyst_rating_sell         int,
  analyst_rating_strong_sell  int,

  PRIMARY KEY (symbol, fiscal_date_ending)
);

CREATE INDEX IF NOT EXISTS idx_valsnap_symbol ON valuation_snapshot (symbol);
CREATE INDEX IF NOT EXISTS idx_valsnap_sector ON valuation_snapshot (sector);
CREATE INDEX IF NOT EXISTS idx_valsnap_as_of  ON valuation_snapshot (as_of_date);

-- 5Y averages per ticker, refreshed whenever we touch valuation_snapshot for that symbol.
CREATE TABLE IF NOT EXISTS valuation_5y_avg (
  symbol              text        PRIMARY KEY,
  computed_at         timestamptz NOT NULL DEFAULT now(),
  pe_ratio_5y         numeric,
  pe_fwd_5y           numeric,
  ps_ttm_5y           numeric,
  pb_ratio_5y         numeric,
  ev_to_revenue_5y    numeric,
  ev_to_ebitda_5y     numeric,
  ev_to_ebit_5y       numeric,
  ev_to_gross_profit_5y numeric,
  price_to_fcf_5y     numeric,
  ev_to_fcf_5y        numeric,
  dividend_yield_5y   numeric
);
