from pathlib import Path

from proposed_tickets.validate import run

FIXTURES = Path(__file__).parent / "fixtures"


def test_offline_run_against_valid_only(tmp_path: Path):
    for name in (
        "valid-feature.md",
        "valid-epic.md",
        "valid-no-epic-but-epic-auto.md",
    ):
        (tmp_path / name).write_text(
            (FIXTURES / name).read_text(encoding="utf-8"), encoding="utf-8"
        )
    rc = run(tmp_path, offline=True, client=None)
    assert rc == 0


def test_offline_run_against_invalid_only(tmp_path: Path):
    for name in (
        "invalid-missing-title.md",
        "invalid-bad-due-date.md",
        "invalid-negative-weight.md",
        "invalid-bad-epic.md",
        "invalid-bad-yaml.md",
    ):
        (tmp_path / name).write_text(
            (FIXTURES / name).read_text(encoding="utf-8"), encoding="utf-8"
        )
    rc = run(tmp_path, offline=True, client=None)
    assert rc == 1


def test_offline_run_empty_directory_passes(tmp_path: Path):
    assert run(tmp_path, offline=True, client=None) == 0
