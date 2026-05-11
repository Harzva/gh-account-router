#!/usr/bin/env python3
"""Run gh commands with the token for a named managed GitHub account."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_ACCESS_FILE = Path(
    os.environ.get(
        "GH_ACCOUNT_ROUTER_ACCESS_FILE",
        Path.home() / ".config" / "gh-account-router" / "accounts.txt",
    )
)
TOKEN_RE = re.compile(r"^(?:gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+)$")
TOKEN_IN_TEXT_RE = re.compile(r"(gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+)")


@dataclass
class AccountBlock:
    token: str
    aliases: list[str]


def normalize(value: str) -> str:
    return value.strip().lower()


def looks_like_token(line: str) -> bool:
    return bool(TOKEN_RE.match(line.strip()))


def parse_access_file(path: Path) -> list[AccountBlock]:
    if not path.exists():
        raise FileNotFoundError(f"Access file not found: {path}")

    blocks: list[AccountBlock] = []
    current_token: str | None = None
    current_aliases: list[str] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if looks_like_token(line):
            if current_token:
                blocks.append(AccountBlock(current_token, current_aliases))
            current_token = line
            current_aliases = []
            continue
        if current_token:
            current_aliases.append(line)

    if current_token:
        blocks.append(AccountBlock(current_token, current_aliases))

    return blocks


def find_account(blocks: list[AccountBlock], account: str) -> AccountBlock:
    wanted = normalize(account)
    for block in blocks:
        aliases = {normalize(alias) for alias in block.aliases}
        if wanted in aliases:
            return block
    known = sorted({alias for block in blocks for alias in block.aliases})
    raise ValueError(f"Account '{account}' not found. Known aliases: {', '.join(known)}")


def redact(text: str) -> str:
    return TOKEN_IN_TEXT_RE.sub("[REDACTED_TOKEN]", text)


def list_accounts(blocks: list[AccountBlock]) -> int:
    for block in blocks:
        alias_text = ", ".join(block.aliases) if block.aliases else "(no aliases)"
        print(f"- {alias_text}")
    return 0


def run_gh(block: AccountBlock, gh_args: list[str]) -> int:
    if not gh_args:
        raise ValueError("Missing gh arguments after --")

    env = os.environ.copy()
    env["GH_TOKEN"] = block.token
    env.pop("GITHUB_TOKEN", None)

    proc = subprocess.run(
        ["gh", *gh_args],
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.stdout:
        sys.stdout.write(redact(proc.stdout))
    if proc.stderr:
        sys.stderr.write(redact(proc.stderr))
    return proc.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--access-file",
        default=str(DEFAULT_ACCESS_FILE),
        help="Path to the private account-token file. Can also be set with GH_ACCOUNT_ROUTER_ACCESS_FILE.",
    )
    parser.add_argument("--account", help="Account alias, such as harzva or saihao")
    parser.add_argument("--list", action="store_true", help="List known account aliases without tokens")
    parser.add_argument("gh_args", nargs=argparse.REMAINDER, help="Arguments passed to gh after --")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    blocks = parse_access_file(Path(args.access_file))

    if args.list:
        return list_accounts(blocks)

    if not args.account:
        parser.error("--account is required unless --list is used")

    gh_args = args.gh_args
    if gh_args and gh_args[0] == "--":
        gh_args = gh_args[1:]

    block = find_account(blocks, args.account)
    return run_gh(block, gh_args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
