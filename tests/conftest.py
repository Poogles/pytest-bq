"""Tests main conftest file."""

import subprocess
import warnings

import pytest_bq.factories.client
import pytest_bq.factories.proc

warnings.filterwarnings(
    "error",
    category=DeprecationWarning,
    module="(_pytest|pytest|google|path|mirakuru).*",
)
executable_path = (
    subprocess.run("which bigquery-emulator", capture_output=True, shell=True)
    .stdout.decode()
    .strip("\n")
)


bq_proc = pytest_bq.factories.proc.bq_proc(
    executable=executable_path, project_id="test-base"
)
bqlocal = pytest_bq.factories.client.bqlocal("bq_proc")


bq_proc1 = pytest_bq.factories.proc.bq_proc(
    executable=executable_path,
    project_id="test-data",
    data_from_yaml="./tests/resources/test_data.yaml",
)
bqlocal1 = pytest_bq.factories.client.bqlocal("bq_proc1")
