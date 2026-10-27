# MyScoutee Roadmap

Project boards, delivery history and AI usage across the portfolio.

| Project board | History |
| --- | --- |
| [MyScoutee](https://github.com/users/fssrepository/projects/2) | [Snapshot](guides/statistics/myscoutee/README.md) |
| [MyScoutee Template](https://github.com/users/fssrepository/projects/6) | [Snapshot](guides/statistics/myscoutee-template/README.md) |
| [MyScoutee Old](https://github.com/users/fssrepository/projects/3) | [Snapshot](guides/statistics/myscoutee-old/README.md) |
| [E-Kozig](https://github.com/users/fssrepository/projects/4) | [Snapshot](guides/statistics/e-kozig/README.md) |
| [Millennium Math Problems](https://github.com/users/fssrepository/projects/5) | [Snapshot](guides/statistics/math/README.md) |
| [AI Pilot](https://github.com/users/fssrepository/projects/7) | [AIP-1 and measurement](guides/statistics/ai-pilot/README.md) |

## AI activity

Measured period: **4 February – 26 October 2026 (October 26 partial)**.

| Measurement | Tokens |
| --- | ---: |
| Current Codex account — lifetime usage | **46.370 billion** (46,370,446,562) |
| Heatmap — combined recorded daily usage across three accounts | **48.617 billion** (48,617,018,763) |

**B means billion (1,000,000,000 tokens); M means million.** Both totals include cached input. The heatmap combines the current account's retained daily records with historical records from two other accounts. It preserves the September baseline; the current account reading includes a later September correction. The two totals overlap; they are separate measurements and must not be added together or to project/task totals. The account API was rechecked after the Pages/viewer closeout and returned the same exact lifetime and October 26 daily values, so the regenerated heatmap image is byte-identical.

The available report measures Codex account usage. A separate ChatGPT conversation-token total is unavailable and has not been added. Other-account history remains included with its original coverage.

![Daily AI token usage](guides/statistics/media/token-activity.png?v=bfb982604d50)

[Measurements](guides/statistics/myscoutee/measurements.json) · [Method](guides/statistics/myscoutee/METHOD.md) · [Daily totals](guides/statistics/account-coverage.json)

## AI Pilot delivery

[AIP-1](https://github.com/fssrepository/myscoutee-roadmap/issues/169) connects the [AI Pilot repository](https://github.com/fssrepository/ai-pilot) to its [Project board](https://github.com/users/fssrepository/projects/7). It records the Qwen inspection playground, Adaptive Llama and Repair Graph experiments, and the contextual `guides/` documentation. The repository history is consolidated into the single [`[AIP-1]` commit](https://github.com/fssrepository/ai-pilot/commit/1734b8373561b1a8a4d9d480349e48047ce1edc6).

Measured through `2026-10-27T18:51:50.018Z`: **53,114,285 tokens**, **3.223623 active / 0.149362 incremental allocated hours**, **421 unique responses**, **$77.83 estimated Standard API equivalent**. Concurrent MSC-122 time keeps its prior allocation. The [AI Pilot snapshot](guides/statistics/ai-pilot/README.md) explains the boundary and evidence.

[Reconstruction tools](guides/history-tools/README.md) · [License: AGPL-3.0](LICENSE)

## Latest mathematical delivery

[MATH-19](https://github.com/fssrepository/myscoutee-roadmap/issues/167) is **Done**: Lean verifies the unrestricted PNT-2/7/8/12/14 counterexamples, Cauchy identities and finite Gram-Schur inequality. **75 theorems, 259 audited declarations**, four expected proof rejections and C++ comparisons pass.

Full task: **14,834,641 tokens**, **0.823521 active / 0.798249 allocated h**, **$21.07 estimated Standard API equivalent**, **gpt-6-astra / high**, through `2026-10-25T16:43:58.451Z`. The previous 18-minute figure covered only the continuation. [Complete task and Project snapshot](guides/statistics/math/README.md).

## Latest CI/CD delivery

[MSC-129](https://github.com/fssrepository/myscoutee-roadmap/issues/168) is **Done**: CI/CD lab, integrated release/dependency flow, accepted template monolith/KVM/VMware, three branded manuals, permanent Pages branches and centered document loading. The GitHub Actions conversion is included and inactive. Sources remain **1.5.0**; no Netcup deployment.

**337,935,588 tokens**, **15.062277 active / 15.062277 allocated hours**, **2,774 unique responses**, **$426.03 frozen Standard API equivalent**, through `2026-10-26T15:05:40Z`. Five retained sessions; shared effort counted once.

127 tracked tasks; all 127 measured. **43,565,575,666 tokens**, **1,137.044 allocated h**, **$33,267.04 Standard API equivalent**. [Ledger and method](guides/statistics/myscoutee/README.md).

## Previous product delivery

[MSC-128](https://github.com/fssrepository/myscoutee-roadmap/issues/165) is **Done**: shared loading/session/localization fixes, main/template **1.5.0** releases, GitHub Pages and signed full installers are published. Netcup runs the final main DEB: **9 healthy containers, 13/13 public checks**. The template release contains **14 verified assets**, including its corrected embedded client tools. [Main release](https://github.com/fssrepository/myscoutee/releases/tag/v1.5.0) · [Template release](https://github.com/fssrepository/myscoutee-template/releases/tag/v1.5.0).

Measured **24–25 October 2026**, through `2026-10-25T15:53:20.632Z`: **663,694,269 tokens**, **17.308352 active / 17.308352 allocated hours**, **3,764 unique responses**, **$222.41 Standard API equivalent**, across **ten Codex sessions**. Corrections and reverted work are included; repeated response IDs and parallel time count once.

At the MSC-128 checkpoint: 126 measured tasks; 43,227,640,078 tokens, 1,121.982 allocated h and $32,841.01 API equivalent. Costs are estimates, not invoices. These task measurements overlap account readings and are not added to them. [Measurement details](guides/statistics/myscoutee/README.md).

## Previous delivery

[MSC-126 — MyScoutee 1.4.5](https://github.com/fssrepository/myscoutee-backend/releases/tag/v1.4.5): loading groups, semantic translations, preferred-language/backend cache startup and guarded WebP/catalog/demo-lifecycle migrations. Main and applicable template releases, five GHCR images, Components 1.4.5 and standalone artifacts are published. Netcup runs 1.4.5 with **13/13 public checks**, nine healthy containers and retained production users/original media. VMware is verified. Installed DEBs remain 1.4.1; no new full template-host qualification or matched Lighthouse score is claimed. [Task](https://github.com/fssrepository/myscoutee-roadmap/issues/164) · [Evidence and remaining priorities](https://github.com/fssrepository/myscoutee-backend/blob/v1.4.5/guides/plans/MSC-126_LIGHTHOUSE_GAINS.md).

## Earlier delivery

[MSC-125 — MyScoutee 1.4.4](https://github.com/fssrepository/myscoutee-backend/releases/tag/v1.4.4): temporary, nginx-controlled landing diagnostics with a bounded memory buffer, 15-second checkpoints for the first minute and early-exit flushing. Local permission/popup/auth/render/error signals, including bounded cleaned errors and load/lifecycle/prerender/user-activation observations, go to a separate nginx log; ordinary API events are retained in the normal log. GitHub releases and GHCR nginx aliases are published and deployed to Netcup. **13/13 public checks passed** on the lifecycle-diagnostic update, all nine containers healthy; only nginx changed. Installed DEB remains 1.4.1 and API image 1.4.2. The overwritten 1.4.4 also fixes stale notification identities after logout, preserves authenticated/background server cleanup, and passes 106 notification/session regressions. The final diagnostic-detail revision passes 59 Node and 23 analyzer checks, plus a live lifecycle/error-detail round trip and original HTML request header hints. The observations do not establish the reason for an early departure. [Release notes and evidence](https://github.com/fssrepository/myscoutee-backend/blob/v1.4.4/guides/releases/v1.4.4.md).

MSC-125 measured period: **20 October 2026, 08:41:34.758–22:53:55.173 UTC**. **266,804,531 tokens**, **8.059066 active/allocated hours**, **1,526 responses**, **$85.13 Standard API equivalent**. Recovered from the dedicated implementation/release session; corrections and reverted work included.

## Versioned source release

Release `v1.5.0` provides a source archive and SHA-256 checksum through GitHub
Releases. The archive is built directly from the version tag. This repository
contains roadmap documents and reconstruction tooling, with no runtime image.
