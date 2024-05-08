"""pytest-bq plugin declaration."""

from shutil import which

from pytest import Parser

import pytest_bq.factories.client
import pytest_bq.factories.proc

_HELP_EXEC = "Exec file to target."
_HELP_HOST = "Host to run bq service on."
_HELP_PORT = "Port to run bq service on."
_HELP_GRPC_PORT = ""
_HELP_LOGLEVEL = (
    "Level for bucket logging. level for logging. Options"
    " same as for logrus: trace, debug, info, warn, error, fatal, and panic"
)
_HELP_PROJECT_ID = "Project ID to use."
_HELP_DATA_FROM_YAML = "bigquery-emulator configuration to use."


def pytest_addoption(parser: Parser) -> None:
    """Plugin configuration options."""
    parser.addini(name="bq_executable", help=_HELP_EXEC, default=which("bigquery"))
    parser.addini(name="bq_port", help=_HELP_PORT)
    parser.addini(name="bq_grpc_port", help=_HELP_GRPC_PORT)
    parser.addini(name="bq_loglevel", help=_HELP_LOGLEVEL)
    parser.addini(name="bq_project_id", help=_HELP_PROJECT_ID)
    parser.addini(name="bq_data_from_yaml", help=_HELP_DATA_FROM_YAML)

    parser.addoption(
        "--bq-executable", action="store", dest="bq_executable", help=_HELP_EXEC
    )
    parser.addoption("--bq-port", action="store", dest="bq_port", help=_HELP_PORT)
    parser.addoption(
        "--bq-grpc-port", action="store", dest="bq_grpc_port", help=_HELP_GRPC_PORT
    )
    parser.addoption(
        "--bq-loglevel", action="store", dest="bq_loglevel", help=_HELP_LOGLEVEL
    )
    parser.addoption(
        "--bq-project-id", action="store", dest="bq_project_id", help=_HELP_PROJECT_ID
    )
    parser.addoption(
        "--bq-data-from-yaml",
        action="store",
        dest="bq_data_from_yaml",
        help=_HELP_DATA_FROM_YAML,
    )
