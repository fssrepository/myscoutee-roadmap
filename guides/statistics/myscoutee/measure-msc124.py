#!/usr/bin/env python3
"""Read-only MSC-124 usage aggregation from the dedicated local task session."""
import argparse, importlib.util, json, pathlib, sys
from datetime import datetime
from zoneinfo import ZoneInfo
sys.dont_write_bytecode = True
root = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('usage', root / 'measure-msc119.py')
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cutoff', required=True)
args = parser.parse_args()
result = usage.extract('MSC-124', {
    'bcdd81d876863b21': [('2026-10-17T22:11:07.094Z', '2026-10-17T22:13:05.579Z')],
    'f594968caebae84b': [('2026-10-19T20:32:10.925Z', args.cutoff)],
}, args.cutoff, started='2026-10-18', include_archived_segments=True,
allow_unpriced_models=True,
note='Includes the separate October 18 account-heatmap commit explicitly assigned to MSC-124 by the owner, plus the dedicated four-language seeds/setup/sign-in task: implementation, corrections and reverted attempts, focused tests, VMware partial deployment, device handoff, source consolidation including the prior maybe-breaking commits, image publication, production Netcup partial update and release/accounting preparation through the cutoff. The earlier commits are retained in the source mapping; work before the observed session is not assigned invented usage. User-controlled login/permission interactions are not agent QA. Response IDs deduplicated and active intervals unioned; tool/build/network waits included, idle gaps excluded. Cached input is within input and reasoning within output. Existing frozen rates only; unpriced models remain unpriced. Final bookkeeping after the cutoff is excluded, not estimated.')
result['finished'] = datetime.fromisoformat(args.cutoff.replace('Z', '+00:00')).astimezone(ZoneInfo('Europe/Prague')).date().isoformat()
print(json.dumps(result, indent=2))
