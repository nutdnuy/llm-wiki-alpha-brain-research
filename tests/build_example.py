import sys
from copy import deepcopy
from pathlib import Path
from support import fixture, write
from storage import initialize
from brain_wiki import rebuild_index

destination = Path(sys.argv[1])
initialize(destination)
records = fixture(destination)
candidate = deepcopy(records[2])
candidate.update(
    id='cand-demo-python', title='Synthetic Python implementation', backend='python',
    expression='synthetic_five_session_change',
    settings=dict(engine='qlib', engine_version='synthetic-demo',
        code_revision='synthetic-code-manifest', data_snapshot='synthetic-data-manifest',
        universe='synthetic demonstration only', sample_start='2020-01-01',
        sample_end='2021-12-31', signal_lag_bars=1, execution_lag_bars=1,
        rebalance='daily', execution_price='next open', portfolio='synthetic equal weights',
        costs=dict(commission_bps=1, slippage_bps=2, borrow_bps_per_year=100)),
    notes='Synthetic counterpart of cand-demo; no code or market-data backtest was run.')
experiment = deepcopy(records[3])
experiment.update(id='exp-demo-python', title='Synthetic planned Python experiment',
    backend='python', candidate=candidate['id'], expression=candidate['expression'],
    settings=deepcopy(candidate['settings']))
records[4]['experiments'].append(experiment['id'])
for record in [candidate, experiment, records[4]]:
    write(destination, record)
rebuild_index(destination)
print('Created seven synthetic notes across BRAIN and Python; no simulation or backtest was run.')
