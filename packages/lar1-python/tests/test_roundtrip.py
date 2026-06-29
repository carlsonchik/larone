"""Round-trip tests for compact and JSON wire formats."""

from __future__ import annotations

import pytest

from lar1 import compact, deserialize_fields, parse, serialize
from lar1.enums import ENUMS
from tests.helpers import load_fixtures


@pytest.mark.parametrize("key,values", list(ENUMS.items()))
def test_compact_roundtrip_enums(key: str, values: tuple[str, ...]) -> None:
    for value in values:
        first = parse(f"LAR:{key}={value}")
        second = parse(compact(first))
        assert second == first


@pytest.mark.parametrize("l_val", [0, 0.5, 1])
def test_compact_roundtrip_likelihood(l_val: float) -> None:
    first = parse(f"LAR:L={l_val}")
    second = parse(compact(first))
    assert second == first


@pytest.mark.parametrize("key,values", list(ENUMS.items()))
def test_json_roundtrip_enums(key: str, values: tuple[str, ...]) -> None:
    for value in values:
        first = parse(f"LAR:{key}={value}")
        second = deserialize_fields(serialize(first))
        assert second == first


def test_full_roundtrip_samples() -> None:
    samples = [
        "LAR:T=now,S=here,C=obs,E=direct,L=0.95,V=verified_tool",
        "LAR:C=inf,L=0.72,V=unverified",
    ]
    for input_str in samples:
        a = parse(input_str)
        b = deserialize_fields(serialize(a))
        assert b == a
        c = parse(compact(a))
        assert c == a


@pytest.mark.parametrize(
    "fixture",
    load_fixtures("valid") + load_fixtures("enum"),
    ids=lambda f: f["id"],
)
def test_fixture_roundtrip(fixture: dict) -> None:
    first = parse(fixture["input"])
    assert parse(compact(first)) == first
    assert deserialize_fields(serialize(first)) == first
