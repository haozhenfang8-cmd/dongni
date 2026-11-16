import urllib.request,urllib.error,http.cookiejar,json,secrets,time,uuid
base='https://dongni-friends.pages.dev';opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def api(path,body=None,status=200):
 req=urllib.request.Request(base+'/api/'+path,data=json.dumps(body).encode() if body is not None else None,headers={'Origin':base,'Content-Type':'application/json','User-Agent':'Mozilla/5.0'})
 try:r=opener.open(req,timeout=30)
 except urllib.error.HTTPError as e:r=e
 data=json.loads(r.read());assert r.code==status,(path,r.code,data);print('PASS',path,status,flush=True);return data
name='delete_test_'+str(int(time.time()));password=secrets.token_urlsafe(24);api('auth/register',{'username':name,'password':password});api('auth/login',{'username':name,'password':password})
q={'id':'fixture','title':'删除回归测试','category':'日常生活','options':['甲','乙'],'correct':[1]};doc=api('documents',{'title':'删除测试专用','questions':[q]});v=api('publish',{'id':doc['id']});priv=api('private',q);submission={'nickname':'测试好友','answers':[1],'client':str(uuid.uuid4())};a=api('play/'+v['id']+'/submit',submission)
api('private/delete',{'id':priv['id']});assert not any(x['id']==priv['id'] for x in api('private'));assert len(api('play/'+v['id'])['questions'])==1;api('private/restore',{'id':priv['id']});assert any(x['id']==priv['id'] for x in api('private'))
api('documents/delete',{'id':doc['id']});assert not any(x['id']==doc['id'] for x in api('documents'));api('play/'+v['id'],status=410);api('play/'+v['id']+'/submit',submission,status=410);api('documents',{'id':doc['id'],'title':'stale','questions':[q]},status=409);assert any(x['id']==doc['id'] for x in api('trash')['documents']);api('documents/restore',{'id':doc['id']});again=api('play/'+v['id']+'/submit',submission);assert again['id']==a['id'] and again['score']==1
api('documents/delete',{'id':doc['id']});api('private/delete',{'id':priv['id']});api('auth/logout',{});print('PASS LIVE delete/restore: only synthetic fixtures modified; original data untouched',flush=True)
