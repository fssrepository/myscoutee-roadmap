#!/usr/bin/env python3
"""Read-only MSC-126 accounting using the existing deduplicated task extractor."""
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
result = usage.extract('MSC-126', {
    '42894755145e8692': [('2026-10-21T12:16:33Z', '2026-10-21T12:18:27.999Z')],
    'f63318a2f5045701': [('2026-10-21T12:18:28Z', args.cutoff)],
}, args.cutoff, started='2026-10-21', include_archived_segments=True,
allow_unpriced_models=True,
note='Two dedicated MSC-126 root sessions: initial request and continued implementation/review, corrections, reverted attempts, focused tests, template applicability, migrations, VMware verification, source consolidation and requested 1.4.5 publication/Netcup release through the cutoff. Reuses unique response-ID accounting, union of observed root active intervals and subtraction of prior task allocations. Tool/build/network waits are included; idle gaps and bookkeeping after cutoff are excluded. Cached input is within input and reasoning within output. Template/shared-component work is one allocation, not counted per repository. Frozen known rates only; unpriced models remain unpriced. Timing is observed agent activity, not invented human working hours or an invoice.')
result['finished'] = datetime.fromisoformat(args.cutoff.replace('Z', '+00:00')).astimezone(ZoneInfo('Europe/Prague')).date().isoformat()
print(json.dumps(result, indent=2))
