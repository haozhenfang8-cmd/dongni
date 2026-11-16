import urllib.request,urllib.error,http.cookiejar,json,secrets,time,uuid
base='https://know-me.know-me.workers.dev';jar=http.cookiejar.CookieJar();opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar));username='smoke_'+str(int(time.time()));password=secrets.token_urlsafe(24)
def api(path,body=None,expected=200):
 req=urllib.request.Request(base+'/api/'+path,data=json.dumps(body).encode() if body is not None else None,headers={'Origin':base,'Content-Type':'application/json','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36'})
 try:r=opener.open(req,timeout=40)
 except urllib.error.HTTPError as e:
  text=e.read().decode();print('FAIL',path,e.code,text[:600]);raise
 d=json.loads(r.read());assert r.status==expected;print('PASS',path,r.status);return d
bank=api('bank');assert len(bank)==320
start=time.monotonic();reg=api('auth/register',{'username':username,'password':password});print('registration wall seconds',round(time.monotonic()-start,3));assert reg.get('recovery');api('auth/login',{'username':username,'password':password});me=api('me');
q={'id':'smoke-q','title':'线上测试：请选择乙','category':'日常生活','options':['甲','乙'],'correct':[1]}
doc=api('documents',{'title':'线上验证专用','questions':[q]});v=api('publish',{'id':doc['id']});api('auth/logout',{});play=api('play/'+v['id']);assert 'correct' not in play['questions'][0]
client=str(uuid.uuid4());body={'nickname':'线上测试好友','answers':[1],'client':client,'score':999};a=api('play/'+v['id']+'/submit',body);assert a['score']==1;again=api('play/'+v['id']+'/submit',body);assert a['id']==again['id'];rank=api('play/'+v['id']+'/ranking');assert len(rank)==1
api('auth/recover',{'username':username,'password':secrets.token_urlsafe(24),'recovery':reg['recovery']});print('PRODUCTION SMOKE PASS; synthetic username',username,'user',reg['id'],'document',doc['id'],'version',v['id'])

