import json,pathlib,hashlib,csv,io,gzip,collections,sys
P=pathlib.Path(__file__).parent;W=P.parent;C=W/'myscoutee-roadmap';D=C/'guides/project-history'
T=json.loads((P/'portfolio-tasks.json').read_text());S=json.loads((P/'portfolio-state.json').read_text());R=json.loads((P/'commits.json').read_text());maps=json.loads((P/'rewrite-map.json').read_text());links=json.loads((P/'commit-task-links.json').read_text());summary=json.loads((P/'prepared-summary.json').read_text());totals=json.loads((P/'portfolio-summary.json').read_text());by={t['key']:t for t in T}
restore=(D/'restore_project.py').read_text() if (D/'restore_project.py').exists() else (D/'myscoutee/restore_project.py').read_text()
restore=restore.replace('stable MSC IDs','stable task IDs').replace("statepath=args.state or pathlib.Path.home()/'.local/state/myscoutee-project-restore/state.json'", "statepath=args.state or pathlib.Path.home()/'.local/state/project-history-restore'/(hashlib.sha256(args.snapshot.read_bytes()).hexdigest()[:16]+'.json')")
views=[{'name':'Delivery history','layout':'TABLE_LAYOUT','visibleFields':['Task ID','Title','Workstream','Status','Started','Finished','Evidence']},{'name':'AI usage and effort','layout':'TABLE_LAYOUT','visibleFields':['Task ID','Title','Tokens M','API equiv USD','Active h','Allocated h','Models','Reasoning','Evidence']}]
def write(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def remote_name(name):return 'myscoutee' if name.endswith('/frontend') else name
commitrows=[]
for r in R:
 for c in r['commits']:
  commitrows.append({'repository':remote_name(r['path']),'original_commit':c['sha'],'task_commit':maps[r['path']][c['sha']],'task_ids':[by[k]['provisional_id'] for k in links[c['sha']]],'original_source_tree':c['tree'],'original_execution_start':c['original_start'],'original_execution_end':c['original_end'],'original_commit_count':len(c['original_commits'])})
method=(P/'public/README.md').read_text().split('## Measurement method')[1].split('## Task identifiers')[0]
method=method.replace('Missing timing is estimated from comparable observed work.','Missing AI timing is estimated from comparable observed work. Manual legacy work has no time estimate; archive dates do not establish its original development period.')
method+='\n- Four independent Projects separate MyScoutee, the manually developed legacy archive, e-kozig and mathematical research. Shared account tokens are allocated once across all four; a Project total is never an additional account total. Historical legacy AI usage is unverified and left blank. The current AI-assisted Project-administration task is measured separately. A final shared maintenance-run measurement is apportioned by snapshot ownership; its overlap with MSC-108 is removed and its net allocation uses the unassigned account allowance, without exact daily billing reconciliation.\n- Mathematical experiments and videos do not establish a solution of the continuous Navier–Stokes problem. The claim withdrawal is a first-class task.\n'
index='# Delivery history and project backups\n\nFour separate Projects preserve distinct work. MyScoutee system repositories share one Project; the legacy archive, e-kozig and math each have their own.\n\n| Project | Tasks | Tokens (M), estimated | Allocated activity (h) | API equivalent (USD), estimated |\n| --- | ---: | ---: | ---: | ---: |\n'
for scope,v in totals.items():
 pr=S['projects'][scope]['project'];h=f"{v['allocated_hours_estimate']:.1f}"+(' AI; manual unknown' if v['manual_effort_unknown'] else '');tokens=f"{v['tokens_estimate']/1e6:,.1f}";cost=f"${v['api_standard_usd_estimate']:,.0f}"
 index+=f"| [{pr['title']}]({pr['url']}) | {v['tasks']} | {tokens} | {h} | {cost} |\n"
index+=f"\nAccount-wide measured tokens: **{summary['account_tokens']:,}**, through September 30, 2026. Estimated allocation across listed AI work: **{summary['allocated_tokens_estimate']:,}**; remaining unassigned: **{summary['unassigned_tokens']:,}**. Activity time includes tool/network waits; it is not human labor time. Legacy manual effort is unknown and excluded from numeric totals. USD is a standardized API list-price comparison, not a subscription invoice or amount paid.\n\n"
index+=f'11 source repositories, 226 consolidated source commits, and {len(T)} retrospective tasks. The task issue records share this public tracker for stable references, while their Project boards and totals are separate. Source repository visibility is unchanged.\n\n'
index+='## Restore from Git\n\n'
for scope in totals:index+=f"- [{scope} backup](guides/project-history/{scope}/README.md)\n"
index+='\nEach source repository also has a `guides/project-history/` snapshot. Complete per-Project snapshots here and compact repository-specific copies preserve issue bodies, fields, values, view definitions, token/model/time ledgers, attribution assumptions and commit mappings. No chat history is needed. Git records versions; no date-named folder is used.\n\n## Measurement method\n'+method
index+='\n## Reconstruction tools\n\nThe [history helper archive](guides/history-tools/README.md) preserves the source scripts and workflow notes used for the reconstruction. It excludes backup bundles, credentials and private conversation extracts.\n'
index+='\n## Task identifiers\n\nMSC, OLD, EKO and MATH IDs are stable task identifiers. Commit bodies link their actual issue numbers; task ID numbers need not equal GitHub issue numbers. Mixed commits retain their contents and can refer to several tasks. Release/archive tags retain their original targets.\n'
(C/'README.md').write_text(index)
(D/'README.md').write_text(index.replace('(guides/project-history/','(').replace('(guides/history-tools/','(../history-tools/'))
write(D/'portfolio-summary.json',totals);write(D/'account-daily-usage.json',json.loads((P/'account-usage.json').read_text()));write(D/'allocation-summary.json',summary)
write(D/'daily-allocation.json',[{**row,'allocation':{by[k]['provisional_id'] if k in by else k:n for k,n in row['allocation'].items()}} for row in json.loads((P/'daily-allocation.json').read_text())])
write(D/'analogy-allocations.json',[{'task_id':t['provisional_id'],'tokens':t['tokens_estimate'],'basis':t['token_basis']} for t in T if t['token_basis'].startswith('Analogy')])
write(D/'views.json',views)
if (P/'maintenance-measurement.json').exists():write(D/'maintenance-measurement.json',json.loads((P/'maintenance-measurement.json').read_text()))
if (P/'documentation-measurement.json').exists():write(D/'documentation-measurement.json',json.loads((P/'documentation-measurement.json').read_text()))
folders=[];project_defs={}
source_scopes=set(sys.argv[1:]) if len(sys.argv)>1 else set(totals)
def backup(folder,scope,selected,subset_name=None):
 folder.mkdir(parents=True,exist_ok=True);ids={t['provisional_id'] for t in selected};pr=S['projects'][scope];counts=totals[scope];full=subset_name is None
 fs=[]
 for name in ['Title','Status','Task ID','Workstream','Started','Finished','Tokens M','API equiv USD','Active h','Allocated h','Models','Reasoning','Evidence']:
  f=pr['fields'][name];fs.append({'name':name,'dataType':f.get('dataType','SINGLE_SELECT'),'options':[{'name':o['name'],'color':o.get('color','GRAY'),'description':o.get('description','')} for o in f.get('options',[])]})
 body=f"# {pr['project']['title']}\n\n{counts['tasks']} retrospective tasks. This Project is separate from the other portfolio Projects.\n\n[Complete Git backup](https://github.com/fssrepository/myscoutee-roadmap/tree/master/guides/project-history/{scope}) · [Measurement method](https://github.com/fssrepository/myscoutee-roadmap#measurement-method)\n\n"
 if scope=='myscoutee-old':body+='Primarily manual legacy development. Original working time is unknown; import dates are archival evidence. AI assistance with GitHub may have occurred, but unsupported tokens, models, costs and time remain blank.\n'
 else:body+=f"Estimated task allocation: {counts['tokens_estimate']/1e9:.3f} B tokens, {counts['allocated_hours_estimate']:.1f} h of activity after removing observed overlap, approximately ${counts['api_standard_usd_estimate']:,.0f} at Standard API rates. These are estimates, not human hours or an invoice.\n"
 body+='\n## Budget by workstream\n\n| Workstream | Tokens (M) | Allocated activity (h) | API equivalent (USD) |\n| --- | ---: | ---: | ---: |\n'
 for area,a in counts.get('workstreams',{}).items():
  body+=f"| {area} | {a['tokens']/1e6:,.2f} | {a['hours']:.2f} | ${a['api_equivalent_usd']:,.2f} |\n" if area!='Legacy manual' else '| Legacy manual | Unknown | Unknown | Unknown |\n'
 if scope=='math':body+='\nNumerical and finite-model experiments are research artifacts, not a solution of the continuous Millennium problem. The withdrawal of normalization claims is preserved as MATH-14.\n'
 body+='\n## Repositories\n\n'+'\n'.join('- ['+r.split('/')[1]+'](https://github.com/'+r+')' for r in pr.get('repositories',[]))+'\n'
 project={'repositories':pr.get('repositories',[]),'owner':'fssrepository','title':pr['project']['title'],'url':pr['project']['url'],'public':True,'shortDescription':f"{counts['tasks']} tasks · {counts['tokens_estimate']/1e6:,.1f}M tokens · {counts['allocated_hours_estimate']:.1f}h AI activity · API equivalent ${counts['api_standard_usd_estimate']:,.0f} (estimates)"+(' · legacy manual effort unknown' if scope=='myscoutee-old' else '')+(' · Navier–Stokes research' if scope=='math' else ''),'readme':body};project_defs[scope]=project
 items=[];metrics=[];rows=[]
 for t in selected:
  issue=S['issues'][t['key']];manual=t.get('manual_time_unknown');items.append({'task_id':t['provisional_id'],'title':t['provisional_id']+': '+t['title'],'body':t['issue_body'],'state':'CLOSED','state_reason':'completed','issue':{'repository':S['repo']['name'],'number':issue['number'],'url':issue['url'],'node_id':issue['id']},'values':{**t['project_fields'],'Status':'Done'}})
  metrics.append({'task_id':t['provisional_id'],'tokens':None if manual else t['tokens_estimate'],'api_standard_usd_estimate':None if manual else t['api_standard_usd_estimate'],'active_hours':None if manual else t['activity_hours_estimate'],'allocated_hours':None if manual else t['allocated_hours'],'manual_effort_unknown':bool(manual),'token_basis':t['token_basis'],'duration_basis':t['duration_basis'],'allocated_time_basis':t['allocated_time_basis'],'models':t['models'],'repository_allocations':{} if manual else t['repository_allocations'],**({'frozen_phase':t['frozen_audit_phase']} if t.get('frozen_audit_phase') else {})})
  rows.append({'task_id':t['provisional_id'],'title':t['title'],'workstream':t['area'],'started':t['start'],'finished':t['end'],'tokens_million':None if manual else round(t['tokens_estimate']/1e6,2),'api_equivalent_usd_estimate':None if manual else t['api_standard_usd_estimate'],'active_hours':None if manual else t['activity_hours_estimate'],'allocated_hours':None if manual else round(t['allocated_hours'],2),'models':None if manual else t['model_display'],'reasoning':None if manual else t['effort_display'],'evidence':t['token_basis']})
 write(folder/'project.json',{'schema_version':1,'scope':'complete-project' if full else subset_name,'project':project,'fields':fs,'views':views,'items':items})
 write(folder/'measurements.json',{'schema_version':1,'project_totals':counts,'account_control':{k:summary[k] for k in ['account_tokens','allocated_tokens_estimate','unassigned_tokens']},'valuation_date':'2026-10-01','rates_per_million':summary['rates_per_million'],'pricing_source':summary['pricing_source'],'observed_token_mix':summary['observed_token_mix'],'tasks':metrics,'maintenance_run':json.loads((P/'maintenance-measurement.json').read_text()) if (P/'maintenance-measurement.json').exists() else None})
 write(folder/'commit-map.json',[r for r in commitrows if (full and ids.intersection(r['task_ids'])) or (not full and r['repository']==subset_name)])
 write(folder/'tasks.json',rows);f=io.StringIO();w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows);(folder/'tasks.csv').write_text(f.getvalue())
 (folder/'restore_project.py').write_text(restore)
 ints=[{'task_id':by[r['task_key']]['provisional_id'],'start_utc_epoch':r['start'],'end_utc_epoch':r['end'],'basis':r['basis'],**({'allocation_share':r['allocation_share']} if 'allocation_share' in r else {})} for r in json.loads((P/'observed-task-intervals.json').read_text()) if by[r['task_key']]['provisional_id'] in ids]
 (folder/'observed-task-intervals.json.gz').write_bytes(gzip.compress(json.dumps(ints,separators=(',',':')).encode(),mtime=0))
 (folder/'METHOD.md').write_text('# Measurement method\n'+method)
 scope_text='Complete Project' if full else 'Repository subset: '+subset_name
 (folder/'README.md').write_text(f'''# Restorable Project history\n\n{scope_text}; {len(selected)} tasks. [Live Project]({project['url']}) · [Canonical complete backup](https://github.com/fssrepository/myscoutee-roadmap/tree/master/guides/project-history/{scope}).\n\n`project.json` preserves full issue bodies, statuses, typed field values and views. `measurements.json` preserves model/token/cost/time components and assumptions. `commit-map.json` links original and task-prefixed commit IDs. CSV/JSON provide convenient presentation exports. Recorded root intervals are retained in compressed JSON for timing reconstruction; there are no private chat texts.\n\n## Validate offline\n\nRun from the repository root:\n\n```bash\npython3 {folder.relative_to(C) if folder.is_relative_to(C) else 'guides/project-history'}/restore_project.py\n```\n\nThis validates all SHA256SUMS files and snapshot structure without network access.\n\n## Recreate a deleted Project\n\nSet `GITHUB_PROJECT_TOKEN` in your local shell to a credential with Projects write access. Run the same command with `--apply`. The script creates a new Project and restores task associations, fields, values, statuses and visible-column views; existing issues and source commits are preserved. Local progress is saved for retries. Use a separate `--state` file to create another copy. A repository subset restores only the tasks in that subset; use the complete backup to restore the whole Project.\n\nIf issues were deleted too, set `GITHUB_REPOSITORY_TOKEN` to an issue-write credential and add `--recreate-missing-issues`. The tracker repository must exist. Recreated issues may receive new issue numbers; stable task IDs remain. Historical execution dates remain in fields, while GitHub creation/closure timestamps reflect restoration.\n\nRepository associations are included in `project.json`. Set `GITHUB_REPOSITORY_TOKEN` (or a suitable `GITHUB_TOKEN`) during restoration to reconnect them automatically. Separate Project-write and repository credentials are supported. Comments, automations and permission grants are outside this reconstruction. Read [METHOD.md](METHOD.md) for estimates, unknown values and measurement boundaries. Git versions these files; no dated folder is needed.\n''')
 folders.append(folder)
