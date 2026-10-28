"""Reproduction contracts for records, not execution-engine API schemas."""
import json
import math
from model import SETTINGS

PYTHON_STRINGS = {
    'engine', 'engine_version', 'code_revision', 'data_snapshot', 'universe',
    'sample_start', 'sample_end', 'rebalance', 'execution_price', 'portfolio',
}
PYTHON_LAGS = {'signal_lag_bars', 'execution_lag_bars'}
COSTS = {'commission_bps', 'slippage_bps', 'borrow_bps_per_year'}


def backend(note):
    # Existing v0.1 records are BRAIN records; keep them readable unchanged.
    value = note.get('backend', 'brain')
    if value not in ('brain', 'python'):
        raise ValueError('backend must be brain or python')
    return value


def validate_settings(value, engine):
    if not isinstance(value, dict):
        raise ValueError('settings must be a mapping')
    json.dumps(value, allow_nan=False)
    if engine == 'brain':
        if not SETTINGS <= value.keys():
            raise ValueError('missing BRAIN reproduction settings')
        if any(value[k] is None for k in SETTINGS):
            raise ValueError('null reproduction setting')
        if type(value['delay']) is not int or value['delay'] < 0:
            raise ValueError('invalid delay')
        return
    required = PYTHON_STRINGS | PYTHON_LAGS | {'costs'}
    if not required <= value.keys():
        raise ValueError('missing Python reproduction settings')
    if any(not isinstance(value[k], str) or not value[k].strip() for k in PYTHON_STRINGS):
        raise ValueError('Python reproduction identifiers must be nonempty strings')
    from datetime import date
    try:
        start, end = (date.fromisoformat(value[k]) for k in ('sample_start', 'sample_end'))
    except ValueError:
        raise ValueError('sample dates must be ISO dates') from None
    if start > end:
        raise ValueError('sample_start must not follow sample_end')
    if any(type(value[k]) is not int or value[k] < 0 for k in PYTHON_LAGS):
        raise ValueError('Python lags must be nonnegative integer bars')
    costs = value['costs']
    if not isinstance(costs, dict) or not COSTS <= costs.keys():
        raise ValueError('Python costs require commission, slippage and annual borrow units')
    if any(type(costs[k]) not in (int, float) or not math.isfinite(costs[k])
           or costs[k] < 0 for k in COSTS):
        raise ValueError('Python costs must be finite nonnegative numbers')


def observed_kind(engine):
    return 'live_brain' if engine == 'brain' else 'local_backtest'


def same_run(a, b):
    return (backend(a) == backend(b) and a['expression'] == b['expression']
            and a['settings'] == b['settings'])
