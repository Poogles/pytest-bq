"""BQ process executor.

Starts a local BQ server using the targeted configuration.
"""

from pathlib import Path
from typing import List, Optional

from mirakuru import HTTPExecutor


class BQExecutor(HTTPExecutor):
    """Local BQ executor."""

    def __init__(
        self,
        executable: Path,
        project_id: str,
        port: int,
        grpc_port: int,
        database_file_path: Path,
        data_from_yaml: Optional[str] = None,
        loglevel: Optional[str] = None,
    ) -> None:
        """Start up local BQ.

        Args:
            executable: executable to call.
            project_id: google project ID to start local emulator with
            port: api port fixture will listen on.
            grpc_port: port storage api fixture will listen on.

        Kwargs:
            database_file_path: bigquery-emulator config file path.
            loglevel: log level passed to `fake-BQ-server` binary.

        Returns:
            None
        """
        command = [
            str(executable),
            "--project",
            project_id,
            "--port",
            str(port),
            "--grpc-port",
            str(grpc_port),
            "--database",
            str(database_file_path),
        ]

        if loglevel:
            command.extend(["--log-level", loglevel])

        if data_from_yaml:
            # TODO: Add some validation that is file is correctly formatted.
            command.extend(["--data-from-yaml", data_from_yaml])

        self._project_id = project_id
        self._port = port
        self._grpc_port = grpc_port
        self._starting_command = command
        self.executable = executable

        super().__init__(
            # TODO: Figure out why this returns a 500?
            command,
            url=f"http://localhost:{port}/bigquery/v2/projects",
            timeout=5,
            status="500",
        )

    def start(self) -> "BQExecutor":
        """Start the BQ executor."""
        super().start()
        return self

    @property
    def project_id(self) -> str:
        """Configured project_id the emulator is running under."""
        return self._project_id

    @property
    def bq_api_port(self) -> int:
        """Configured port the bigquery api emulator is running on."""
        return self._port

    @property
    def storage_api_port(self) -> int:
        """Configured port the storage api is running under."""
        return self._grpc_port
