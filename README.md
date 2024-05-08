## Pytest GCS

This is a pytest plugin in similar vein to [pytest-postgres](https://github.com/ClearcodeHQ/pytest-postgresql) and [pytest-kafka](https://pypi.org/project/pytest-kafka/).

This would have been much more painful without [Mirakuru](https://github.com/ClearcodeHQ/mirakuru)
and [bigquery-emulator](https://github.com/goccy/bigquery-emulator); this is a simple wrapper around
those tools.


### Installation

This tool requires you to have a copy of the `bigquery-emulator` binary somewhere on your path.
Depending upon your architecture you'll need a different version of the tool.

```sh
wget https://github.com/goccy/bigquery-emulator/releases/download/v0.6.1/bigquery-emulator-linux-amd64
mv bigquery-emulator-linux-amd64 /usr/local/bin/bigquery-emulator
```

To install this library:

```sh
pip install pytest-bq
```


### Demo

```python
# conftest.py
from pytest_bq.factories import client as bq_client
from pytest_bq.factories import proc as bq_process

# Create a process and a local client that targets that process.
bq_proc = bq_process.bq_proc(executable='/usr/local/bin/bigquery-emulator', project_id='test')
bqlocal = bq_client.bqlocal("bq_proc")

# tests/test_bq.py
from google.cloud import bigquery
from pytest_bq.executor.process import BQExecutor


def test_can_list_datasets(bq_proc: BQExecutor, bqlocal: bigquery.Client) -> None:
    """MVP to ensure everything works."""
    test_dataset = "test_base"
    bqlocal.create_dataset(test_dataset)
    datasets = [x.full_dataset_id for x in bqlocal.list_datasets()]

    assert test_dataset in datasets
```


### Contributing

PRs are accepted.

```sh
# Install the dependencies with:
pip install .[test]
# Install pre-commit hooks.
pre-commit install
# Validate everything passes.
pre-commit run --all
# Run the tests.
pytest tests/
```


### TODOs

* Implement the events outputs, `-event.bucket`, `-event.list`, etc.
