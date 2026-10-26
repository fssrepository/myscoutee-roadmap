# Restorable Project history

Project snapshot checked 2026-10-26: 127 tracked tasks / 127 measured; MSC-129 is closed. [Live Project](https://github.com/users/fssrepository/projects/2) · [Canonical complete backup](https://github.com/fssrepository/myscoutee-roadmap/tree/master/guides/statistics/myscoutee).

`project.json` preserves full issue bodies, statuses, typed field values and views. `measurements.json` preserves model/token/cost/time components and assumptions. `commit-map.json` links original and task-prefixed commit IDs. CSV/JSON provide convenient presentation exports. Recorded root intervals are retained in compressed JSON for timing reconstruction; there are no private chat texts.

## Validate offline

Run from the repository root:

```bash
python3 guides/statistics/myscoutee/restore_project.py
```

This validates all SHA256SUMS files and snapshot structure without network access.

## Recreate a deleted Project

Set `GITHUB_PROJECT_TOKEN` in your local shell to a credential with Projects write access. Run the same command with `--apply`. The script creates a new Project and restores task associations, fields, values, statuses and visible-column views; existing issues and source commits are preserved. Local progress is saved for retries. Use a separate `--state` file to create another copy. A repository subset restores only the tasks in that subset; use the complete backup to restore the whole Project.

If issues were deleted too, set `GITHUB_REPOSITORY_TOKEN` to an issue-write credential and add `--recreate-missing-issues`. The tracker repository must exist. Recreated issues may receive new issue numbers; stable task IDs remain. Historical execution dates remain in fields, while GitHub creation/closure timestamps reflect restoration.

Repository associations are included in `project.json`. Set `GITHUB_REPOSITORY_TOKEN` (or a suitable `GITHUB_TOKEN`) during restoration to reconnect them automatically. Separate Project-write and repository credentials are supported. Comments, automations and permission grants are outside this reconstruction. Read [METHOD.md](METHOD.md) for estimates, unknown values and measurement boundaries. Git versions these files; no dated folder is needed.

## Subsequent task measurements

The October 9 MSC-120/121 token update is retained in the existing
`measurements.json` `post_control_task_usage` ledger and in the live Project.
The 111-task calibration remains historical; the complete 127-task restoration snapshot also retains later task bodies and statuses. Mixed-session
attribution and exact measurement cutoffs are recorded beside each total.
The current README summary uses `current_project_totals`, merging measurements by
stable task ID. It includes MSC-114/115/116/117/118/119/120/121/122/123/124/125/126/127/128 once and preserves MSC-113 already present
in the historical total. The live Project currently tracks 127 tasks; 127 have
measurements. MSC-129 is closed. The recovered MSC-114 initial batch is separate from later MSC-123 work.

## MSC-121 closeout

Closed / Project Done. Final deployment evidence is Helm 123; usage is recorded through 2026-10-09T15:12:03.126Z. The latest task components and intervals are in `measurements.json` under `post_control_task_usage`; these replace earlier checkpoints by task ID. Historical calibration totals remain frozen. The October-10 publication turn is excluded.

The canonical roadmap `commit-map.json` records the October-10 consolidation;
repository subset maps retain their earlier reconstruction boundary. Runtime
verification is the recorded October-9 evidence; the October-10 SSH check could
not reach the KVM and did not restart it.

Consolidated source commits: [backend `0941aac8`](https://github.com/fssrepository/myscoutee-backend/commit/0941aac8a700b7c2c6cc7aef2b4dda61fbd44d99) and [frontend `3601abd4`](https://github.com/fssrepository/myscoutee/commit/3601abd40a05c4746c2d57c62e0d15cc7392bba6). The 15 original commits map to these two in `commit-map.json`; the backend gitlink records the new frontend commit.

## MSC-122 closeout

Closed / Project Done. Original template/components 1.4.0 publication and exact DEB VMware verification remain accepted. October 17 template regression 1–32 PASS / CLOSED, including point 31 and cleanup; no new DEB installation is claimed. **1,304,324,997 tokens**, **46.917611 active / 46.804358 allocated hours**, through `2026-10-17T07:51:53.465Z`. The original 1,134,112,133-token delivery and 170,212,864-token regression increment are retained as components, counted once. **$1,599.94 Standard API equivalent**, including the October 24 missing-rate supplement. Reproduce the increment with `measure-msc122-regression.py --cutoff 2026-10-17T07:51:53.465Z`. Corrections, reverted attempts and failure/recovery are included; final accounting/publication after cutoff excluded.

## MSC-115 closeout

Closed / Project Done through QA step 119. Usage through 2026-10-15T11:52:55.467000+00:00: **1,328,857,714 tokens**, **48.248381 active/allocated hours**, **$1,749.59 Standard API equivalent**. Exact response components, interval union, scope exclusions and attribution limits are in `post_control_task_usage`. Separate template/live qualification and compilation optimization do not reopen this closed scope.

The three final backend commits were consolidated into [`799918535`](https://github.com/fssrepository/myscoutee-backend/commit/799918535e832f3e77eee27cef9fb57f49a93c01) at the user’s request. The final tree and frontend gitlink are identical; the original-to-consolidated mapping is in `commit-map.json`. The optimization follow-up note remains separate in scope.

## MSC-116 closeout

Closed / Project Done for consolidated development QA through step85, including the remaining MSC-119 introduction. Exact usage, selected windows, exclusions and overlap allocation are in `measurements.json`; reproduce the recorded cutoff with `measure-msc116.py --cutoff 2026-10-15T20:52:03.159Z`. Template runtime and external-host/publication qualification remain separate. No duplicate MSC-119 measurement was added.

## MSC-117 closeout

Closed / Project Done for the accepted development scope. **105,282,015 tokens**, **5.206302 active/allocated hours** through `2026-10-16T09:26:30.000Z`. Reproduce with `measure-msc117.py --cutoff 2026-10-16T09:26:30.000Z`. **$107.32 Standard API equivalent**, including the October 24 missing-rate supplement. [QA evidence and limits](https://github.com/fssrepository/myscoutee-backend/blob/7f12b02ec102440d042b923cbd86a28e9573c94d/guides/qa/evidence/general/MSC117-20261016/summary.json); template/live qualification stays separate.

## MSC-118 usage update

**182,287,382 tokens**, **4.680690 active / 4.369485 allocated hours**, **$242.00 frozen Standard API equivalent**, through `2026-10-16T14:49:00Z`. Includes implementation, checklist preparation, QA, shared-list corrections and reverted attempts. Reproduce with `measure-msc118.py --cutoff 2026-10-16T14:49:00Z`. Scoped eight-step guide QA is PASS / CLOSED; template regression 1–32 PASS / CLOSED on October 17, accounted under MSC-122.


## October 17 history consolidation

Consecutive task commits and the regression backup commits were consolidated; the MSC-120 backend sequence is one commit. `commit-map.json` retains original-to-consolidated identities. Application trees are preserved; the approved changes are concise README/accounting updates, fresh `/docs` artifacts from the existing `npm run build:github` command, plus the installer workflow’s existing supported-tag restriction. Existing release tags are unchanged. The refactor branch is integrated into master; the obsolete backend Pages site and branch are removed after preserving the current frontend demo.

## MSC-123 deployment/release update

MSC-123 complete: VMware/device scope closed; app/template signed 1.4.1 and Components registry published. Production Netcup upgraded from package 1.3.0 / frontend 1.3.3 to exact signed 1.4.1; host qualification, 13 public checks, Angular render and retained-data checks PASS. 347,361,510 tokens / 5.688961 allocated h through 2026-10-17T14:40:04.051000+00:00; shared allocation counted once. **$49.04 Standard API equivalent**, including the October 24 missing-rate supplement. **5.688961 active / 5.688961 allocated hours**, 1,662 responses. Status: **Done**.

## Project metadata reconciliation

MSC-114 now retains all nine missing measurement fields for the isolated initial batch: **5,615,396 tokens**, **47 responses**, **0.199895 active/allocated h**, **$1.70 frozen API equivalent**, **gpt-6-sol / xhigh**, executed **1 October 2026**. Later security/dependency work remains allocated to MSC-123. MSC-121 Workstream is **QA and release**. Current totals include the recovered measurement once; historical calibration stays unchanged.

The requested documentation/metadata follow-up is folded into the existing MSC-123 commits: backend `756b9faf92edb65d327f1d3a621d01ba62a7bd76` and frontend `889d3281421b4a0a84f66e0866ced3ffd17ba7ac`. Six manuals now carry 1.4.1 internally and use stable filenames without version suffixes. The source mapping retains the preceding commit identities; signed release artifacts and existing tags retain their original identities.

## MSC-124 release and deployment

Closed / Project Done. MSC-124 complete: EN/HU/DE/ES application/admin/backend catalogs, nonblocking setup and Firebase/avatar fixes; VMware handoff and owner mobile checks accepted. Separate v1.4.2 tags/releases and two GHCR images published. Netcup partial update: 9 healthy containers, only API/nginx changed, 13/13 public HTTPS checks, four-language parity and retained users/configuration/947 media objects PASS. Installed DEB stays 1.4.1. 57,483,958 tokens / 1.864686 allocated h through 2026-10-19T22:28:52.036Z; includes the owner-assigned October 18 roadmap commit. **$71.49 Standard API equivalent**, including the October 24 missing-rate supplement.

**1.864686 active / 1.864686 allocated hours**, **444 responses**. Reproduce with `measure-msc124.py --cutoff 2026-10-19T22:28:52.036Z`. The requested October 18 roadmap/account-heatmap commit is retitled under MSC-124; its isolated measured interval is included once. Earlier maybe-breaking source commits are retained in `commit-map.json`. Separate 1.4.1 and 1.4.2 release entries are preserved. [Release notes](https://github.com/fssrepository/myscoutee-backend/releases/tag/v1.4.2). Final bookkeeping after the cutoff is excluded.

## MSC-126 release and deployment

Closed / Project Done for the delivered 1.4.5 batch. MSC-126 release batch complete: main/template loading groups and semantic captions, preferred-language/cache startup, guarded WebP/catalog/demo-lifecycle migrations, fullscreen mobile setup. Five v1.4.5 source releases/tags, five GHCR images and Components 1.4.5 published. Netcup 13/13 public checks; nine healthy containers; seven production users and original media retained. VMware verified. Installed DEBs remain 1.4.1. No matched Lighthouse gain or new template host qualification claimed. 288,442,597 tokens / 9.919969 allocated h through 2026-10-21T23:51:01Z; shared template/component effort counted once. **$51.19 Standard API equivalent**, including the October 24 missing-rate supplement.

**9.919969 active / 9.919969 allocated hours**, **1,513 responses**. Reproduce with `measure-msc126.py --cutoff 2026-10-21T23:51:01Z`. Detailed token components, source windows and interval union are retained in `measurements.json`. [Release](https://github.com/fssrepository/myscoutee-backend/releases/tag/v1.4.5) · [Task](https://github.com/fssrepository/myscoutee-roadmap/issues/164). Remaining Lighthouse priorities await a new matched report. Historical account totals remain frozen; final accounting after cutoff is excluded.

## MSC-127 closeout

MSC-127 closed by owner request; remaining fixes and qualification transferred to MSC-128. 1,237,840,553 tokens / 30.291569 allocated h / 6,744 responses through 2026-10-24T13:18:13.613Z. Includes corrections and reverted work; shared effort counted once. **$218.94 Standard API equivalent**, including the October 24 missing-rate supplement.

**30.687602 active / 30.291569 allocated hours**. Reproduce with `python3 guides/statistics/myscoutee/measure-msc127.py`. The 17 selected root histories use the existing response-ID deduplication and active-interval union. Previously allocated overlap is subtracted; shared work counts once. MSC-128 starts at `2026-10-24T13:18:13.614Z` and is excluded. This closure does not assert completion of the transferred checks.

126 tracked tasks; all 126 measured. **43,227,640,078 tokens**, **1,121.982 allocated h**, **$32,841.01 Standard API equivalent**. Costs are estimates, not invoices.

## Missing-field reconciliation

MSC-125: **266,804,531 tokens**, **8.059066 active/allocated hours**, **1,526 responses**, **$85.13 Standard API equivalent**, measured **20 October 2026, 08:41:34.758–22:53:55.173 UTC**. Reproduce with `measure-msc125.py`. The dedicated implementation/release session includes corrections and reverted attempts.

Missing API-equivalent cells for MSC-117/122/123/124/126/127 are filled using the October 24 pricing supplement. Previously priced components retain their valuation. Current totals are recomputed from one merged record per task, preserving earlier fields when a later checkpoint is partial. Historical calibration and account readings are unchanged. MSC-128 is now closed and measured in the closeout below.

## MSC-128 closeout

Completed **24–25 October 2026**, closed on the owner's confirmation. Main and template **1.5.0** releases are published, with consolidated MSC-128 source commits and matching tags. The release task is complete.

### Delivered

- Restored granular Components loading and consolidated shared sources; corrected startup, selected-language content, loading indicators, Guide/Setup behavior, profile/location handling, icon/font caching and gateway IP-ban behavior. Applicable fixes are included in both applications.
- Corrected encrypted account persistence, account/demo boundaries, login/logout and obsolete Base class mappings. CodeQL alerts 54 and 55 are fixed. Main backend standard suite: **2009/2009**; template: **440/440**; session regressions: **33/33 in each frontend**. Published Packaging verifier regressions: **11/11 with each application's configuration**.
- Published main/template production images, signed full DEBs, client tools, standalone archives and GitHub Pages. The template release has **14 verified assets**, including the corrected embedded client-tools archive. Shared packages remain at **1.5.0**.
- Netcup runs the exact final main DEB: host qualification passed, **9 healthy containers**, **7 matching managed-image fingerprints**, **13/13 public checks**. The template's earlier signed candidate passed VMware host qualification; the final packaging-only replacement was published with verified signatures and payload identities. The owner explicitly did not require another VMware installation of the final rebuild.

[Main backend release](https://github.com/fssrepository/myscoutee-backend/releases/tag/v1.5.0) · [Main downloads](https://github.com/fssrepository/myscoutee/releases/tag/v1.5.0) · [Template release](https://github.com/fssrepository/myscoutee-template/releases/tag/v1.5.0) · [Template frontend](https://github.com/fssrepository/myscoutee-template-frontend/releases/tag/v1.5.0)

Final DEB SHA-256: main `c5b6bb046b7276267112333e68d4a297e24f12d61eebe1cab86f4f8fcf0c62f3`; template `5498fa131f8728ce81db5163f456bdb0c0b9ab893a0cb607b0337fcddeb05fb1`.

### Measured effort

Measured period: **2026-10-24T13:18:13.614Z–2026-10-25T15:53:20.632Z (UTC)**. **663,694,269 tokens**, **17.308352 active / 17.308352 allocated hours**, **3,764 unique responses**, **$222.41 Standard API equivalent**.

The measurement combines **ten retained Codex sessions**, including continuations, separate frontend fixes, template delivery, corrections, failed and reverted attempts. Response IDs are deduplicated globally and active intervals are unioned; parallel activity is not added twice. Identifiable prior-task bookkeeping blocks are excluded; attribution of mixed operations is estimated. Tool/build/network waits count; idle gaps and this final accounting session are excluded. Cached input is included in input, reasoning in output. Shared main/template work is counted once. Models: gpt-6-astra and gpt-6.1-sol; high/xhigh reasoning.

[Reproduce the measurement](https://github.com/fssrepository/myscoutee-roadmap/blob/master/guides/statistics/myscoutee/measure-msc128.py) · [Ledger and method](https://github.com/fssrepository/myscoutee-roadmap/tree/master/guides/statistics/myscoutee). Existing frozen rates and the October 24 supplement are reused. API equivalent is an estimate, not an invoice. Account usage and task usage overlap and must not be added.


126 tracked tasks; all 126 measured. **43,227,640,078 tokens**, **1,121.982 allocated h**, **$32,841.01 Standard API equivalent**. Costs are estimates, not invoices.

## MSC-129 closeout

**337,935,588 tokens**, **15.062277 active / 15.062277 allocated hours**, **2,774 unique responses**, **$426.03 frozen Standard API equivalent**, through `2026-10-26T15:05:40Z`.

Completed 25–26 October 2026; the owner accepted the final template VMware result and requested documentation and closure.

## Delivered

- Reproducible Docker GitLab CE, myscoutee group, 22 project declarations, isolated validation and native build runners with four parallel build slots. Public defaults and project config/ci mappings are versioned; credentials remain in ignored files owned by the appropriate repository.
- Feature → master branching and manual integrated release branch/tag/publication/MR/PR flow. Normal builds and released-dependency consumer builds are automatic; tests, heavy packaging, infrastructure, deployment, release and Pages retain their explicit manual controls.
- Registry-first infrastructure preparation, reusable Terraform module with independent product state/configuration, separate domain images and unchanged-image reuse, GitLab Kubernetes agent/environment integration, scoped host setup and retention maintenance.
- GitHub Actions conversion is included but inactive under config/ci/github-actions.yml and was not separately executed. The two frontend Pages workflows were removed when publication switched to the permanent branch source.
- Automatic frontend builds prepare production and Pages output. Manual `deploy:github` commits ignored `docs/` to permanent `gh-pages/docs` from the existing checkout and requests a Pages build. MyScoutee, Template and e-kozig served content was verified against those branch outputs; master contains no generated docs.
- Shared document-viewer loading is centered for consent/help/terms in both frontends; the Template lazy consent indicator is centered too. Both frontend Pages builds passed.
- Source/package baseline remains 1.5.0; corrected shared dependency packages and locks are aligned. Trial release publications were withdrawn. One consolidated [MSC-129] commit per participating repository is synchronized to GitHub and GitLab.

## Accepted template qualification

| Target | Pipeline / jobs | Result |
| --- | --- | --- |
| Monolith | 563; deploy 2210, verify 2215 | 14 passed, 0 failed, 0 skipped; operator accepted |
| KVM | 567; package 2228, infra 2231, deploy 2232, verify 2237, agent retry 2241 | 10 public checks passed; all four domain images reused; operator accepted |
| VMware | 571; deploy 2253, verify 2258 | 11 passed, 0 failed, 3 HTTP checks skipped for the custom HTTPS tunnel; operator accepted |

Targets ran sequentially. Template VMware is left available at https://localhost:18445; monolith and KVM guests are stopped with data retained. SonarQube pipeline 488 / release job 2159 exercised the integrated release path; backend pipeline 489 / job 2165 exercised DEB packaging. No new backend/DEB rerun, Netcup deployment, full optional-test sweep or GitHub Actions runtime qualification is claimed.

## Documentation and repository closure

- [Backend access manual](https://github.com/fssrepository/myscoutee-backend/blob/master/guides/publication/manuals/MyScoutee_Laboratory_Access_Manual_EN.pdf)
- [Template access manual](https://github.com/fssrepository/myscoutee-template/blob/master/guides/publication/manuals/MyScoutee_Laboratory_Access_Manual_EN.pdf)
- [CI/CD branching and configuration manual](https://github.com/fssrepository/myscoutee-ci/blob/master/guides/publication/manuals/MyScoutee_CICD_Manual_EN.pdf)

All include the inactive Actions conversion. Editable sources/generators and logos are versioned; PDFs were visually checked. No PDF is copied to a frontend. CI references use guides/development/ci, not a parallel docs directory.

Full workspace audit includes the 25 owned repositories and their frontend checkouts; external Lean dependency checkouts are read-only. Owned source repositories have synchronized master branches and no unmerged feature/backup branches or local-only source commits; the three published frontend sites retain permanent gh-pages branches. At the owner's explicit request, the obsolete backend/frontend v1.4.2 tags and matching GitHub releases were removed; no untagged release remains. Existing application data and other releases are retained.

[Detailed qualification](https://github.com/fssrepository/myscoutee-ci/blob/master/guides/development/ci/verification.md) · [Completed plan](https://github.com/fssrepository/myscoutee-ci/blob/master/guides/development/ci/MSC-129-plan.md)


Reproduce with `python3 guides/statistics/myscoutee/measure-msc129.py`. Five root sessions, globally deduplicated responses and unioned active intervals; shared effort counted once.
