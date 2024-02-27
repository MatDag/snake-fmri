"""Test the CLI with simple scenarios."""

import pytest
import subprocess
from hydra.test_utils.test_utils import run_python_script


def test_scenario1():
    cmd = ["src/snkf/cli/main.py", "--config-name=scenario1.yaml"]
    result, _err = run_python_script(cmd)
