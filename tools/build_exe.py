"""Build the standalone Windows executable in the project root."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ENTRY_POINT = PROJECT_ROOT / "tanks.py"


def main() -> None:
	"""Create ``Tanks.exe`` beside the README and source launcher."""
	command = [
		sys.executable,
		"-m",
		"PyInstaller",
		"--noconfirm",
		"--clean",
		"--onefile",
		"--windowed",
		"--name",
		"Tanks",
		"--paths",
		str(PROJECT_ROOT / "src"),
		"--distpath",
		str(PROJECT_ROOT),
		"--workpath",
		str(PROJECT_ROOT / "build" / "pyinstaller"),
		"--specpath",
		str(PROJECT_ROOT / "build"),
		str(SOURCE_ENTRY_POINT),
	]
	subprocess.run(command, cwd=PROJECT_ROOT, check=True)


if __name__ == "__main__":
	main()
