import json,pathlib,collections,datetime,re,math,bisect,csv
P=pathlib.Path(__file__).parent
repos=json.loads((P/'commits.json').read_text()); sessions=json.loads((P/'session-usage.json').read_text()); account=json.loads((P/'account-usage.json').read_text())
T={}; links=collections.defaultdict(list)
def task(key,title,area='Product',commits=()):
 t={'key':key,'title':title,'area':area,'commits':[],'days':{},'models':{},'sessions':set(),'activity_seconds':0};T[key]=t
 for ri,ci in commits:attach(key,ri,ci)
 return t
def attach(key,ri,ci):
 c=repos[ri]['commits'][ci-1];T[key]['commits'].append({'repo':repos[ri]['path'],'index':ci,'sha':c['sha'],'title':c['title'],'start':c['original_start'][:10],'end':c['original_end'][:10],'original_count':len(c['original_commits']),'execution_start':c['original_start'],'execution_end':c['original_end']});links[c['sha']].append(key)
for i,c in enumerate(repos[0]['commits'],1):
 area='Product'
 if i in [37]:area='Marketing'
 if i in [45,46,53,62,63,64]:area='Creative'
 if i in [16,24,40,42,67,69,72,81,83,85,86]:area='Operations'
 if i in [15,18,19,43,44,49,51,55,56,57,59,61,65,66,68,74,75,78,79,80,84]:area='QA and release'
 task('B'+str(i),c['title'],area,[(0,i)])
for i in range(1,7):task('F'+str(i),repos[1]['commits'][i-1]['title'],'Product',[(1,i)])
fm={7:1,8:1,9:1,10:2,11:3,12:4,13:5,14:6,15:7,16:8,17:9,18:10,19:11,20:12,21:13,22:14,23:16,24:17,25:18,26:20,27:21,28:22,29:22,30:23,31:24,32:25,33:25,34:26,35:27,36:27,37:28,38:29,39:30,40:30,41:32,42:34,43:35,44:38,45:39,46:41,47:44,48:48,49:49,50:50,51:54,52:55,53:56,54:57,55:58,56:59,57:60,58:65,59:67,60:68,61:69,62:70,63:72,64:73,65:74,66:75,67:76,68:77,69:78,70:79,71:80,72:82,73:83,74:84,75:84}
for fi,bi in fm.items():attach('B'+str(bi),1,fi)
# Mixed consolidated commits keep one tree and can reference several tasks.
for fi,bi in [(22,15),(25,19),(30,22),(31,23),(41,31),(42,33),(43,36),(46,40),(47,43),(50,52),(57,61),(58,66),(62,71),(71,81)]:attach('B'+str(bi),1,fi)
for i,b in {1:38,2:38,3:39,4:39,5:39,6:39,7:39,8:39,9:39,10:40,11:41,12:68,15:78,16:86}.items():attach('B'+str(b),2,i)
task('REGDOC','License and document the Registry release','Operations',[(2,13)])
task('REGSEC','Update Registry toolchain and security dependencies','Operations',[(2,14)])
task('SIM','Build persistent Stripe and Barion payment simulation','Tooling',[(3,1)])
for i,b in {2:58,3:58,4:58,5:60,6:60,7:76}.items():attach('B'+str(b),3,i)
for i,b in {1:71,2:73,3:77}.items():attach('B'+str(b),4,i)
task('ADMIN','Build and package the desktop administrator monitor','Tooling',[(5,1)])
attach('B78',5,2)
task('MCP','Introduce the MCP service and scoped OAuth integration','Tooling',[(6,1)])
attach('B80',6,2);attach('B86',6,3)
task('AGENT','Build the standalone trust decision agent','Tooling',[(7,1)])
task('OLD','Import the archived MyScoutee frontend prototype','Legacy manual',[(8,1)])
for i in range(2,5):task('OLD'+str(i),repos[8]['commits'][i-1]['title'],'Legacy manual',[(8,i)])
for i,c in enumerate(repos[9]['commits'],1):task('E'+str(i),c['title'],'Administration portal',[(9,i)])
for i in list(range(1,12))+[15]:task('M'+str(i),repos[10]['commits'][i-1]['title'],'Mathematical research',[(10,i)])
task('MCOMM','Review research correspondence and document claim limitations','Research communication')
# Explicitly separate creative deliverables from application/QA work in mixed commits.
T['B45']['title']='Write and publish MyScoutee story and book editions'
T['B46']['title']='Develop film shot prompts and frame continuity'
T['B47']['title']='Refine checkout participation state'
T['B48']['title']='Qualify entry and ticket lifecycle with demo fixtures'
T['B51']['title']='Publish the reusable QA guidance'
task('NARRATION','Edit video narration and subtitle timing','Creative',[(0,47)])
task('REEL','Produce the MyScoutee product reel and short promotional edits','Marketing',[(0,48)])
task('BOOKS','Translate, revise and prepare paperback book editions','Creative',[(0,45),(0,46),(0,51)])
task('PROMO','Produce social banners, promotional images and advertising copy','Marketing')
task('RESEARCHVIDEO','Prepare the Navier–Stokes research video and presentation','Research communication',[(10,12)])
task('M16','Prepare research video assets and production handoff','Research communication',[(10,13)])
task('M17','Finalize the research video and publication package','Research communication',[(10,14)])
AUDIT=pathlib.Path('/home/USER/workspace/myscoutee-backend/guides/story/london/cinema_studio_steps/04_tracking/production_audit')
frozen=json.loads((AUDIT/'summary.json').read_text())
task('STORY','Develop the storyboard and source-film production plan','Creative',[(0,45)])
task('FLOW','Run early AI-video experiments and develop the source story','Creative',[(0,45)])
task('AUDIOBOOK','Prepare audiobook material and Kindle editions','Creative',[(0,51)])
task('PAPERBACK','Correct and package paperback editions','Creative',[(0,51)])
task('MASTER','Review and adapt the festival master prompt for production','Creative',[(0,62)])
phase_keys={1:'STORY',2:'FLOW',3:'B45',4:'B46',5:'BOOKS',6:'REEL',7:'AUDIOBOOK',8:'PAPERBACK',9:'B53',10:'MASTER',11:'B62',12:'B63',13:'NARRATION',14:'B64'}
T['NARRATION']['commits']=[];links[repos[0]['commits'][46]['sha']].remove('NARRATION');attach('NARRATION',0,64);attach('B46',0,47)
# The frozen production metrics are reused unchanged; later work is kept separate.
for ph in frozen['phases']:
 k=phase_keys[int(ph['phase'][:2])];T[k]['frozen_audit_phase']=ph
