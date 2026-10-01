import json,pathlib,csv,io,statistics,collections,datetime
P=pathlib.Path(__file__).parent;tasks=json.loads((P/'tasks.json').read_text());summary=json.loads((P/'allocation-summary.json').read_text());out=P/'public';out.mkdir(exist_ok=True)
# Missing isolated usage gets a conservative comparable-task estimate from the unassigned account balance.
ratio=summary['observed_token_mix'];rates=summary['rates_per_million'];inferred=0
for t in tasks:
 if t['tokens_estimate'] or t.get('manual_time_unknown'):continue
 peers=[x for x in tasks if x['area']==t['area'] and x['tokens_estimate'] and not x.get('frozen_audit_phase')]
 if not peers:continue
 percommit=statistics.median(x['tokens_estimate']/max(1,sum(c['original_count'] for c in x['commits'])) for x in peers)
 n=int(min(20000000,max(250000,percommit*sum(c['original_count'] for c in t['commits']))));t['tokens_estimate']=n;inferred+=n
 d=t['end'];model=next(m for date,m in [('2026-09-03','gpt-6-astra'),('2026-07-09','gpt-5.6-sol'),('2026-04-23','gpt-5.5'),('2026-03-05','gpt-5.4'),('2026-02-05','gpt-5.3-codex'),('0001-01-01','gpt-5.2')] if d>=date)
 v={k:n*r for k,r in ratio.items()};t['models']={model+'|estimated':v};a,b,c,w=rates[model];t['api_standard_usd_estimate']=round(((v['input_tokens']-v['cached_input_tokens'])*a+v['cached_input_tokens']*b+v['output_tokens']*c)/1e6,2)
 t['token_basis']='Analogy estimate from comparable tasks; reserved from unassigned account balance, daily attribution unavailable'
 t['activity_hours_estimate']=round(n*statistics.median(x['activity_hours_estimate']/x['tokens_estimate'] for x in peers),1)
 t['duration_basis']='Comparable-task estimate; historical timing not individually logged'
