#!/usr/bin/env python3
"""只读发布预检：版本一致性、Tag/Release 冲突和发布说明草稿。

默认不写文件、不执行 Git 写操作。只有 --notes-file 会写出发布说明。
需要网络检查时显式加 --check-remote。
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_VERSION_RE = re.compile(r"^\s{2}version:\s*[\"']?([0-9]+\.[0-9]+\.[0-9]+)[\"']?\s*$", re.MULTILINE)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        fail(f"git {' '.join(args)} failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip()


def read(path: str) -> str:
    file_path = ROOT / path
    if not file_path.is_file():
        fail(f"missing file: {path}")
    return file_path.read_text(encoding="utf-8")


def extract_changelog_section(changelog: str, version: str) -> str:
    lines = changelog.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith(f"## [{version}]"):
            start = index
            break
    if start is None:
        fail(f"CHANGELOG.md has no section for {version}")
    section = []
    for line in lines[start + 1:]:
        if line.startswith("## ["):
            break
        section.append(line)
    body = "\n".join(section).strip()
    if not body:
        fail(f"CHANGELOG.md section for {version} is empty")
    return body + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="版本号，例如 0.5.0")
    parser.add_argument("--tag", help="Tag 名，默认 v<version>")
    parser.add_argument("--title", help="Release 标题，默认 v<version>")
    parser.add_argument("--skill", help="Skill 目录，默认按 v0.<minor> 推断")
    parser.add_argument("--notes-file", help="可选：把发布说明写入该文件")
    parser.add_argument("--skip-git-status", action="store_true", help="跳过工作区干净检查（仅用于本地试跑）")
    parser.add_argument("--check-remote", action="store_true", help="额外检查 GitHub 上是否已有 Tag/Release")
    args = parser.parse_args()

    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", args.version):
        fail(f"invalid version: {args.version}")
    tag = args.tag or f"v{args.version}"
    title = args.title or f"v{args.version}"
    major, minor, _patch = args.version.split(".")
    skill_dir = Path(args.skill) if args.skill else ROOT / "Skills" / f"python-study-assistant-v{major}-{minor}"
    if not skill_dir.is_dir():
        fail(f"missing skill directory: {skill_dir}")

    readme = read("README.md")
    changelog = read("CHANGELOG.md")
    checklist = read("RELEASE_CHECKLIST.md")

    skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    version_match = SKILL_VERSION_RE.search(skill_md)
    if not version_match:
        fail(f"cannot find metadata.version in {skill_dir / 'SKILL.md'}")
    skill_version = version_match.group(1)
    if skill_version != args.version:
        fail(f"SKILL metadata.version is {skill_version}, expected {args.version}")

    openai = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
    if f"v{major}.{minor}" not in openai:
        fail(f"agents/openai.yaml display_name does not mention v{major}.{minor}")

    if f"v{args.version}" not in readme:
        fail(f"README.md does not contain v{args.version}")
    if f"## [{args.version}]" not in changelog:
        fail(f"CHANGELOG.md does not contain ## [{args.version}]")
    if args.version not in checklist:
        fail(f"RELEASE_CHECKLIST.md does not contain {args.version}")

    if not args.skip_git_status:
        status = run_git("status", "--porcelain")
        if status:
            fail("working tree is not clean; commit or stash changes first")

    existing_tags = run_git("tag", "--list", tag)
    if existing_tags:
        fail(f"local tag already exists: {existing_tags}")

    remote_checked = False
    if args.check_remote:
        remote_checked = True
        repo_result = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if repo_result.returncode != 0:
            fail(f"cannot resolve GitHub repository: {repo_result.stderr.strip()}")
        repo = repo_result.stdout.strip()
        tag_result = subprocess.run(
            ["gh", "api", f"repos/{repo}/git/ref/tags/{tag}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if tag_result.returncode == 0:
            fail(f"remote tag already exists: {tag}")
        release_result = subprocess.run(
            ["gh", "release", "view", tag, "--json", "tagName"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if release_result.returncode == 0:
            fail(f"remote release already exists: {tag}")

    notes = extract_changelog_section(changelog, args.version)
    print(f"version: {args.version}")
    print(f"skill: {skill_dir.relative_to(ROOT).as_posix()}")
    print(f"tag: {tag}")
    print(f"title: {title}")
    print(f"notes: {len(notes)} characters from CHANGELOG.md")
    print(f"remote tag/release: {'checked (absent)' if remote_checked else 'not checked'}")
    print("planned actions:")
    print(f"  git tag -a {tag} -m {title!r}")
    print(f"  git push origin {tag}")
    print(f"  gh release create {tag} --title {title!r} --notes-file <notes>")
    print("guardrails: no visibility change, no force push, no history rewrite")

    if args.notes_file:
        Path(args.notes_file).write_text(notes, encoding="utf-8")
        print(f"notes written: {args.notes_file}")

    print("PASS: release preflight")


if __name__ == "__main__":
    main()
