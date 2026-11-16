import sqlite3,json,pathlib
p=pathlib.Path(__file__).resolve().parents[1]
q=json.loads((p/'data/questions.json').read_text(encoding='utf-8-sig'))
assert 300<=len(q)<=500
assert len({x['id'] for x in q})==len(q)
assert len({x['title'] for x in q})==len(q)
assert all(len(x['options'])>=2 and len(set(x['options']))==len(x['options']) and all(x['options']) and 'correct' not in x for x in q)
c=sqlite3.connect(':memory:')
for f in sorted((p/'migrations').glob('*.sql')):c.executescript(f.read_text(encoding='utf-8-sig'))
assert c.execute('select count(*) from bank').fetchone()[0]==len(q)
print(f'PASS: {len(q)} questions; uniqueness, options, no public answers, SQLite migrations')