summary['analogy_tokens']=inferred;summary['allocated_tokens_estimate']+=inferred;summary['unassigned_tokens']-=inferred;summary['api_standard_usd_estimate']=round(sum(t['api_standard_usd_estimate'] for t in tasks),2)
assert summary['unassigned_tokens']>=0
repo='fssrepository/myscoutee-roadmap'
for t in tasks:
 models=collections.Counter()
 for key,v in t['models'].items():models[key]+=v['total_tokens']
 ordered=sorted(models,key=models.get,reverse=True);t['model_display']='; '.join(dict.fromkeys(x.split('|')[0]+(' (est.)' if x.endswith('|estimated') else '') for x in ordered)) or 'Unknown'
 t['effort_display']='; '.join(dict.fromkeys(x.split('|')[1] if not x.endswith('|estimated') else 'unrecorded' for x in ordered)) or 'Unrecorded'
 lines=[f"Retrospective record of **{t['title'][0].lower()+t['title'][1:]}**.",'',f"Historical execution: **{t['start']} → {t['end']} (UTC dates)**. This issue was created retrospectively on 2026-10-01; its creation/closure time is not the historical execution time.",'',f"Workstream: **{t['area']}**",'','| Metric | Value |','| --- | --- |',f"| Tokens, including cached input | {t['tokens_estimate']/1e6:,.2f} M |",f"| Standard API list-price equivalent | approximately ${t['api_standard_usd_estimate']:,.0f} USD |",f"| Active task time | approximately {t['activity_hours_estimate']:,.1f} h |",f"| Model(s) | {t['model_display']} |",f"| Reasoning effort | {t['effort_display']} |",'',f"Token basis: {t['token_basis']}.",f"Time basis: {t['duration_basis']}."]
 if 'joint_hours_low' in t:lines.append(f"Joint collaboration window: {t['joint_hours_low']:.2f}–{t['joint_hours_high']:.2f} h under the existing audit's 15–30 minute gap rules.")
 lines+=['','The USD figure is an estimate using the 2026-10-01 Standard short-context API rate card. It is not a subscription invoice or a verified payment. Missing model/mix data is estimated; quota-driven model switches may be unobserved. Image/video provider credits are separate.','',f"[Accounting method and limitations](https://github.com/{repo}#measurement-method)"]
 if t.get('frozen_audit_phase'):
  lines+=['','This phase reuses the frozen 2026-09-12 production audit. Its recorded token totals and model/effort values are preserved; the audit itself is outside the original production cutoff.']
 if t['key']=='B53':lines+=['','The local title is measured. The original master-prompt conversation is missing. The creator reports roughly one additional day for that prompt; that is not converted into 24 working hours. The August 27 Git snapshot predates GPT-6 Astra, so GPT-5.6 Sol is the estimated original model. Unmeasured original-prompt tokens remain outside this frozen phase total.']
 lines+=['','Delivery evidence:']
 if t['commits']:
  seen=set()
  for c in t['commits']:
   if c['sha'] in seen:continue
   seen.add(c['sha']);name='myscoutee' if c['repo'].endswith('/frontend') else c['repo'];lines.append(f"- {name}: [{c['title']}](https://github.com/fssrepository/{name}/commit/{c['sha']})")
  lines+=['','The commits record delivered work. This retrospective does not claim a fresh test run. Some consolidated commits cover several tasks; the references preserve that relationship without splitting their code changes. Private source repositories retain their access restrictions.']
 else:lines+=['- Historical conversation and delivered-artifact records; no standalone Git commit was identified for this task.','- This record summarizes the historical work; it does not claim a new publication or deployment.']
 if t.get('manual_time_unknown'):
  lines=[f"Historical record: **{t['title']}**.",'',f"Archive/import dates: {t['start']} → {t['end']}; these do not establish the original development period.",'','The creator confirms that this is primarily manual legacy development. Historical effort is unknown and is deliberately left blank. Git commit spacing does not establish working hours. Minor AI help with GitHub may have occurred, but no task-level record supports assigning tokens, models or costs to this work.','',*lines[lines.index('Delivery evidence:'):]]
 if t['project_scope']=='math':lines+=['','Research status: finite-model experiments, numerical diagnostics and partial lemmas do not establish a solution of the continuous Navier–Stokes Millennium problem. The later withdrawal of amplitude-inhomogeneous normalization claims is recorded separately (MATH-14).']
 t['issue_body']='\n'.join(lines)+'\n'
 t['project_fields']={'Task ID':t['provisional_id'],'Workstream':t['area'],'Started':t['start'],'Finished':t['end'],'Tokens M':round(t['tokens_estimate']/1e6,2),'API equiv USD':round(t['api_standard_usd_estimate']),'Active h':round(t['activity_hours_estimate'],1),'Models':t['model_display'][:1000],'Reasoning':t['effort_display'],'Evidence':'Frozen audit' if t.get('frozen_audit_phase') else 'Estimated allocation'}
for t in tasks:
 if t.get('manual_time_unknown'):
  for k in ['Tokens M','API equiv USD','Active h','Models','Reasoning']:t['project_fields'].pop(k,None)
  t['project_fields']['Evidence']='Manual legacy; effort unknown'
