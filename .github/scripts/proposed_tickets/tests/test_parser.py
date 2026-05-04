from pathlib import Path

import pytest

from proposed_tickets.parser import FrontmatterError, parse_directory, parse_file, split_frontmatter

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_valid_feature():
    ticket = parse_file(FIXTURES / "valid-feature.md")
    assert ticket.frontmatter["title"] == "Add a user search endpoint"
    assert ticket.frontmatter["weight"] == 3
    assert "Endpoint accepts" in ticket.body
    assert ticket.is_epic is False


def test_parse_valid_epic_marks_is_epic():
    ticket = parse_file(FIXTURES / "valid-epic.md")
    assert ticket.is_epic is True


def test_split_frontmatter_no_opening_delimiter():
    with pytest.raises(FrontmatterError):
        split_frontmatter("no frontmatter here")


def test_split_frontmatter_no_closing_delimiter():
    with pytest.raises(FrontmatterError):
        split_frontmatter("---\ntitle: foo\nbody without closing")


def test_split_frontmatter_invalid_yaml():
    with pytest.raises(FrontmatterError):
        parse_file(FIXTURES / "invalid-bad-yaml.md")


def test_parse_directory_collects_errors_and_tickets(tmp_path: Path):
    (tmp_path / "a.md").write_text(
        '---\ntitle: "A"\n---\nbody\n', encoding="utf-8"
    )
    (tmp_path / "b.md").write_text("not a frontmatter file", encoding="utf-8")
    tickets, errors = parse_directory(tmp_path)
    assert [t.filename for t in tickets] == ["a.md"]
    assert len(errors) == 1
    assert errors[0][0].name == "b.md"
