CREATE TABLE categories(name TEXT PRIMARY KEY,description TEXT NOT NULL DEFAULT '',section TEXT NOT NULL DEFAULT 'interest',active INTEGER NOT NULL DEFAULT 1);
INSERT INTO categories(name,section) SELECT DISTINCT category,CASE WHEN category IN ('日常生活','朋友相处','情绪与情境') THEN 'personality' ELSE 'interest' END FROM bank;
CREATE INDEX questions_parent ON questionnaire_questions(scope,parent_id);
CREATE INDEX options_parent ON questionnaire_options(scope,parent_id,question_position);
CREATE INDEX rates_expiry ON rate_limits(expires);
