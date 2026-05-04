from pathlib import Path

from proposed_tickets.parser import parse_file
from proposed_tickets.schema import (
    labels_for_ticket,
    validate_pr_invariants,
    validate_ticket,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _load(name: str):
    return parse_file(FIXTURES / name)


def test_valid_feature_passes():
    assert validate_ticket(_load("valid-feature.md")) == []


def test_valid_epic_passes():
    assert validate_ticket(_load("valid-epic.md")) == []


def test_valid_no_epic_but_epic_auto_passes():
    assert validate_ticket(_load("valid-no-epic-but-epic-auto.md")) == []


def test_missing_title_fails():
    errors = validate_ticket(_load("invalid-missing-title.md"))
    assert any("title" in e for e in errors)


def test_bad_due_date_fails():
    errors = validate_ticket(_load("invalid-bad-due-date.md"))
    assert any("due_date" in e for e in errors)


def test_negative_weight_fails():
    errors = validate_ticket(_load("invalid-negative-weight.md"))
    assert any("weight" in e for e in errors)


def test_bad_epic_value_fails():
    errors = validate_ticket(_load("invalid-bad-epic.md"))
    assert any("epic" in e for e in errors)


def test_pr_invariants_allow_zero_or_one_epic():
    assert validate_pr_invariants([_load("valid-feature.md")]) == []
    assert validate_pr_invariants([_load("valid-epic.md")]) == []
    assert validate_pr_invariants(
        [_load("valid-epic.md"), _load("valid-feature.md")]
    ) == []


def test_pr_invariants_reject_two_epics(tmp_path: Path):
    epic_a = tmp_path / "epic-a.md"
    epic_b = tmp_path / "epic-b.md"
    body = '---\ntype: epic\ntitle: "X"\n---\n\nBody\n'
    epic_a.write_text(body, encoding="utf-8")
    epic_b.write_text(body, encoding="utf-8")
    errors = validate_pr_invariants([parse_file(epic_a), parse_file(epic_b)])
    assert errors and "At most one" in errors[0]


def test_labels_for_ticket_appends_weight_label():
    labels = labels_for_ticket(_load("valid-feature.md"))
    assert "weight:3" in labels
    assert "type::feature" in labels


def test_labels_for_ticket_no_weight_no_synthetic_label():
    labels = labels_for_ticket(_load("valid-no-epic-but-epic-auto.md"))
    assert all(not lbl.startswith("weight:") for lbl in labels)
