# MyScoutee Roadmap

Project boards, delivery history and AI usage across the portfolio.

| Project board | History |
| --- | --- |
| [MyScoutee](https://github.com/users/fssrepository/projects/2) | [Snapshot](guides/project-history/myscoutee/README.md) |
| [MyScoutee Template](https://github.com/users/fssrepository/projects/6) | [Snapshot](guides/project-history/myscoutee-template/README.md) |
| [MyScoutee Old](https://github.com/users/fssrepository/projects/3) | [Snapshot](guides/project-history/myscoutee-old/README.md) |
| [E-Kozig](https://github.com/users/fssrepository/projects/4) | [Snapshot](guides/project-history/e-kozig/README.md) |
| [Millennium Math Problems](https://github.com/users/fssrepository/projects/5) | [Snapshot](guides/project-history/math/README.md) |

## AI activity

Usage through **17 October 2026**, refreshed **18 October**:

| Measurement | Tokens |
| --- | ---: |
| Current Codex account — lifetime usage | **43.129 billion** (43,129,237,675) |
| Heatmap — combined recorded daily usage across three accounts | **45.376 billion** (45,375,809,876) |

**B means billion (1,000,000,000 tokens); M means million.** Both totals include cached input. The heatmap combines the current account's retained daily records with historical records from two other accounts. It preserves the September baseline; the current account reading includes a later September correction. The two totals overlap; they are separate measurements and must not be added together or to project/task totals.

![Daily AI token usage](guides/project-history/media/token-activity.png)

[Measurements](guides/project-history/myscoutee/measurements.json) · [Method](guides/project-history/myscoutee/METHOD.md) · [Daily totals](guides/project-history/account-coverage.json)

[Reconstruction tools](guides/history-tools/README.md) · [License: AGPL-3.0](LICENSE)

## Latest delivery

[MSC-125 — MyScoutee 1.4.4](https://github.com/fssrepository/myscoutee-backend/releases/tag/v1.4.4): temporary, nginx-controlled landing diagnostics with a bounded memory buffer, 15-second checkpoints for the first minute and early-exit flushing. Local permission/popup/auth/render/error signals, including bounded cleaned errors and load/lifecycle/prerender/user-activation observations, go to a separate nginx log; ordinary API events are retained in the normal log. GitHub releases and GHCR nginx aliases are published and deployed to Netcup. **13/13 public checks passed** on the lifecycle-diagnostic update, all nine containers healthy; only nginx changed. Installed DEB remains 1.4.1 and API image 1.4.2. The overwritten 1.4.4 also fixes stale notification identities after logout, preserves authenticated/background server cleanup, and passes 106 notification/session regressions. The final diagnostic-detail revision passes 59 Node and 23 analyzer checks, plus a live lifecycle/error-detail round trip and original HTML request header hints. The observations do not establish the reason for an early departure. [Release notes and evidence](https://github.com/fssrepository/myscoutee-backend/blob/v1.4.4/guides/releases/v1.4.4.md).

MSC-125 usage has not been reconciled into the historical measurement ledger. The existing measured totals below remain unchanged.

Last measured task, MSC-124: **57,483,958 tokens**, **1.864686 allocated hours**, through `2026-10-19T22:28:52.036Z`; includes the owner-assigned October 18 roadmap update. [Project and measurement details](guides/project-history/myscoutee/README.md). Current Project: **122 measured tasks**, **40,770,858,128 tokens**, **1,056.403 allocated hours**. These task totals overlap the historical account readings above and are not added to them. Full API valuation is unavailable for unpriced models.
