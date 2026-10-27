# AIP-1 measurement method

The ledger uses the existing `myscoutee/measure-msc119.py` response-ID and active-interval extractor. Three local root sessions were selected by the SHA-256 prefix of their thread IDs; no conversation text or account identifiers are published. The source windows are recorded in `measurements.json`.

- October 11: dedicated AI Pilot model selection, Qwen playground, Adaptive Llama and Repair Graph implementation through the final consolidation request. The earlier MyScoutee conversation-summary setup before 06:06 UTC is excluded.
- October 27: dedicated AI Pilot `guides/` reorganization from 18:27 to 18:31 UTC.
- October 27: AI Pilot task inquiry, AIP-1 Project work, source-history squash and roadmap publication from 18:46:49 to the fixed 18:56:15 UTC accounting cutoff. Final accounting updates after that cutoff are excluded.

Unique response IDs prevent duplicate tokens. Cached input is included in input; reasoning is included in output. Active time is the union of recorded root turns and includes tool/network waits. The prior MSC-122 interval overlaps the October 11 AI Pilot work by 3.074261 hours; it retains its previous allocation, so AIP-1 adds 0.223150 hours to portfolio totals. This incremental accounting does not change the MSC-122 ledger. The AI Pilot responses are distinct from MSC-122 responses, so all 55,517,627 task tokens are added to the current task allocation once. The account total is an overlapping control, not an amount to add.

The $78.50 figure applies the existing roadmap's frozen Standard short-context API rate card to measured input, cached input and output by recorded model. It is a comparison estimate, not an invoice. No human labor estimate or cost for local compute/model downloads is claimed. Final accounting updates after the recorded cutoff are excluded.
