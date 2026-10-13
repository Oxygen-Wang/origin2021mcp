"""Install private CPython 3.8 wheels for the Origin 2021 Start App.

Run with the external Python 3.10+ used by the MCP server, after installing
the Start/Stop Apps. No administrator access or embedded pip is required.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REQUIREMENTS = [
    "numpy==1.24.4",
    "pandas==2.0.3",
    "originpro==1.1.15",
    "OriginExt==1.2.5",
    "openpyxl==3.1.5",
    "xlrd==2.0.2",
]


def patch_originpro(target: Path) -> None:
    """Defer Generator annotations evaluated by originpro under Python 3.8."""
    for name in ("project.py", "pe.py"):
        file = target / "originpro" / name
        source = file.read_text(encoding="utf-8-sig")
        directive = "from __future__ import annotations"
        if directive not in source:
            file.write_text(directive + "\n" + source, encoding="utf-8")


def main() -> None:
    default = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--app-dir", type=Path, default=default / "OriginLab/Apps/Origin MCP Bridge Start"
    )
    args = parser.parse_args()
    if not (args.app_dir / "start_bridge.py").is_file():
        parser.error("Install the Start/Stop Apps first: origin-mcp install-origin-app --force")
    target = args.app_dir / "python38-deps"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "--target",
            str(target),
            "--python-version",
            "3.8",
            "--platform",
            "win_amd64",
            "--implementation",
            "cp",
            "--abi",
            "cp38",
            "--only-binary=:all:",
            *REQUIREMENTS,
        ],
        check=True,
    )
    patch_originpro(target)
    print(f"Origin 2021 private dependencies ready: {target}")
    print("Restart Origin, then click Origin MCP Bridge Start.")


if __name__ == "__main__":
    main()
