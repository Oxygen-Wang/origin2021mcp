"""Regressions for the Origin 2021 compatibility bridge."""

import runpy
from pathlib import Path

import pytest

from origin_mcp._py38_compat import zip_compat
from origin_mcp.app_installer import START_BRIDGE_PY


def test_strict_zip_rejects_either_truncated_input():
    for left, right in (([1, 2], [3]), ([1], [2, 3])):
        with pytest.raises(ValueError):
            list(zip_compat(iter(left), iter(right), strict=True))
    assert list(zip_compat([1, 2], [3, 4], strict=True)) == [(1, 3), (2, 4)]
    assert list(zip_compat(strict=True)) == []


def test_app_launcher_loads_private_dependencies_before_addon():
    assert START_BRIDGE_PY.index("deps = APP_DIR") < START_BRIDGE_PY.index("addon = _load_addon()")
    compile(START_BRIDGE_PY, "start_bridge.py", "exec")


def test_originpro_patch_is_idempotent(tmp_path):
    setup = runpy.run_path(str(Path(__file__).parents[1] / "scripts/setup_origin2021.py"))
    folder = tmp_path / "originpro"
    folder.mkdir()
    for name in ("project.py", "pe.py"):
        (folder / name).write_text("value = 1\n", encoding="utf-8")
    for _ in range(2):
        setup["patch_originpro"](tmp_path)
    for name in ("project.py", "pe.py"):
        assert (folder / name).read_text().count("from __future__ import annotations") == 1
