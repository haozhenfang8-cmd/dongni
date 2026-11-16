ALTER TABLE documents ADD COLUMN deleted_at INTEGER;
ALTER TABLE private_questions ADD COLUMN deleted_at INTEGER;
CREATE INDEX documents_owner_deleted ON documents(owner,deleted_at);
CREATE INDEX private_owner_deleted ON private_questions(owner,deleted_at);
