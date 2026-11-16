import json,sqlite3,pathlib,tempfile
p=pathlib.Path(__file__).resolve().parents[1]
c=sqlite3.connect(':memory:')
for f in ['0001.sql','0002_seed.sql']:c.executescript((p/'migrations'/f).read_text(encoding='utf-8-sig'))
q=json.dumps([{'id':'old-q','title':'旧题目','category':'音乐','options':['甲','乙'],'correct':[1]}])
c.execute('insert into documents values (?,?,?,?,?,?)',('old-doc','github-42','旧问卷','旧简介',q,1))
c.execute('insert into versions values (?,?,?,?,?,?,?)',('old-v','old-doc','github-42','旧问卷','旧简介',q,1))
c.execute('insert into attempts values (?,?,?,?,?,?,?,?)',('old-a','old-v','老朋友','[1]',1,1,1,'old-client'))
c.commit()
backup='\n'.join(c.iterdump())
for f in ['0003_accounts.sql','0004_relational.sql','0005_bank_expansion.sql']:c.executescript((p/'migrations'/f).read_text(encoding='utf-8-sig'))
assert c.execute('select owner,questions from documents').fetchone()==('github-42',q)
assert c.execute('select title from questionnaire_questions where scope="version"').fetchone()[0]=='旧题目'
assert c.execute('select label,is_correct from questionnaire_options where scope="version" order by position').fetchall()==[('甲',0),('乙',1)]
assert c.execute('select option_position from attempt_answers').fetchone()[0]==1
assert c.execute('select score from attempts').fetchone()[0]==1
restored=sqlite3.connect(':memory:');restored.executescript(backup)
assert restored.execute('select questions from documents').fetchone()[0]==q
assert restored.execute('select count(*) from attempts').fetchone()[0]==1
print('PASS legacy migration preserves owner IDs, snapshots, version options, correct answers, attempts; SQL export/restore rehearsal')
