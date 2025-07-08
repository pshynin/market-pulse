-- MarketPulse Database Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable TimescaleDB for time-series data (if available)
-- Uncomment if you have TimescaleDB installed
-- CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Market Data table
CREATE TABLE IF NOT EXISTS market_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    spy_price FLOAT NOT NULL,
    rsp_price FLOAT NOT NULL,
    vix_value FLOAT NOT NULL,
    pe_ratio FLOAT NOT NULL,
    eps_value FLOAT NOT NULL,
    m2_supply FLOAT,
    fed_balance FLOAT,
    gdp_value FLOAT,
    ism_value FLOAT,
    raw_data JSONB
);

-- Create index on timestamp for market_data
CREATE INDEX idx_market_data_timestamp ON market_data (timestamp DESC);

-- Signal Results table
CREATE TABLE IF NOT EXISTS signal_results (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    market_breadth_signal VARCHAR(10) NOT NULL,
    valuation_signal VARCHAR(10) NOT NULL,
    volatility_signal VARCHAR(10) NOT NULL,
    liquidity_signal VARCHAR(10) NOT NULL,
    macro_signal VARCHAR(10) NOT NULL,
    overall_signal VARCHAR(10) NOT NULL,
    market_data_id INTEGER REFERENCES market_data(id)
);

-- Create index on timestamp for signal_results
CREATE INDEX idx_signal_results_timestamp ON signal_results (timestamp DESC);

-- AI Insights table
CREATE TABLE IF NOT EXISTS ai_insights (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    content TEXT NOT NULL,
    signal_result_id INTEGER REFERENCES signal_results(id)
);

-- Create index on timestamp for ai_insights
CREATE INDEX idx_ai_insights_timestamp ON ai_insights (timestamp DESC);

-- For time-series optimization with TimescaleDB 
-- Uncomment if using TimescaleDB
-- SELECT create_hypertable('market_data', 'timestamp');
-- SELECT create_hypertable('signal_results', 'timestamp');
-- SELECT create_hypertable('ai_insights', 'timestamp');

-- Comments
COMMENT ON TABLE market_data IS 'Stores raw market data collected from APIs';
COMMENT ON TABLE signal_results IS 'Stores processed signal indicators (Green/Yellow/Red)';
COMMENT ON TABLE ai_insights IS 'Stores AI-generated market insights';
