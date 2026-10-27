# AIP-1 measurement method

The ledger uses the existing `myscoutee/measure-msc119.py` response-ID and active-interval extractor. Three local root sessions were selected by the SHA-256 prefix of their thread IDs; no conversation text or account identifiers are published. The source windows are recorded in `measurements.json`.

- October 11: dedicated AI Pilot model selection, Qwen playground, Adaptive Llama and Repair Graph implementation through the final consolidation request. The earlier MyScoutee conversation-summary setup before 06:06 UTC is excluded.
- October 27: dedicated AI Pilot `guides/` reorganization from 18:27 to 18:31 UTC.
- October 27: AI Pilot task inquiry and AIP-1 Project work from 18:46:49 to the fixed 18:51:50 UTC accounting cutoff. Work after that cutoff, including publication, is excluded.

Unique response IDs prevent duplicate tokens. Cached input is included in input; reasoning is included in output. Active time is the union of recorded root turns and includes tool/network waits. The prior MSC-122 interval overlaps the October 11 AI Pilot work by 3.074261 hours; it retains its previous allocation, so AIP-1 adds 0.149362 hours to portfolio totals. This incremental accounting does not change the MSC-122 ledger. The AI Pilot responses are distinct from MSC-122 responses, so all 53,114,285 task tokens are added to the current task allocation once. The account total is an overlapping control, not an amount to add.

The $77.83 figure applies the existing roadmap's frozen Standard short-context API rate card to measured input, cached input and output by recorded model. It is a comparison estimate, not an invoice. No human labor estimate or cost for local compute/model downloads is claimed. The active time and token totals stop at the recorded cutoff, so they are a lower bound for the complete publication task.
