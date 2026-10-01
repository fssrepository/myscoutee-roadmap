from pathlib import Path
p=Path(__file__).parent/'build-tasks.py';s=p.read_text().replace('import json,pathlib,collections,datetime,re,math,bisect','import json,pathlib,collections,datetime,re,math,bisect,csv')
pos=s.index('# The dated tasks')
s=s[:pos]+'''AUDIT=Path('/home/USER/workspace/myscoutee-backend/guides/story/london/cinema_studio_steps/04_tracking/production_audit')
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
''' .replace('AUDIT=Path(', 'AUDIT=pathlib.Path(')+s[pos:]
s=s.replace('def choose(s,e):','choice_cache={}\ndef choose(s,e):')
s=s.replace(" mk=media_kind(text)"," cachekey=(root['id'],d,idx)\n if cachekey in choice_cache:return choice_cache[cachekey]\n mk=media_kind(text)")
s=s.replace(" return max(candidates)[1] if candidates else 'UNASSIGNED'", " result=max(candidates)[1] if candidates else 'UNASSIGNED';choice_cache[cachekey]=result;return result")
s=s.replace("  if mk=='FILM' and t['area']!='Creative':continue", "  if t.get('frozen_audit_phase'):continue\n  if mk=='FILM' and t['area']!='Creative':continue")
# Route unmatched post-audit creative work to a separate actual task rather than altering frozen metrics.
s=s.replace(" if mk and mk!='FILM':return mk", " if mk in ['BOOKS','NARRATION','REEL','FILM']:\n  return 'PROMO'\n if mk:return mk")
s=s.replace("  if d>'2026-09-30':continue", "  if d>'2026-09-30' or isfrozen(s['id'],e['timestamp']):continue")
start=s.index(' # Observed model-active time proxy');end=s.index('# Daily account totals',start)
s=s[:start]+''' # Same task-interval union method as the existing production audit.
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
for t in T.values():t['activity_seconds']=sum(b-a for a,b in union(t.pop('intervals',[])))

''' +s[end:]
s=s.replace(" d=bucket['startDate'];total=bucket['tokens'];weights=", " d=bucket['startDate'];account_total=bucket['tokens'];reserved=frozen_daily[d];total=account_total-sum(reserved.values());assert total>=0,(d,total)\n for k,n in reserved.items():T[k]['days'][d]={'tokens':n,'basis':'Frozen production-audit record'}\n weights=")
s=s.replace("   if cs:weights[t['key']]", "   if cs and not t.get('frozen_audit_phase'):weights[t['key']]")
s=s.replace("model='gpt-5.3-codex' if d<'2026-07-09' else 'gpt-5.6-sol'", "model=next(m for date,m in [('2026-09-03','gpt-6-astra'),('2026-07-09','gpt-5.6-sol'),('2026-04-23','gpt-5.5'),('2026-03-05','gpt-5.4'),('2026-02-05','gpt-5.3-codex'),('0001-01-01','gpt-5.2')] if d>=date)")
s=s.replace(" ledger.append({'date':d,'account_tokens':total,'allocation':alloc,'basis':mode})", " ledger.append({'date':d,'account_tokens':account_total,'allocation':dict(collections.Counter(alloc)+reserved),'basis':mode})\nfor k,models in frozen_models.items():T[k]['models']=dict(models)")
s=s.replace("rates={'gpt-5.3-codex'", "rates={'gpt-5.2':[1.75,.175,14,0],'gpt-5.4':[2.5,.25,15,0],'gpt-5.5':[5,.5,30,0],'gpt-5.3-codex'")
s=s.replace(" t['duration_basis']='Observed model-activity proxy (successive usage gaps capped at 15 minutes); includes parallel agent time'", " t['duration_basis']='Union of recorded root task intervals; includes tool/network waits, not human labor time'")
s=s.replace(" t['token_basis']='Estimated task allocation of measured daily account totals'", " t['token_basis']='Estimated task allocation of measured daily account totals'\n if t.get('frozen_audit_phase'):\n  ph=t['frozen_audit_phase'];t['activity_hours_estimate']=round(ph['automatic_seconds']/3600,2);t['joint_hours_low']=round(ph['window15_seconds']/3600,2);t['joint_hours_high']=round(ph['window30_seconds']/3600,2);t['duration_basis']='Reused frozen production audit: union of recorded root task intervals';t['token_basis']='Reused frozen production audit, exact logged token ledger'\n  assert t['tokens_estimate']==ph['total_tokens'],(t['key'],t['tokens_estimate'],ph['total_tokens'])\n  t['start']=min(t['days']);t['end']=max(t['days'])")
s=s.replace("'model_calendar_source':'https://developers.openai.com/api/docs/changelog'", "'model_calendar_source':'https://developers.openai.com/api/docs/changelog','frozen_production_audit_tokens':sum(sum(d.values()) for d in frozen_daily.values())")
p.write_text(s)
