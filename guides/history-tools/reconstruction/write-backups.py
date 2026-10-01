import json,pathlib,hashlib,shutil,csv,io,gzip
from github_api import P
W=pathlib.Path('/home/USER/workspace');state=json.loads((P/'publish-state.json').read_text());tasks=json.loads((P/'final-tasks.json').read_text());repos=json.loads((P/'commits.json').read_text());maps=json.loads((P/'rewrite-map.json').read_text());links=json.loads((P/'commit-task-links.json').read_text());summary=json.loads((P/'prepared-summary.json').read_text());times=json.loads((P/'time-summary.json').read_text());views=json.loads((P/'project-view-definitions.json').read_text());key_to_id={t['key']:t['provisional_id'] for t in tasks}
views[1]['visibleFields'].insert(5,'Allocated h')
central=W/'myscoutee-roadmap';dest=central/'guides/project-history';dest.mkdir(parents=True,exist_ok=True)
readme=(P/'public/README.md').read_text().replace('PROJECT_URL',state['project']['url']).replace('(tasks.csv)','(guides/project-history/tasks.csv)').replace('(tasks.json)','(guides/project-history/tasks.json)')
readme+='''\n## Time by repository\n\nTask-level active hours and the overlap-adjusted allocation are both retained. The system total combines **%.1f observed hours without overlap** and **%.1f estimated hours**, approximately **%.0f hours** altogether. This is task activity, including active tool/network waits, not human working time. Unlogged overlap cannot be measured. Cross-repository work is split by original commit counts as a presentation estimate.\n\n| Repository / scope | Allocated hours | Tokens (M) | API equivalent (USD) |\n| --- | ---: | ---: | ---: |\n'''%(times['observed_nonoverlapping_hours'],times['additional_estimated_hours'],times['total_allocated_hours_estimate'])
for name,v in times['repositories'].items():readme+=f"| {name} | {v['hours']:.1f} | {v['tokens']/1e6:,.1f} | ${v['api_equivalent_usd']:,.0f} |\n"
readme+='\nThe backend share includes creative artifacts stored there. Workstreams remain separate in the Project and measurement export.\n\n## Restore without the chat history\n\nThe complete [Git backup](guides/project-history/README.md) contains issue bodies, fields, statuses, views, model/token/time ledgers, rate assumptions and commit mappings, with checksums and a standalone restore script. Repository-specific subsets are committed under the same `guides/project-history/` path in each source repository. Git records versions; no date-named directory is required.\n'
(central/'README.md').write_text(readme)
project_readme=readme.replace('(guides/project-history/','(https://github.com/fssrepository/myscoutee-roadmap/blob/master/guides/project-history/')
fields=[]
for name in ['Title','Status','Task ID','Workstream','Started','Finished','Tokens M','API equiv USD','Active h','Allocated h','Models','Reasoning','Evidence']:
 f=state['fields'][name];fields.append({'name':name,'dataType':f.get('dataType','SINGLE_SELECT'),'options':[{'name':o['name'],'color':o.get('color','GRAY'),'description':o.get('description','')} for o in f.get('options',[])]})
items=[]
for t in tasks:
 issue=state['issues'][t['key']]
 items.append({'task_id':t['provisional_id'],'title':t['provisional_id']+': '+t['title'],'body':t['issue_body'],'state':'CLOSED','state_reason':'completed','issue':{'repository':state['repo']['name'],'number':issue['number'],'url':issue['url'],'node_id':issue['id']},'values':{**t['project_fields'],'Status':'Done'}})
project={'owner':'fssrepository','title':'MyScoutee delivery history','url':state['project']['url'],'public':True,'shortDescription':'Delivered work across MyScoutee: historical dates, models, tokens, activity time and clearly labeled cost estimates.','readme':project_readme}
commitrows=[]
for r in repos:
 for c in r['commits']:
  commitrows.append({'repository':'myscoutee' if r['path'].endswith('/frontend') else r['path'],'original_commit':c['sha'],'task_commit':maps[r['path']][c['sha']],'task_ids':[key_to_id[k] for k in links[c['sha']]],'original_source_tree':c['tree'],'original_execution_start':c['original_start'],'original_execution_end':c['original_end'],'original_commit_count':len(c['original_commits'])})
metrics=[]
for t in tasks:
 metrics.append({'task_id':t['provisional_id'],'workstream':t['area'],'tokens':t['tokens_estimate'],'api_standard_usd_estimate':t['api_standard_usd_estimate'],'active_hours':t['activity_hours_estimate'],'allocated_hours':t['allocated_hours'],'token_basis':t['token_basis'],'duration_basis':t['duration_basis'],'allocated_time_basis':t['allocated_time_basis'],'models':t['models'],'repository_allocations':t['repository_allocations'],**({'frozen_phase':t['frozen_audit_phase']} if t.get('frozen_audit_phase') else {})})
