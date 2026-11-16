-- Preserve legacy snapshots for rollback; backfill each question and answer separately.
CREATE TABLE questionnaire_questions(scope TEXT NOT NULL,parent_id TEXT NOT NULL,position INTEGER NOT NULL,question_id TEXT NOT NULL,title TEXT NOT NULL,category TEXT NOT NULL,PRIMARY KEY(scope,parent_id,position));
CREATE TABLE questionnaire_options(scope TEXT NOT NULL,parent_id TEXT NOT NULL,question_position INTEGER NOT NULL,position INTEGER NOT NULL,label TEXT NOT NULL,is_correct INTEGER NOT NULL DEFAULT 0,PRIMARY KEY(scope,parent_id,question_position,position));
CREATE TABLE attempt_answers(attempt_id TEXT NOT NULL REFERENCES attempts(id),position INTEGER NOT NULL,option_position INTEGER NOT NULL,PRIMARY KEY(attempt_id,position));
INSERT INTO questionnaire_questions SELECT 'draft',d.id,CAST(j.key AS INTEGER),COALESCE(json_extract(j.value,'$.id'),d.id||':'||j.key),json_extract(j.value,'$.title'),COALESCE(json_extract(j.value,'$.category'),'其他兴趣') FROM documents d,json_each(d.questions) j;
INSERT INTO questionnaire_questions SELECT 'version',d.id,CAST(j.key AS INTEGER),COALESCE(json_extract(j.value,'$.id'),d.id||':'||j.key),json_extract(j.value,'$.title'),COALESCE(json_extract(j.value,'$.category'),'其他兴趣') FROM versions d,json_each(d.questions) j;
INSERT INTO questionnaire_options SELECT 'draft',d.id,CAST(j.key AS INTEGER),CAST(o.key AS INTEGER),o.value,EXISTS(SELECT 1 FROM json_each(j.value,'$.correct') a WHERE a.value=CAST(o.key AS INTEGER)) FROM documents d,json_each(d.questions) j,json_each(j.value,'$.options') o;
INSERT INTO questionnaire_options SELECT 'version',d.id,CAST(j.key AS INTEGER),CAST(o.key AS INTEGER),o.value,EXISTS(SELECT 1 FROM json_each(j.value,'$.correct') a WHERE a.value=CAST(o.key AS INTEGER)) FROM versions d,json_each(d.questions) j,json_each(j.value,'$.options') o;
INSERT INTO attempt_answers SELECT a.id,CAST(j.key AS INTEGER),j.value FROM attempts a,json_each(a.answers) j;
CREATE TABLE favorites(owner TEXT NOT NULL,question_id TEXT NOT NULL,PRIMARY KEY(owner,question_id));
CREATE TABLE private_questions(id TEXT PRIMARY KEY,owner TEXT NOT NULL,body TEXT NOT NULL);
CREATE TABLE review_history(id TEXT PRIMARY KEY,submission_id TEXT NOT NULL,reviewer TEXT NOT NULL,decision TEXT NOT NULL,reason TEXT NOT NULL,created INTEGER NOT NULL);