T['B46']['title']='Produce the earlier Part I and Part II films and continuity repairs'
T['B53']['title']='Prepare the festival master-prompt package and local title'
T['NARRATION']['title']='Assemble the festival film, narration and voice tests'
frozen_windows=collections.defaultdict(list)
def ts(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
for m in frozen['manifest']:frozen_windows[m['session_id']].append((ts(m['first']),ts(m['last'])))
def isfrozen(sid,stamp):return any(a<=stamp<=b for a,b in frozen_windows.get(sid,[]))
frozen_daily=collections.defaultdict(collections.Counter);frozen_models=collections.defaultdict(lambda:collections.defaultdict(collections.Counter))
for row in csv.DictReader((AUDIT/'responses.csv').open()):
 k=phase_keys[int(row['phase'][:2])];d=row['ts'][:10];frozen_daily[d][k]+=int(row['total_tokens']);label=row['model']+'|'+row['reasoning_effort']
 for name in ['input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens','total_tokens']:frozen_models[k][label][name]+=int(row[name])
 T[k]['sessions'].add(row['session_id'])
# The dated tasks are reconstructed from actual commit dates. New issue creation is separate.
for t in T.values():
 if t['commits']:
  t['start']=min(c['start'] for c in t['commits']);t['end']=max(c['end'] for c in t['commits'])
 else:t['start']='2026-08-01';t['end']='2026-09-30'

def words(s):
 s=s.lower();s=re.sub(r'https?://\S+',' ',s);return set(re.findall(r'[a-záéíóöőúüű]{4,}',s))
stop=words('with from this that refine complete introduce record publish align finalize update changes backend frontend myscoutee http into over about user task context setup open tabs request codex project repository guides shared support state lifecycle')
def vocab(s):return words(s)-stop
for t in T.values():t['_words']=vocab(t['title']+' '+' '.join(c['title'] for c in t['commits']))
outside_ids={e['id'] for e in json.loads((P/'additional-history-files.json').read_text()) if 'millennium-math-problems' in (e.get('cwd') or '')}
byid={s['id']:s for s in sessions}
def rootof(s):
 seen=set()
 while s.get('parent_id') in byid and s['id'] not in seen:
  seen.add(s['id']);s=byid[s['parent_id']]
 return s

def day(ts):return datetime.datetime.fromtimestamp(ts,datetime.timezone.utc).date().isoformat()
def daynum(s):return datetime.date.fromisoformat(s).toordinal()
def media_kind(text):
 x=text.lower()
 if re.search(r'navier|stokes',x):
  return 'MCOMM' if re.search(r'email|levél|válasz|readme|locate|keresd',x) else 'RESEARCHVIDEO'
 if re.search(r'e-k[oö]zig',x):return 'EKO'
 if re.search(r'bartek|levelére|email session',x):return 'UNASSIGNED'
 if re.search(r'paperback|könyv|konyv|book|blurb',x):return 'BOOKS'
 if re.search(r'facebook|instagram|youtube.banner|promóké|promoké|reklám|reklam|linkedin',x):return 'PROMO'
 if re.search(r'narrat|narráció|felirat|subtitle|indiai|beszéd',x):return 'NARRATION'
 if re.search(r'reel|promóvide|promovide',x):return 'REEL'
 if re.search(r'higgsfield|cinema|vide[oó]|storyboard|story.shot|film|frame|openart|seedance',x):return 'FILM'
 return None

choice_cache={}
def choose(s,e):
 root=rootof(s);d=day(e['timestamp']);root_title=re.split(r'##? My request(?: for Codex)?:',root['title'])[-1];text=root_title
 # Recent user instructions disambiguate long multi-topic sessions without publishing private text.
 ps=root.get('prompts',[])
 idx=bisect.bisect_right([p['timestamp'] for p in ps],e['timestamp'])-1
 if idx>=0:
  msg=ps[idx]['text'].split('## My request:')[-1].split('## My request for Codex:')[-1]
  text+=' '+msg[-3500:]
 cachekey=(root['id'],d,idx)
 if cachekey in choice_cache:return choice_cache[cachekey]
 mk=media_kind(root_title)
 # Explicit project ownership overrides the inherited IDE cwd.
 if root['id'] in outside_ids:
  mk='MATH'
 if re.search(r'e-k[oö]zig',root_title,re.I):mk='EKO'
 if mk in ['MATH','EKO']:
  prefix='M' if mk=='MATH' else 'E'
  candidates=[t for t in T.values() if re.fullmatch(prefix+r'\d+',t['key']) and t['key'] not in ['M16','M17']]
  result=min(candidates,key=lambda t:min(max(ts(c['execution_start'])-e['timestamp'],e['timestamp']-ts(c['execution_end']),0)/3600 for c in t['commits'])-.1*len(vocab(text)&t['_words']))['key']
  choice_cache[cachekey]=result;return result
 if mk in ['BOOKS','NARRATION','REEL','FILM']:
  return 'PROMO'
 if mk=='RESEARCHVIDEO':
  return min(['RESEARCHVIDEO','M16','M17'],key=lambda k:min(max(ts(c['execution_start'])-e['timestamp'],e['timestamp']-ts(c['execution_end']),0) for c in T[k]['commits']))
 if mk:return mk
 if root['id']=='01a0f413-b718-7533-8886-b01664c027d3':
  return 'B86' if re.search(r'compose|docker|restart|prod|e2e',text[-2500:],re.I) else 'B85'
 ws=vocab(text)
 candidates=[]
 for t in T.values():
  if t['key'] in ['B85','B86','MCOMM'] or re.fullmatch(r'(?:E|M|OLD)\d*',t['key']):continue
  if re.search(r'qa|teszt|test',root_title,re.I) and t['area']=='Operations':continue
  if t['key'] in ['PROMO','RESEARCHVIDEO','NARRATION','BOOKS','REEL','OLD']:continue
  if t.get('frozen_audit_phase'):continue
  if mk=='FILM' and t['area']!='Creative':continue
  if mk is None and t['area']=='Creative':continue
  dist=max(daynum(t['start'])-daynum(d),daynum(d)-daynum(t['end']),0)
  if dist>4:continue
  overlap=len(ws&t['_words'])
  score=overlap*1.5-dist*3
  if t['start']<=d<=t['end']:score+=6
  # Avoid giving a long-running simulator's entire date window precedence over current work.
  score-=math.log2(max(1,daynum(t['end'])-daynum(t['start'])+1))*.4
  score+=min(2,math.log2(1+sum(c['original_count'] for c in t['commits']))*.15)
  candidates.append((score,t['key']))
 result=max(candidates)[1] if candidates else 'UNASSIGNED';choice_cache[cachekey]=result;return result

raw=collections.defaultdict(lambda:collections.defaultdict(collections.Counter)); sidmap=collections.defaultdict(collections.Counter)
keys=['input_tokens','cached_input_tokens','cache_write_input_tokens','output_tokens','reasoning_output_tokens','total_tokens']
for s in sessions:
 if s['kind']=='review':continue
 for e in s['events']:
  d=day(e['timestamp'])
  if d>'2026-09-30' or isfrozen(s['id'],e['timestamp']):continue
  k=choose(s,e);model=e.get('model') or s.get('model') or 'unknown';eff=e.get('effort') or 'unknown'
  label=model+'|'+eff
  for f in keys:raw[d][k][label+'::'+f]+=e.get(f,0)
  sidmap[s['id']][k]+=e['total_tokens']
  if k in T:T[k]['sessions'].add(s['id'])
 # Same task-interval union method as the existing production audit.
 if s['kind']=='root':
  active=None;intervals=[]
  for ae in s.get('activity_events',[]):
   at=ae['timestamp']
   if ae['type']=='task_started':
    if active is not None:intervals.append((active,at))
    active=at
   elif active is not None:
    intervals.append((active,at));active=None
  if active is not None and s['events']:intervals.append((active,max(active,s['events'][-1]['timestamp'])))
  for a,b in intervals:
   if day(a)>'2026-09-30' or isfrozen(s['id'],a):continue
   k=choose(s,{'timestamp':a})
   if k in T and not T[k].get('frozen_audit_phase'):T[k].setdefault('intervals',[]).append((a,b))
def union(xs):
 out=[]
 for a,b in sorted(xs):
  if b<a:continue
  if out and a<=out[-1][1]:out[-1][1]=max(out[-1][1],b)
  else:out.append([a,b])
 return out
time_intervals=[{'task_key':t['key'],'start':a,'end':b,'basis':'logged root interval'} for t in T.values() for a,b in union(t.get('intervals',[]))]
for row in csv.DictReader((AUDIT/'task_intervals.csv').open()):
 time_intervals.append({'task_key':phase_keys[int(row['phase'][:2])],'start':float(row['start']),'end':float(row['end']),'basis':'frozen production audit'})
(P/'observed-task-intervals.json').write_text(json.dumps(time_intervals,separators=(',',':'))+'\n')
for t in T.values():t['activity_seconds']=sum(b-a for a,b in union(t.pop('intervals',[])))

# Daily account totals provide the control. Local counters are attribution weights,
# not additive account totals: fork histories/retries can otherwise inflate them.
ledger=[];grand=account['summary']['lifetimeTokens'];unassigned=0
for bucket in account['dailyUsageBuckets']:
 d=bucket['startDate'];account_total=bucket['tokens'];reserved=frozen_daily[d];total=account_total-sum(reserved.values());assert total>=0,(d,total)
 for k,n in reserved.items():T[k]['days'][d]={'tokens':n,'basis':'Frozen production-audit record'}
 weights=collections.Counter({k:sum(v for key,v in z.items() if key.endswith('::total_tokens')) for k,z in raw[d].items()})
 mode='Daily account total / session-weighted estimate'
 if not sum(weights.values()):
  # Before local session retention, use archived commit activity as an explicit weaker proxy.
  for t in T.values():
   cs=[c for c in t['commits'] if c['start']<=d<=c['end']]
   if cs and not t.get('frozen_audit_phase') and not t['key'].startswith('OLD'):weights[t['key']]=sum(max(1,c['original_count'])/(daynum(c['end'])-daynum(c['start'])+1)/len(links[c['sha']]) for c in cs)
  mode='Daily account total / commit-weighted estimate'
 if not weights:weights['UNASSIGNED']=1;mode='Unassigned account activity'
 denom=sum(weights.values());alloc={k:int(total*w/denom) for k,w in weights.items()};alloc[max(weights,key=weights.get)]+=total-sum(alloc.values())
 for k,n in alloc.items():
  if k not in T:unassigned+=n;continue
  t=T[k];t['days'][d]={'tokens':n,'basis':mode};t['start']=min(t['start'],d);t['end']=max(t['end'],d)
  z=raw[d].get(k);den=sum(v for key,v in (z or {}).items() if key.endswith('::total_tokens'))
  if den:
   for label in set(key.split('::')[0] for key in z):
    dst=t['models'].setdefault(label,collections.Counter())
    for f in keys:dst[f]+=z.get(label+'::'+f,0)*n/den
  else:
   # User-recalled families; release calendar constrains this estimate but does not prove usage.
   model=next(m for date,m in [('2026-09-03','gpt-6-astra'),('2026-07-09','gpt-5.6-sol'),('2026-04-23','gpt-5.5'),('2026-03-05','gpt-5.4'),('2026-02-05','gpt-5.3-codex'),('0001-01-01','gpt-5.2')] if d>=date)
   label=model+'|estimated'
   dst=t['models'].setdefault(label,collections.Counter());dst['total_tokens']+=n
 ledger.append({'date':d,'account_tokens':account_total,'allocation':dict(collections.Counter(alloc)+reserved),'basis':mode})
for k,models in frozen_models.items():T[k]['models']=dict(models)

# Estimate missing input/cache/output mix using observed primary coding-session usage.
observed=collections.Counter()
for t in T.values():
 for label,v in t['models'].items():
  if not label.endswith('|estimated'):
   observed.update(v)
ratio={f:observed[f]/observed['total_tokens'] for f in keys}
rates={'gpt-5.2':[1.75,.175,14,0],'gpt-5.4':[2.5,.25,15,0],'gpt-5.5':[5,.5,30,0],'gpt-5.3-codex':[1.75,.175,14,0],'gpt-5.6-sol':[4,.4,20,5],'gpt-5.6-terra':[2,.2,12,2.5],'gpt-6-astra':[10,1,50,12.5],'gpt-6-sol':[2,.2,10,2.5],'gpt-6-luna':[.1,.01,.5,.125]}
for t in T.values():
 t.pop('_words');t['sessions']=sorted(t['sessions']);t['tokens_estimate']=sum(d['tokens'] for d in t['days'].values());cost=0;unpriced=0
 for label,v in t['models'].items():
  model,eff=label.split('|',1)
  if eff=='estimated':
   for f in keys:
    if f!='total_tokens':v[f]=v['total_tokens']*ratio[f]
  if model in rates:
   a,b,c,w=rates[model];cache=min(v['input_tokens'],v['cached_input_tokens']);writes=min(max(0,v['input_tokens']-cache),v['cache_write_input_tokens'])
   cost+=(max(0,v['input_tokens']-cache-writes)*a+cache*b+writes*(w or a)+v['output_tokens']*c)/1e6
  else:unpriced+=v['total_tokens']
 t['api_standard_usd_estimate']=round(cost,2);t['unpriced_tokens']=round(unpriced);t['activity_hours_estimate']=round(t['activity_seconds']/3600,1)
 t['duration_basis']='Union of recorded root task intervals; includes tool/network waits, not human labor time'
 if not t['activity_hours_estimate'] and t['tokens_estimate']:
  # Empirical throughput proxy for periods with no retained session timings.
  known=sum(x['activity_seconds'] for x in T.values());rawtokens=sum(sum(v for k,v in z.items() if k.endswith('::total_tokens')) for daydata in raw.values() for z in daydata.values())
  t['activity_hours_estimate']=round(t['tokens_estimate']*known/max(1,rawtokens)/3600,1)
  t['duration_basis']='Estimated from observed token-to-model-activity ratio; not human labor time'
 t['token_basis']='Estimated task allocation of measured daily account totals'
 if t.get('frozen_audit_phase'):
  ph=t['frozen_audit_phase'];t['activity_hours_estimate']=round(ph['automatic_seconds']/3600,2);t['joint_hours_low']=round(ph['window15_seconds']/3600,2);t['joint_hours_high']=round(ph['window30_seconds']/3600,2);t['duration_basis']='Reused frozen production audit: union of recorded root task intervals';t['token_basis']='Reused frozen production audit, exact logged token ledger'
  assert t['tokens_estimate']==ph['total_tokens'],(t['key'],t['tokens_estimate'],ph['total_tokens'])
  t['start']=min(t['days']);t['end']=max(t['days'])
 if not t['commits']:
  assigned=[d for d,v in t['days'].items() if v['tokens']]
  if assigned:t['start']=min(assigned);t['end']=max(assigned)
 t['status']='Done' if t['commits'] else 'Recorded'
assert sum(t['tokens_estimate'] for t in T.values())+unassigned==grand
assert set(links)=={c['sha'] for r in repos for c in r['commits']}
ordered=sorted(T.values(),key=lambda t:(t['start'],t['end'],t['key']))
previous={t['key']:t['provisional_id'] for t in json.loads((P/'final-tasks.json').read_text())}
for t in ordered:
 k=t['key']
 t['project_scope']='myscoutee-old' if k.startswith('OLD') else 'e-kozig' if re.fullmatch(r'E\d+',k) else 'math' if k=='RESEARCHVIDEO' or k=='MCOMM' or re.fullmatch(r'M\d+',k) else 'myscoutee'
 t['provisional_id']=previous.get(k) or ('EKO-'+k[1:] if k.startswith('E') else 'MATH-'+('13' if k=='MCOMM' else '14' if k=='M15' else k[1:]) if k.startswith('M') else 'OLD-'+k[3:])
 if k=='OLD':t['provisional_id']='OLD-1'
 if k=='RESEARCHVIDEO':t['provisional_id']='MATH-12'
 if k=='M16':t['provisional_id']='MATH-15'
 if k=='M17':t['provisional_id']='MATH-16'
 if k.startswith('OLD'):
  t['activity_hours_estimate']=0;t['activity_seconds']=0;t['token_basis']='Primarily manual legacy work, confirmed by the creator; no attributable AI usage retained';t['duration_basis']='Unknown manual effort; commit spacing is not used as a time estimate';t['manual_time_unknown']=True

(P/'tasks.json').write_text(json.dumps(ordered,indent=2)+'\n');(P/'commit-task-links.json').write_text(json.dumps(links,indent=2)+'\n');(P/'daily-allocation.json').write_text(json.dumps(ledger,indent=2)+'\n');(P/'session-task-links.json').write_text(json.dumps(sidmap,indent=2)+'\n')
summary={'tasks':len(T),'commits':len(links),'account_tokens':grand,'allocated_tokens_estimate':grand-unassigned,'unassigned_tokens':unassigned,'api_standard_usd_estimate':round(sum(t['api_standard_usd_estimate'] for t in T.values()),2),'note':'Task allocation and USD are estimates. The account total is measured. USD uses 2026-10-01 Standard short-context API rates, not a subscription invoice.','observed_token_mix':ratio,'rates_per_million':rates,'pricing_source':'https://developers.openai.com/api/docs/pricing','model_calendar_source':'https://developers.openai.com/api/docs/changelog','frozen_production_audit_tokens':sum(sum(d.values()) for d in frozen_daily.values())}
(P/'allocation-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
for t in ordered:print(t['provisional_id'],t['key'],t['area'],t['start'],t['end'],round(t['tokens_estimate']/1e6,1),'M',t['title'])