(P/'prepared-tasks.json').write_text(json.dumps(tasks,indent=2)+'\n');(P/'prepared-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
publicrows=[{'task_id':t['provisional_id'],'title':t['title'],'workstream':t['area'],'historical_start_utc':t['start'],'historical_end_utc':t['end'],'tokens_million':round(t['tokens_estimate']/1e6,2),'api_equivalent_usd_estimate':round(t['api_standard_usd_estimate']),'active_hours_estimate':t['activity_hours_estimate'],'models':t['model_display'],'reasoning':t['effort_display'],'evidence':t['token_basis']} for t in tasks]
f=io.StringIO();w=csv.DictWriter(f,fieldnames=list(publicrows[0]));w.writeheader();w.writerows(publicrows);(out/'tasks.csv').write_text(f.getvalue());(out/'tasks.json').write_text(json.dumps(publicrows,indent=2)+'\n')
accounts=json.loads((P/'account-usage.json').read_text());(out/'account-daily-usage.json').write_text(json.dumps(accounts,indent=2)+'\n')
readme=f'''# MyScoutee delivery history

A public retrospective of the MyScoutee system and its related creative work: application features, quality assurance, deployment, integrations, books, films and promotional assets.

The record covers **9 source repositories, 197 consolidated commits and {len(tasks)} reconstructed tasks**. Source repositories keep their existing visibility. This repository contains curated task summaries and aggregate measurements, not private conversations or private source code.

[Open the delivery Project](PROJECT_URL) · [Browse tasks](https://github.com/{repo}/issues?q=is%3Aissue) · [Download task metrics](tasks.csv)

## Recorded scale

| Measure | Value |
| --- | ---: |
| Account tokens, 2026-02-04 through 2026-09-30 | **38,488,016,278** |
| Account daily records | **167** |
| Tokens allocated to listed tasks, estimated | **{summary['allocated_tokens_estimate']/1e9:.2f} billion** |
| Account tokens still unassigned | **{summary['unassigned_tokens']/1e9:.2f} billion** |
| Standard API list-price equivalent of listed tasks | **approximately ${summary['api_standard_usd_estimate']:,.0f} USD** |

The account total is measured account-wide activity. It includes repeatedly processed context and is not a count of original words produced. The task allocation and USD value are retrospective estimates. The USD value is **not the amount paid for a ChatGPT subscription**, a provider invoice, or a proven monetary saving.

## Measurement method

- Local active and archived `.codex` histories are the primary execution evidence. All 649 JSONL files were inventoried, including split conversations; the history database was checked for additional coverage. Local retained conversations start on July 22, while account daily records reach February 4.
- Reuse the existing production audit method: unique response IDs when available; positive cumulative-counter differences for older records; unchanged counters contribute nothing; an initial partial counter or reset contributes only its recorded last response. Approval-review histories are not counted as extra user work. Cached input is inside input; reasoning output is inside output.
- Reuse the frozen September 12 film/book audit without changing its 14 phase totals: **{summary['frozen_production_audit_tokens']/1e9:.3f} billion logged tokens**, including the separately identified product campaign. Its cutoff excludes that audit's own work. Those tokens are reserved before allocating other account activity, so they are not counted twice.
- For other tasks, date/topic evidence from original commits and conversation requests supplies allocation weights. The daily account totals are control totals. Task splits remain estimates, particularly for mixed conversations and work before local history retention. Unrelated or unsupported activity remains unassigned. {inferred/1e6:.1f} M tokens for tasks without isolated daily evidence are comparable-task estimates reserved from the unassigned account balance; their daily attribution is unavailable.
- Active time follows the existing audit's union of recorded task intervals, so overlapping root intervals are not added twice. It includes tool execution and waiting within active tasks and is not a human timesheet. Missing timing is estimated from comparable observed work. Frozen creative tasks also retain their 15–30 minute joint-window estimates.
- Historical start/finish fields describe when the work happened. GitHub issue creation/closure dates describe this retrospective import. A historical Done record is evidence of delivered work, not a claim that the current software was retested during import.
- Logged model/effort values take precedence. When missing, the creator's stated preference for the strongest available Codex model is combined with release dates: GPT-5.3-Codex from February 5, GPT-5.4 from March 5, GPT-5.5 from April 23, GPT-5.6 Sol from July 9, GPT-6 Astra from September 3. These are explicitly estimated selections; quota-driven fallbacks and rollout timing may differ. Missing reasoning effort remains unrecorded.
- USD estimates use [OpenAI's Standard API rates](https://developers.openai.com/api/docs/pricing), valued on 2026-10-01, for input, cached input, cache writes when observed, and output. Missing token mix is estimated from observed sessions. This standardized short-context comparison excludes Fast/Ultrafast, long-context and regional uplifts, subscription charging, infrastructure, and image/video/TTS-provider credits. It is not historical billing reconciliation.

Model date sources: [GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/), [GPT-5.4](https://openai.com/index/introducing-gpt-5-4/), [GPT-5.5](https://openai.com/index/introducing-gpt-5-5/), [GPT-5.6](https://openai.com/index/gpt-5-6/), [GPT-6 Astra](https://openai.com/index/safety-overview-gpt-6-astra/).

## Task identifiers and Git history

`MSC-N` corresponds to issue `#N` here. Commit subjects reference their relevant task IDs and commit bodies link the public issues. A mixed commit can reference several tasks. Task grouping changes commit metadata, not the application file contents; existing release tags continue to identify their original commits.

The public [CSV](tasks.csv) and [JSON](tasks.json) are presentation exports. Raw conversations, credentials, local machine paths and private evidence remain local. Individual issue descriptions distinguish frozen measurements from estimates.
'''
(out/'README.md').write_text(readme)
print(json.dumps({'tasks':len(tasks),'analogy_tokens':inferred,'allocated':summary['allocated_tokens_estimate'],'unassigned':summary['unassigned_tokens'],'usd_estimate':summary['api_standard_usd_estimate']}))
