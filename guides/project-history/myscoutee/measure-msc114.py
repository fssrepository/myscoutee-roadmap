#!/usr/bin/env python3
"""Read-only MSC-114 initial CodeQL batch measurement; no conversation text."""
import importlib.util, json, pathlib, sys
sys.dont_write_bytecode = True
root = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('usage', root / 'measure-msc119.py')
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)
result = usage.extract('MSC-114',{'d681f480e18191e8':[('2026-10-01T05:00:25.000Z','2026-10-01T05:13:54.393Z')]},'2026-10-01T05:13:54.393Z',started='2026-10-01',include_archived_segments=True,note='Initial seven CodeQL code locations, diagnosis, focused fixes/tests and MSC-114 issue/commit creation. Includes active tool waits; excludes subsequent licence/publishing work and later CodeQL/dependency work allocated to MSC-123. Response IDs deduplicated; cached input is within input, reasoning within output. Full observed root turn intervals; task attribution scoped to this initial batch.')
print(json.dumps(result, indent=2))