for scope in totals:backup(D/scope,scope,[t for t in T if t['project_scope']==scope])
for r in R:
 scope='myscoutee-old' if r['path']=='myscoutee-old' else 'e-kozig' if r['path']=='e-kozig' else 'math' if r['path']=='millennium-math-problems' else 'myscoutee'
 if scope not in source_scopes:continue
 selected=[t for t in T if t['project_scope']==scope and (scope!='myscoutee' or any(c['repo']==r['path'] for c in t['commits']) or t['key']=='MAINT' or (r['path']=='myscoutee-backend' and not t['commits']))]
 backup(W/r['path']/'guides/project-history',scope,selected,None if scope!='myscoutee' else remote_name(r['path']))
for folder in folders:
 (folder/'SHA256SUMS').write_text('\n'.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name for f in sorted(folder.iterdir()) if f.is_file() and f.name!='SHA256SUMS')+'\n')
# Public per-project summaries use the same ledger as the Project backups.
for scope,repo in {'e-kozig':'e-kozig','myscoutee-old':'myscoutee-old','math':'millennium-math-problems'}.items():
 if scope not in source_scopes:continue
 v=totals[scope];pr=S['projects'][scope]['project'];p=W/repo/'README.md'
 marker='<!-- project-effort-summary -->';s=p.read_text().split(marker)[0].rstrip()
 table=f'''\n\n{marker}

---

## Project effort and delivery

[View tasks and AI usage]({pr['url']}) · [Restorable records and methodology](guides/project-history/README.md)

| Measure | This project |
| --- | ---: |
| Completed tasks | {v['tasks']} |
| AI tokens, including cached input | {v['tokens_estimate']/1e6:,.2f} M |
| Allocated AI activity | {v['allocated_hours_estimate']:.2f} h |
| Standard API list-price equivalent | ${v['api_standard_usd_estimate']:,.2f} USD |
'''
 if scope=='myscoutee-old':table+='| Original manual development time | Unknown |\n'
 table+='\nThese are retrospective estimates, combining recorded session usage with\nlabeled task allocations. Activity includes tool and network waits; it is not\nhuman working time. The USD figure is an API-price comparison, not actual\nspending or a subscription invoice. Each project has its own allocation;\nshared work is split rather than counted in full more than once.\n'
 if scope=='myscoutee-old':table+='\nThe numeric AI figures cover the recent archive and documentation work. They\ndo not measure the original manual development or convert the recalled\nresearch and refactoring phases into hours.\n'
 p.write_text(s+table)
for name in ['tasks.csv','tasks.json','account-daily-usage.json']:
 (C/name).unlink(missing_ok=True)
(D/'restore_project.py').unlink(missing_ok=True)
write(P/'portfolio-project-definitions.json',project_defs);write(P/'portfolio-backup-folders.json',[str(f) for f in folders]);print('Wrote',len(folders),'snapshots (selected source scopes and canonical portfolio)',flush=True)
