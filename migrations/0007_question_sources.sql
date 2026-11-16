ALTER TABLE questionnaire_questions ADD COLUMN source_id TEXT;
UPDATE questionnaire_questions SET source_id=question_id WHERE question_id IN (SELECT id FROM bank);
