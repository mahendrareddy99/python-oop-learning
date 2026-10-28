"""JSON persistence for the library application."""
import json
from pathlib import Path
from typing import Any
from .exceptions import StorageError


class JSONStorage:
    """Read and write JSON lists stored in the data directory."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or Path(__file__).resolve().parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        for filename in ("books.json", "members.json", "issues.json"):
            path = self.data_dir / filename
            if not path.exists():
                self.write(filename, [])

    def read(self, filename: str) -> list[dict[str, Any]]:
        """Load a JSON list; raise StorageError for invalid data."""
        path = self._path(filename)
        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                raise StorageError(f"{filename} must contain a JSON list.")
            return data
        except StorageError:
            raise
        except (OSError, json.JSONDecodeError) as exc:
            raise StorageError(f"Could not read {filename}: {exc}") from exc

    def write(self, filename: str, records: list[dict[str, Any]]) -> None:
        """Write records to JSON using a temporary file before replacing the target."""
        path = self._path(filename)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = path.with_suffix(path.suffix + ".tmp")
            with temp_path.open("w", encoding="utf-8") as file:
                json.dump(records, file, indent=2, ensure_ascii=False)
            temp_path.replace(path)
        except OSError as exc:
            raise StorageError(f"Could not write {filename}: {exc}") from exc

    def _path(self, filename: str) -> Path:
        """Allow only the known JSON data files."""
        allowed = {"books.json", "members.json", "issues.json"}
        if filename not in allowed:
            raise StorageError(f"Unsupported data file: {filename}")
        return self.data_dir / filename
