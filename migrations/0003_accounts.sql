-- Additive only: existing owner IDs and all legacy data remain untouched.
CREATE TABLE users(id TEXT PRIMARY KEY,username TEXT NOT NULL,username_key TEXT NOT NULL UNIQUE,password_hash TEXT NOT NULL,email TEXT,recovery_hash TEXT,created INTEGER NOT NULL);
CREATE TABLE sessions(token_hash TEXT PRIMARY KEY,user_id TEXT NOT NULL REFERENCES users(id),expires INTEGER NOT NULL,created INTEGER NOT NULL);
CREATE INDEX sessions_user ON sessions(user_id);
CREATE TABLE legacy_claims(legacy_id TEXT PRIMARY KEY,user_id TEXT NOT NULL REFERENCES users(id),approved_at INTEGER NOT NULL);
