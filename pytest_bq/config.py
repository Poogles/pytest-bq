"""Config loading helpers."""

from typing import Any, List, Optional, TypedDict

from _pytest.fixtures import FixtureRequest


class GcsConfigType(TypedDict):
    """pytest-bq config definition type."""

    executable: str
    port: Optional[int]
    groc_port: Optional[int]
    project_id: str
    loglevel: str


def get_config(request: FixtureRequest) -> GcsConfigType:
    """Return a dictionary with config options."""

    def get_conf_option(option: str) -> Any:
        option_name = "bq_" + option
        return request.config.getoption(option_name) or request.config.getini(
            option_name
        )

    port = get_conf_option("port")
    grpc_port = get_conf_option("grpc_port")
    config: GcsConfigType = {
        "executable": get_conf_option("executable"),
        "project_id": get_conf_option("project_id"),
        "port": int(port) if port else None,
        "grpc_port": int(grpc_port) if grpc_port else None,
        "loglevel": get_conf_option("loglevel"),
        "data_from_yaml": get_conf_option("data_from_yaml"),
    }
    return config
