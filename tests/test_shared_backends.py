"""Include the portable skill's backend contract suite in repository CI."""
import importlib.util
from support import SKILL

spec = importlib.util.spec_from_file_location(
    'skill_backend_tests', SKILL / 'tests/test_backends.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
SharedWikiTests = module.SharedWikiTests
