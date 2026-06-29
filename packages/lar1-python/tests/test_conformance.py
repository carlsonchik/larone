"""Conformance tests against SPEC/conformance fixtures."""

from __future__ import annotations

import pytest

from lar1 import compact, parse, validate
from lar1.errors import Lar1ParseError
from tests.helpers import load_fixtures


@pytest.mark.parametrize(
    "fixture",
    load_fixtures("valid") + load_fixtures("enum"),
    ids=lambda f: f["id"],
)
def test_valid_fixtures(fixture: dict) -> None:
    parsed = parse(fixture["input"])
    assert {"LAR-1": parsed} == fixture["expected"]
    assert validate(parsed)
    assert compact(parsed) == fixture["input"]


@pytest.mark.parametrize(
    "fixture",
    load_fixtures("invalid"),
    ids=lambda f: f["id"],
)
def test_invalid_fixtures(fixture: dict) -> None:
    with pytest.raises(Lar1ParseError) as exc:
        parse(fixture["input"])
    assert exc.value.code == fixture["error"]


@pytest.mark.parametrize(
    "fixture",
    [f for f in load_fixtures("boundary") if f.get("expected")],
    ids=lambda f: f["id"],
)
def test_boundary_valid(fixture: dict) -> None:
    parsed = parse(fixture["input"])
    assert {"LAR-1": parsed} == fixture["expected"]
    assert validate(parsed)


@pytest.mark.parametrize(
    "fixture",
    [f for f in load_fixtures("boundary") if f.get("error")],
    ids=lambda f: f["id"],
)
def test_boundary_invalid(fixture: dict) -> None:
    with pytest.raises(Lar1ParseError) as exc:
        parse(fixture["input"])
    assert exc.value.code == fixture["error"]
