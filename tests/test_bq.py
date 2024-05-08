"""General plugin tests."""
import pytest
from google.cloud import bigquery

from pytest_bq.executor.process import BQExecutor


def test_can_list_datasets(bq_proc: BQExecutor, bqlocal: bigquery.Client) -> None:
    """MVP to ensure everything works."""
    test_dataset = "test_base"
    bqlocal.create_dataset(test_dataset)
    datasets = [x.full_dataset_id for x in bqlocal.list_datasets()]

    assert test_dataset in datasets


@pytest.fixture(scope="session")
def session_based_fixture(bq_proc: bigquery.Client) -> None:
    """Empty fixture to validate clients are session scoped."""
    pass


def test_validate_client_is_session_based(session_based_fixture: None) -> None:
    """Empty test that validates client is session scoped."""
    pass


def test_can_load_test_data_yaml(bqlocal1: bigquery.Client) -> None:
    """Test we can load test data and execute query against it."""
    job = bqlocal1.query(
        query="SELECT id FROM dataset1.table_a",
        job_config=bigquery.QueryJobConfig(),
    )
    results = [x.values() for x in job.result()]
    assert results == [(1, ), (2, )]
