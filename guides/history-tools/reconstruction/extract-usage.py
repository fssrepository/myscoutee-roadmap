import pathlib,json,sqlite3,subprocess,collections,datetime,re,time,os
R=pathlib.Path('/home/USER/workspace');O=pathlib.Path(__file__).resolve().parent
os.umask(0o077)
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args],text=True).strip()
paths=['myscoutee-backend','myscoutee-backend/frontend','myscoutee-registry','myscoutee-payment-simulator','myscoutee-client','myscoutee-client-admin','myscoutee-mcp','myscoutee-agent','myscoutee-old']
oldmap={}
for folder in R.glob('history-cleanup-20260930-*'):
 f=folder/'manifest.json'
 if not f.exists():continue
 for repo in json.loads(f.read_text()):
  for group in repo.get('groups',[]):oldmap[group['new']]=group
c=sqlite3.connect('file:/home/USER/.codex/state_5.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
rows=[dict(x) for x in c.execute("select id,cwd,title,rollout_path,model,reasoning_effort,tokens_used,created_at,updated_at,git_sha,git_origin_url,source,agent_role,agent_path,first_user_message from threads where cwd like '%myscoutee%' or git_origin_url like '%myscoutee%' order by created_at")]
(O/'thread-metadata.json').write_text(json.dumps(rows,indent=2)+'\n')
keys=['input_tokens','cached_input_tokens','cache_write_input_tokens','output_tokens','reasoning_output_tokens','total_tokens']
def stamp(v):
 try:return datetime.datetime.fromisoformat(v.replace('Z','+00:00')).timestamp()
 except:return 0
out=[];seen_responses=set();bytes_read=0;started=time.time()
for n,row in enumerate(rows):
 kind='root' if row['source']=='vscode' else 'review' if 'guardian' in row['source'] else 'subagent'
 if kind=='root':row=dict(row);row['created_at']=0
 parent=None
 try:parent=json.loads(row['source']).get('subagent',{}).get('thread_spawn',{}).get('parent_thread_id')
 except:pass
 stat={k:row[k] for k in ['id','title','model','reasoning_effort','tokens_used','created_at','updated_at','git_sha']}
 stat.update(kind=kind,parent_id=parent,usage={},events=[],turns=[],prompts=[],outcomes=[],counter_resets=0,repeated_counters=0,partial_initial_counter=False)
 prev=None;model=None;effort=None;turn=None;times=[];modern=[];turn_models={}
 with open(row['rollout_path'],'rb') as f:
  for line in f:
   bytes_read+=len(line)
   head=line[:220].replace(b' ',b'')
   if b'"type":"turn_context"' not in head and b'"type":"event_msg"' not in head and b'"type":"token_usage_record"' not in head:continue
   try:event=json.loads(line)
   except:continue
   p=event.get('payload',{});ts=stamp(event.get('timestamp',''))
   if event['type']=='turn_context':
    model=p.get('model',model);effort=p.get('effort',p.get('reasoning_effort',effort));turn=p.get('turn_id')
    turn_models[turn]=(model,effort)
    if ts>=row['created_at']-2:stat['turns'].append(dict(timestamp=ts,model=model,effort=effort,turn_id=turn))
    continue
   if event['type']=='token_usage_record':
    rid=p.get('response_id');tid=p.get('turn_id');usage=p.get('usage')
    if ts>=row['created_at']-2 and p.get('thread_id')==row['id'] and rid and rid not in seen_responses and usage:
     seen_responses.add(rid);m,ef=turn_models.get(tid,(model,effort))
     modern.append(dict(timestamp=ts,model=m,effort=ef,turn_id=tid,response_id=rid,**{k:usage.get(k,0) for k in keys}))
    continue
   typ=p.get('type')
   if typ=='token_count' and p.get('info'):
    info=p['info'];total=info.get('total_token_usage');last=info.get('last_token_usage')
    if not total:continue
    if ts<row['created_at']-2:prev=total;continue
    if prev==total:stat['repeated_counters']+=1;continue
    if prev and total.get('total_tokens',0)>=prev.get('total_tokens',0):
     delta={k:max(0,total.get(k,0)-prev.get(k,0)) for k in keys}
    else:
     if prev:stat['counter_resets']+=1
     delta={k:(last or total).get(k,0) for k in keys}
     if not prev and last and total.get('total_tokens',0)>last.get('total_tokens',0):stat['partial_initial_counter']=True
    prev=total
    if not delta['total_tokens']:continue
    label=(model or 'unknown')+'|'+(effort or 'unknown');bucket=stat['usage'].setdefault(label,{k:0 for k in keys})
    for k in keys:bucket[k]+=delta[k]
    stat['events'].append(dict(timestamp=ts,model=model,effort=effort,turn_id=turn,**delta));times.append(ts)
   elif ts>=row['created_at']-2:
    if typ=='item_completed' and kind=='root':
     item=p.get('item',{});it=item.get('type')
     if it=='UserMessage':
      msg='\n'.join(c.get('text','') for c in item.get('content',[]) if c.get('type')=='text')
      stat['prompts'].append(dict(timestamp=ts,text=msg[-6000:]))
     elif it=='AgentMessage':
      msg='\n'.join(c.get('text','') for c in item.get('content',[]) if c.get('type') in ['Text','text'])
      if item.get('phase') in ['final','final_answer']:stat['outcomes'].append(dict(timestamp=ts,text=msg[:6000]))
    if typ in ['task_started','task_complete','turn_aborted']:stat.setdefault('activity_events',[]).append(dict(timestamp=ts,type=typ,turn_id=p.get('turn_id')))
    if typ=='user_message' and kind=='root':
     msg=p.get('message','')
     if isinstance(msg,str) and len(msg)<100000:stat['prompts'].append(dict(timestamp=ts,text=msg[:1800]))
    elif typ=='agent_message' and kind=='root':
     msg=p.get('message','')
     if isinstance(msg,str) and len(msg)<100000 and p.get('phase')=='final':stat['outcomes'].append(dict(timestamp=ts,text=msg[:5000]))
 if modern:
  stat['events']=modern;stat['usage']={};times=[e['timestamp'] for e in modern];stat['accounting']='unique_response_id'
  for e in modern:
   label=(e['model'] or 'unknown')+'|'+(e['effort'] or 'unknown');bucket=stat['usage'].setdefault(label,{k:0 for k in keys})
   for k in keys:bucket[k]+=e[k]
 else:stat['accounting']='cumulative_delta'
 if times:
  stat['first_usage_at']=min(times);stat['last_usage_at']=max(times)
  # Presentational activity proxy: gaps beyond 15 minutes are not counted as continuous work.
  stat['activity_gap_capped_seconds']=sum(min(max(0,b-a),900) for a,b in zip(sorted(times),sorted(times)[1:]))
 out.append(stat)
 if (n+1)%25==0:print('History scan:',n+1,'/',len(rows),'threads;',round(bytes_read/1e9,2),'GB;',round(time.time()-started),'seconds',flush=True)
(O/'session-usage.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
summary={'threads':len(out),'categories':dict(collections.Counter(x['kind'] for x in out)),'models':dict(collections.Counter(t['model'] for x in out for t in x['turns'])),'bytes_scanned':bytes_read,'seconds':time.time()-started,'roots_with_outcomes':sum(bool(x['outcomes']) for x in out if x['kind']=='root')}
(O/'extraction-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)
