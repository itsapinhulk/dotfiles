"""Run all test files in this directory, excluding shell-dependent tests."""

import sys
import unittest
from pathlib import Path

# test_update_git_submodules requires bash and has its own CI job restricted to
# unix runners, so it is excluded here.
EXCLUDE = {"test_update_git_submodules.py"}

test_dir = Path(__file__).parent
sys.path.insert(0, str(test_dir))

loader = unittest.TestLoader()
suite = unittest.TestSuite()
for path in sorted(test_dir.glob("test_*.py")):
    if path.name not in EXCLUDE:
        suite.addTests(loader.loadTestsFromName(path.stem))

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
