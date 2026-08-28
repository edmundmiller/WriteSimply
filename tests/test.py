#!/usr/bin/env python3
"""Run WriteSimply's package-install and fixture tests."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
VALE = os.environ.get("VALE", "vale")


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def main() -> None:
    expected_version = (ROOT / ".vale-version").read_text().strip()
    actual_version = run(VALE, "--version").stdout.strip()
    if actual_version != f"vale version {expected_version}":
        raise AssertionError(
            f"expected Vale {expected_version}, got {actual_version!r}"
        )

    expected = json.loads((ROOT / "tests/cases.json").read_text())
    with tempfile.TemporaryDirectory(prefix="write-simply-") as temporary:
        temp = Path(temporary)
        package = temp / "WriteSimply.zip"
        run("python3", str(ROOT / "scripts/package.py"), str(package))
        second_package = temp / "WriteSimply-second.zip"
        run("python3", str(ROOT / "scripts/package.py"), str(second_package))
        if package.read_bytes() != second_package.read_bytes():
            raise AssertionError("consecutive package builds are not reproducible")

        consumer = temp / "consumer"
        fixtures = consumer / "fixtures"
        fixtures.mkdir(parents=True)
        shutil.copytree(ROOT / "tests/fixtures", fixtures, dirs_exist_ok=True)
        documentation = consumer / "documentation"
        documentation.mkdir()
        documentation_files = sorted(ROOT.glob("*.md"))
        for source in documentation_files:
            shutil.copy2(source, documentation / source.name)
        (consumer / ".vale.ini").write_text(
            "StylesPath = styles\n"
            "MinAlertLevel = suggestion\n"
            "IgnoredScopes = code, tt, img, url, a\n"
            "SkippedScopes = script, style, pre, figure, code\n"
            f"Packages = {package}\n\n"
            "[*.{md,mdx}]\n"
            "BasedOnStyles = WriteSimply\n"
        )

        run(VALE, "sync", cwd=consumer)
        installed = consumer / "styles/WriteSimply"
        if not installed.is_dir():
            raise AssertionError("vale sync did not install WriteSimply")
        for source in (ROOT / "WriteSimply").iterdir():
            if source.read_bytes() != (installed / source.name).read_bytes():
                raise AssertionError(f"installed {source.name} differs from source")

        result = run(
            VALE,
            "--output=JSON",
            *[str(fixtures / name) for name in expected],
            cwd=consumer,
        )
        observed_json = json.loads(result.stdout or "{}")

        for fixture_name, wanted in expected.items():
            fixture_path = str(fixtures / fixture_name)
            alerts = observed_json.get(fixture_path, [])
            observed = [
                [
                    alert["Check"],
                    alert["Match"],
                    (alert.get("Action", {}).get("Params") or [None])[0],
                ]
                for alert in alerts
            ]
            if observed != wanted:
                raise AssertionError(
                    f"{fixture_name}: expected {wanted!r}, observed {observed!r}"
                )
            for alert in alerts:
                if (
                    alert["Check"] == "WriteSimply.SentenceLength"
                    and alert["Message"]
                    != "This sentence has 36 words; split or simplify it."
                ):
                    raise AssertionError(
                        f"unexpected sentence count: {alert['Message']!r}"
                    )

        docs_result = run(
            VALE,
            "--output=JSON",
            *[str(documentation / source.name) for source in documentation_files],
            cwd=consumer,
        )
        docs_alerts = json.loads(docs_result.stdout or "{}")
        if docs_alerts:
            findings = {
                Path(path).name: [alert["Check"] for alert in alerts]
                for path, alerts in docs_alerts.items()
            }
            raise AssertionError(f"documentation has style findings: {findings!r}")

    print(
        f"PASS: Vale {expected_version}; sync, {len(expected)} fixtures, "
        f"and {len(documentation_files)} documentation files verified"
    )


if __name__ == "__main__":
    main()