restore=(dest/'restore_project.py').read_text()
def write(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def backup(folder,selected,scope):
 folder.mkdir(parents=True,exist_ok=True);ids={t['provisional_id'] for t in selected}
 write(folder/'project.json',{'schema_version':1,'scope':scope,'project':project,'fields':fields,'views':views,'items':[i for i in items if i['task_id'] in ids]})
 write(folder/'measurements.json',{'schema_version':1,'scope':scope,'account_control':{'lifetime_tokens':summary['account_tokens'],'allocated_tokens_estimate':summary['allocated_tokens_estimate'],'unassigned_tokens':summary['unassigned_tokens']},'valuation_date':'2026-10-01','rates_per_million':summary['rates_per_million'],'pricing_source':summary['pricing_source'],'time_summary':times,'tasks':[m for m in metrics if m['task_id'] in ids]})
 write(folder/'commit-map.json',[r for r in commitrows if scope=='complete-project' or r['repository']==scope])
 (folder/'restore_project.py').write_text(restore)
 rows=[{'task_id':t['provisional_id'],'title':t['title'],'workstream':t['area'],'started':t['start'],'finished':t['end'],'tokens_million':round(t['tokens_estimate']/1e6,2),'api_equivalent_usd_estimate':round(t['api_standard_usd_estimate']),'active_hours':t['activity_hours_estimate'],'allocated_hours':round(t['allocated_hours'],2),'models':t['model_display'],'reasoning':t['effort_display'],'evidence':t['token_basis']} for t in selected]
 write(folder/'tasks.json',rows);f=io.StringIO();w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows);(folder/'tasks.csv').write_text(f.getvalue())
 text=f'''# Restorable project history\n\nScope: **{scope}**. This version preserves **{len(selected)} tasks**. The [complete Project](https://github.com/fssrepository/myscoutee-roadmap/tree/master/guides/project-history) is the canonical full backup. No chat-history files or credentials are needed to read these results or restore the Project.\n\n- `project.json`: full task descriptions, issue references, status, typed field values, historical dates and view definitions.\n- `measurements.json`: saved model/token components, timing, allocation assumptions and rates.\n- `commit-map.json`: previous and task-prefixed commit IDs and task relationships. Mixed commits remain intact.\n- `tasks.csv` / `tasks.json`: convenient presentation exports.\n- `restore_project.py`: dependency-free GitHub restoration tool.\n- `SHA256SUMS`: integrity checks for this snapshot.\n\n## Validate offline\n\n```bash\npython3 guides/project-history/restore_project.py\n```\n\nThis default mode validates the snapshot and makes no network requests.\n\n## Recreate a deleted Project\n\nSet `GITHUB_PROJECT_TOKEN` in your local shell to a token with Projects write access, then run:\n\n```bash\npython3 guides/project-history/restore_project.py --apply\n```\n\nThe script creates a new Project and restores its fields, task associations, values, statuses and visible-column views. Existing issues and Git commits are preserved. Progress is saved locally so an interrupted restore can resume. To start a separate restore, supply a different `--state` path.\n\nIf issues were deleted too, set `GITHUB_REPOSITORY_TOKEN` to a credential allowed to create issues in the tracker repository and add `--recreate-missing-issues`. The repository must exist. Recreated issues can receive new GitHub numbers; the stable MSC task ID is retained. The snapshot preserves historical execution dates, but GitHub creation/closure timestamps will reflect the restore. Native repository-to-Project sidebar links require combined repository/Projects permissions and can be added separately; they are not required to restore the task data.\n\nThe backup does not include comments, project automations, permissions/grants or private source code. None were part of this reconstructed record. The Git history versions these files; a timestamped folder is unnecessary.\n'''
 (folder/'README.md').write_text(text)
backup(dest,tasks,'complete-project')
shutil.copy2(P/'account-usage.json',dest/'account-daily-usage.json');shutil.copy2(P/'prepared-summary.json',dest/'allocation-summary.json')
intervals=json.loads((P/'observed-task-intervals.json').read_text());publicints=[{**r,'task_id':key_to_id[r['task_key']]} for r in intervals]
for r in publicints:r.pop('task_key')
(dest/'observed-task-intervals.json.gz').write_bytes(gzip.compress(json.dumps(publicints,separators=(',',':')).encode(),mtime=0))
folders=[dest]
for r in repos:
 name='myscoutee' if r['path'].endswith('/frontend') else r['path'];selected=[t for t in tasks if any(c['repo']==r['path'] for c in t['commits']) or (r['path']=='myscoutee-backend' and not t['commits'])]
 folder=W/r['path']/'guides/project-history';assert not folder.exists(),str(folder);backup(folder,selected,name);folders.append(folder)
for folder in folders:
 sums=[]
 for f in sorted(folder.iterdir()):
  if f.is_file() and f.name!='SHA256SUMS':sums.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name)
 (folder/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
# Move initial presentation exports into the requested guides location.
for name in ['tasks.csv','tasks.json','account-daily-usage.json']:
 f=central/name
 if f.exists():f.unlink()
(P/'final-project-readme.txt').write_text(project_readme);(P/'final-view-definitions.json').write_text(json.dumps(views,indent=2)+'\n')
print('Wrote',len(folders),'Git-backed snapshots,',len(tasks),'tasks; all source-repository subsets cover',len(set(i['task_id'] for f in folders[1:] for i in json.loads((f/'project.json').read_text())['items'])),'distinct tasks')
