import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "finTrackDb")

SCHEMA = """
CREATE TABLE IF NOT EXISTS banks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    slug            TEXT    NOT NULL UNIQUE,
    name            TEXT    NOT NULL,
    description     TEXT,
    logo            TEXT,
    site            TEXT,
    phone           TEXT,
    email           TEXT,
    legal_address   TEXT,
    rating          REAL,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS bank_branches (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_id     INTEGER NOT NULL REFERENCES banks(id) ON DELETE CASCADE,
    name        TEXT    NOT NULL,
    address     TEXT,
    latitude    REAL,
    longitude   REAL,
    phone       TEXT,
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS nbu_rates (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    currency    TEXT    NOT NULL UNIQUE,
    rate        REAL    NOT NULL,
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS bank_rates (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_id     INTEGER NOT NULL REFERENCES banks(id) ON DELETE CASCADE,
    currency    TEXT    NOT NULL,
    buy         REAL,
    sell        REAL,
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE (bank_id, currency)
);

CREATE INDEX IF NOT EXISTS idx_bank_branches_bank_id  ON bank_branches(bank_id);
CREATE INDEX IF NOT EXISTS idx_bank_branches_coords   ON bank_branches(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_bank_rates_bank_id     ON bank_rates(bank_id);
CREATE INDEX IF NOT EXISTS idx_bank_rates_currency    ON bank_rates(currency);
"""
