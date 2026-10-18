#!/usr/bin/env python3
"""Ensure Python tools required by the 2D asset pipeline are available."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import venv
from pathlib import Path


REQUIRED_IMPORTS = ("PIL",)


def can_import(python: Path, module: str) -> bool:
    result = subprocess.run(
        [str(python), "-c", f"import {module}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def install_requirements(python: Path, requirements: Path) -> None:
    subprocess.run(
        [str(python), "-m", "pip", "install", "-r", str(requirements)],
        check=True,
    )


def ensure_venv(venv_dir: Path) -> Path:
    python = venv_python(venv_dir)
    if not python.exists():
        venv.EnvBuilder(with_pip=True, clear=False).create(venv_dir)
    return python


def main() -> int:
    parser = argparse.ArgumentParser(description="Install/check Pillow for 2D animation asset scripts.")
    parser.add_argument(
        "--venv",
        default=".venv-2d-assets",
        help="Virtual environment directory to create when dependencies are missing.",
    )
    parser.add_argument(
        "--requirements",
        default=str(Path(__file__).resolve().parents[1] / "requirements.txt"),
        help="requirements.txt path.",
    )
    parser.add_argument(
        "--prefer-current-python",
        action="store_true",
        help="Use the current Python when dependencies are already installed there.",
    )
    args = parser.parse_args()

    current_python = Path(sys.executable)
    if args.prefer_current_python and all(can_import(current_python, module) for module in REQUIRED_IMPORTS):
        print(current_python)
        return 0

    venv_dir = Path(args.venv).expanduser().resolve()
    requirements = Path(args.requirements).expanduser().resolve()
    if not requirements.exists():
        raise SystemExit(f"requirements file not found: {requirements}")

    python = ensure_venv(venv_dir)
    if not all(can_import(python, module) for module in REQUIRED_IMPORTS):
        install_requirements(python, requirements)

    missing = [module for module in REQUIRED_IMPORTS if not can_import(python, module)]
    if missing:
        raise SystemExit(f"missing required modules after install: {', '.join(missing)}")

    print(python)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
