import json, pathlib, collections, datetime
from github_api import graphql, request
P=pathlib.Path(__file__).parent
def read(n): return json.loads((P/n).read_text())
def write(n,v): (P/n).write_text(json.dumps(v,indent=2)+'\n')
T=read('portfolio-tasks.json'); S=read('portfolio-state.json'); summary=read('prepared-summary.json')
assert not any(t['key']=='EKODOCS' for t in T), 'Documentation already recorded'
u=read('maintenance-session-usage.json')[0]
start=1790811264.557; end=max(e['timestamp'] for e in u['events'])
events=[e for e in u['events'] if start<=e['timestamp']<=end]
keys=['input_tokens','cached_input_tokens','cache_write_input_tokens','output_tokens','reasoning_output_tokens','total_tokens']
models=collections.defaultdict(collections.Counter)
for e in events:
 for k in keys: models[(e.get('model') or 'unknown')+'|'+(e.get('effort') or 'unknown')][k]+=e.get(k,0)
tokens=sum(m['total_tokens'] for m in models.values()); hours=(end-start)/3600
iso=lambda s: datetime.datetime.fromtimestamp(s,datetime.timezone.utc).isoformat()
specs=[('e-kozig','EKODOCS','EKO-16','e-kozig',.6,'Publish a clear English introduction and process diagram','Structure the English README, retain the Hungarian introduction and original assets, translate the editable process diagram, correct its SVG text positioning, capitalize the Project name, and publish a project-specific effort summary.'),('myscoutee-old','OLDDOCS','MSC-OLD-6','myscoutee-old',.3,'Document the original project and its evolution into MyScoutee','Expand the README with the creator-reported 2016 origin, approximately 1.5 years of research/development and a later half-year refactor. Explain the recalled backend clone and subsequent AI-assisted rewrite, preserve uncertainty about the lost standalone backend, and display project-specific metrics without inventing historical human hours.'),('math','MATHDOCS','MATH-18','millennium-math-problems',.1,'Publish the project effort summary in the repository README','Add a project-specific task, token, activity and API-equivalent summary to the README, linked to the existing Project and restorable measurement records. Preserve the existing research-status qualifications.')]
assigned=0; intervals=read('observed-task-intervals.json')
for idx,(scope,key,tid,repo,share,title,description) in enumerate(specs):
 n=round(tokens*share) if idx<2 else tokens-assigned; assigned+=n
 mm={label:{k:v*share for k,v in m.items()} for label,m in models.items()}; cost=0
 for label,v in mm.items():
  a,c,o,w=summary['rates_per_million'][label.split('|')[0]]; cached=min(v['input_tokens'],v['cached_input_tokens']); writes=min(v['input_tokens']-cached,v['cache_write_input_tokens'])
  cost+=(max(0,v['input_tokens']-cached-writes)*a+cached*c+writes*(w or a)+v['output_tokens']*o)/1e6
 cost=round(cost,2); h=hours*share
 basis='Measured shared documentation-session tokens; estimated allocation 60% E-Kozig, 30% MyScoutee Old, 10% math'
 duration='Observed active session window, including tool waits; estimated project split, not human labor'
 body=f'''{description}

| Metric | Value |
| --- | ---: |
| Allocated tokens | {n/1e6:.3f} M |
| Allocated activity | {h:.3f} h |
| Standard API equivalent | ${cost:.2f} USD |
| Model / reasoning | gpt-6-astra / high |

The shared documentation window recorded {tokens:,} tokens from {iso(start)} to {iso(end)}. Its effort is split once across EKO-16 (60%), MSC-OLD-6 (30%) and MATH-18 (10%); these are estimated shares of one measured session, not independent measurements. The bounded cutoff excludes the final publishing/accounting tail. Token components, model and reasoning come from the local session records. The allocation reserves part of the portfolio's previously unassigned allowance, without claiming exact reconciliation to the earlier account-wide daily snapshot. API equivalent is a list-price comparison, not an invoice or credits paid.

Validation: documentation links, original Hungarian asset preservation, SVG text positions and PNG preview, and offline restore/checksum checks. No application behavior changed.

Project: {S['projects'][scope]['project']['url']}
'''
 t=dict(key=key,provisional_id=tid,project_scope=scope,title=title,area='Documentation (AI-assisted)',commits=[],start='2026-10-01',end='2026-10-01',days={},models=mm,tokens_estimate=n,api_standard_usd_estimate=cost,activity_hours_estimate=h,allocated_hours=h,allocated_time_basis=duration,token_basis=basis,duration_basis=duration,model_display='gpt-6-astra',effort_display='high',repository_allocations={repo:dict(hours=h,tokens=n,api_equivalent_usd=cost)},status='Done',issue_body=body,frozen_audit_phase={'start_utc':iso(start),'cutoff_utc':iso(end),'shared_tokens':tokens,'shared_hours':hours,'allocation_share':share})
 t['project_fields']={'Task ID':tid,'Workstream':t['area'],'Started':t['start'],'Finished':t['end'],'Tokens M':round(n/1e6,3),'API equiv USD':cost,'Active h':round(h,3),'Allocated h':round(h,3),'Models':'gpt-6-astra','Reasoning':'high','Evidence':'Measured session; estimated project split'}
 T.append(t); intervals.append(dict(task_key=key,start=start,end=end,basis=duration,allocation_share=share))
summary['tasks']=len(T); summary['allocated_tokens_estimate']+=tokens; summary['unassigned_tokens']-=tokens;summary['api_standard_usd_estimate']=round(sum(t['api_standard_usd_estimate'] for t in T),2)
assert sum(t['tokens_estimate'] for t in T)+summary['unassigned_tokens']==summary['account_tokens']
totals={}
for scope in S['projects']:
 subset=[t for t in T if t['project_scope']==scope]; areas={}
 for t in subset:
  a=areas.setdefault(t['area'],dict(tokens=0,api_equivalent_usd=0,hours=0));a['tokens']+=t['tokens_estimate'];a['api_equivalent_usd']+=t['api_standard_usd_estimate'];a['hours']+=t['allocated_hours']
 totals[scope]=dict(tasks=len(subset),tokens_estimate=sum(t['tokens_estimate'] for t in subset),api_standard_usd_estimate=round(sum(t['api_standard_usd_estimate'] for t in subset),2),allocated_hours_estimate=sum(t['allocated_hours'] for t in subset),manual_effort_unknown=scope=='myscoutee-old',workstreams=areas)
S['projects']['e-kozig']['project']['title']='E-Kozig'
for n,v in [('portfolio-tasks.json',T),('prepared-tasks.json',T),('portfolio-state.json',S),('portfolio-summary.json',totals),('prepared-summary.json',summary),('observed-task-intervals.json',intervals)]:write(n,v)
write('documentation-measurement.json',dict(start_utc=iso(start),cutoff_utc=iso(end),tokens=tokens,hours=hours,models=models,shares={s[0]:s[4] for s in specs}))
request('repos/fssrepository/e-kozig',{'description':'Public UI prototype for Hungarian public administration and tax services: documents, appointments, tax deadlines and delegated access.','homepage':'https://fssrepository.github.io/e-kozig/'},method='PATCH')
print('Recorded three documentation tasks:',tokens,'shared tokens;',round(hours,3),'hours')
