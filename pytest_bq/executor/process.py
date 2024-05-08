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
        data_from_yaml: Optional[str] = None,
        loglevel: Optional[str] = None,
    ) -> None:
        """Start up local BQ.

        Args:
            executable: executable to call.
            host: host address fixture will be started on.
            port: port fixture will listen on.
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
        ]

        if loglevel:
            command.extend(["--log-level", loglevel])

        if data_from_yaml:
            # TODO: Add some validation that is file is correctly formatted.
            command.extend(["--data-from-yaml", data_from_yaml])

        self._project_id = project_id
        self._starting_command = command
        self.executable = executable

        super().__init__(
            # TODO: Figure out why this returns a 500?
            command, url=f"http://localhost:{port}/bigquery/v2/projects", timeout=5, status="500"
        )

    def start(self) -> "BQExecutor":
        """Start the BQ executor."""
        super().start()
        return self

    @property
    def project_id(self) -> str:
        """Return the configured project_id the emulator is running under."""
        return self._project_id
