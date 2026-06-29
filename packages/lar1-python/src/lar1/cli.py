"""LAR-1 command-line interface."""

from __future__ import annotations

import argparse
import json
import sys

from lar1 import compact, deserialize_fields, parse, serialize, validate
from lar1.errors import Lar1ParseError


def _read_input(path: str | None) -> str:
    if path and path != "-":
        with open(path, encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def cmd_validate(args: argparse.Namespace) -> int:
    raw = _read_input(args.file).strip()
    try:
        if raw.startswith("{"):
            data = deserialize_fields(raw)
        else:
            data = parse(raw)
        if validate(data):
            print("OK")
            return 0
        print("INVALID", file=sys.stderr)
        return 1
    except (Lar1ParseError, ValueError) as exc:
        code = getattr(exc, "code", "INVALID")
        print(code, file=sys.stderr)
        return 1


def cmd_compact(args: argparse.Namespace) -> int:
    raw = _read_input(args.file).strip()
    try:
        if raw.startswith("{"):
            data = deserialize_fields(raw)
        else:
            data = parse(raw)
        print(compact(data))
        return 0
    except (Lar1ParseError, ValueError) as exc:
        code = getattr(exc, "code", str(exc))
        print(code, file=sys.stderr)
        return 1


def cmd_json(args: argparse.Namespace) -> int:
    raw = _read_input(args.file).strip()
    try:
        data = parse(raw)
        print(serialize(data))
        return 0
    except Lar1ParseError as exc:
        print(exc.code, file=sys.stderr)
        return 1


def main() -> None:
    parser = argparse.ArgumentParser(prog="lar1", description="LAR-1 semantic overlay CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate", help="Validate compact or JSON input")
    p_validate.add_argument("file", nargs="?", default="-", help="File path or - for stdin")
    p_validate.set_defaults(func=cmd_validate)

    p_compact = sub.add_parser("compact", help="Output canonical compact string")
    p_compact.add_argument("file", nargs="?", default="-")
    p_compact.set_defaults(func=cmd_compact)

    p_json = sub.add_parser("json", help="Convert compact to application/lar+json")
    p_json.add_argument("file", nargs="?", default="-")
    p_json.set_defaults(func=cmd_json)

    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
