"""bq process factory."""
from pathlib import Path
from typing import Callable, Generator, Optional

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.tmpdir import TempPathFactory
from port_for import get_port

from pytest_bq.config import get_config
from pytest_bq.executor import BQExecutor


def bq_proc(
    executable: Optional[str] = None,
    project_id: Optional[str] = None,
    port: Optional[int] = None,
    grpc_port: Optional[int] = None,
    loglevel: Optional[str] = None,
    data_from_yaml: Optional[str] = None,
) -> Callable[[FixtureRequest, TempPathFactory], Generator[BQExecutor, None, None]]:
    """Fixture factory for pytest-bq."""

    @pytest.fixture(scope="session")
    def bq_proc_fixture(
        request: FixtureRequest, tmp_path_factory: TempPathFactory
    ) -> Generator[BQExecutor, None, None]:
        """Fixture for pytest-bq.

        This fixture:
        * Get configs.
        * Run bq process.
        * Stop bq process after tests runs and does any cleanup.

        Args:
            request: Request fixture we're targeting.
            tmp_path_factory: Temporary directory fixture.

        Yields:
            Configured and active bqExecutor.
        """
        config = get_config(request)

        bq_exec = executable or config["executable"]
        assert bq_exec, "Unable to find a bigquery-emulator exec."

        bq_project_id = project_id or config["project_id"]
        assert bq_project_id, "Project ID is required."

        bq_port = (
            get_port(port) if port else get_port(config["port"]) or get_port(None)
        )
        assert bq_port, "Unable to find a port available."
        bq_grpc_port = (
            get_port(grpc_port) if grpc_port else get_port(config["grpc_port"]) or get_port(None)
        )
        assert bq_grpc_port, "Unable to find a port available."

        bq_executor = BQExecutor(
            executable=Path(bq_exec),
            project_id=bq_project_id,
            data_from_yaml=data_from_yaml,
            port=bq_port,
            grpc_port=bq_grpc_port,
            loglevel=loglevel or config["loglevel"],
        )
        with bq_executor:
            yield bq_executor

    return bq_proc_fixture
