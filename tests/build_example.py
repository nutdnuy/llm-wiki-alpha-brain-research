import sys
from pathlib import Path
from support import fixture
from storage import initialize
from brain_wiki import rebuild_index

destination = Path(sys.argv[1])
initialize(destination)
fixture(destination)
rebuild_index(destination)
print('Created five synthetic notes; no simulation was run.')
