"""bq client fixture factory."""

from typing import Callable, Generator

import pytest
from _pytest.fixtures import FixtureRequest
from google.api_core.client_options import ClientOptions
from google.auth.credentials import AnonymousCredentials
from google.cloud import bigquery

from pytest_bq.executor import BQExecutor


def bqlocal(
    process_fixture_name: str,
) -> Callable[[FixtureRequest], Generator[bigquery.Client, None, None]]:
    """Create connection fixture factory for pytest-bq.

    Args:
        process_fixture_name: Name of fixture to load client on.

    Returns:
        Local bq client factory.
    """

    @pytest.fixture(scope="session")
    def bqlocal_factory(
        request: FixtureRequest,
    ) -> Generator[bigquery.Client, None, None]:
        """Create connection for pytest-bq.

        1. Load bq fixture.
        2. Create a new local client that targets the fixture.

        Args:
            request: pytest request fixture.

        Yields:
            bq client configured for test fixture.
        """
        proc_fixture: BQExecutor = request.getfixturevalue(process_fixture_name)

        endpoint = f"http://{proc_fixture.host}:{proc_fixture.port}"

        bq_client = bigquery.Client(
            proc_fixture.project_id,
            client_options=ClientOptions(api_endpoint=endpoint),
            credentials=AnonymousCredentials(),
        )
        yield bq_client

    return bqlocal_factory
