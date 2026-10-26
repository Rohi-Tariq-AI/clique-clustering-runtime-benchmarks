from __future__ import annotations

import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
import networkx as nx


def describe_environment() -> dict:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "networkx_version": nx.__version__,
        "cpu_count": os.cpu_count(),
    }


def write_environment(path: str | Path) -> None:
    Path(path).write_text(json.dumps(describe_environment(), indent=2), encoding="utf-8")
