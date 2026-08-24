#!/usr/bin/env python3
"""Build a reproducible style-only Vale package archive."""

from __future__ import annotations

from pathlib import Path
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "WriteSimply"
EXPECTED = {"Filler.yml", "PlainWords.yml", "SentenceLength.yml", "meta.json"}


def main() -> None:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist/WriteSimply.zip"
    files = {path.name for path in STYLE.iterdir() if path.is_file()}
    if files != EXPECTED:
        raise SystemExit(f"unexpected package contents: {sorted(files ^ EXPECTED)}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(STYLE.iterdir()):
            entry = zipfile.ZipInfo(f"WriteSimply/{source.name}")
            entry.date_time = (1980, 1, 1, 0, 0, 0)
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, source.read_bytes())

    print(output)


if __name__ == "__main__":
    main()
