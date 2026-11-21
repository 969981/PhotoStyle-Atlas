#!/usr/bin/env python3
"""Vendor upstream Agent Skills as real repository files (no submodules or symlinks)."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCES_FILE = ROOT / "config" / "sources.yaml"
LOCK_FILE = ROOT / "config" / "upstream-lock.json"
CATALOG_FILE = ROOT / "catalog" / "skills.json"
STYLES_FILE = ROOT / "catalog" / "styles.json"
OVERRIDES_FILE = ROOT / "catalog" / "overrides.yaml"
REPO_RE = re.compile(r"^[\w.-]+/[\w.-]+$")
REF_RE = re.compile(r"^[\w./-]+$")


def run(*args: str, cwd: Path | None = None) -> str:
    proc = subprocess.run(
        list(args), cwd=cwd, capture_output=True, text=True,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_LFS_SKIP_SMUDGE": "1"},
    )
    if proc.returncode:
        raise RuntimeError(
            "Command failed: " + " ".join(args[:5]) + "\n"
            + (proc.stderr or proc.stdout)[-3500:]
        )
    return proc.stdout.strip()


def read_json(path: Path, default: dict) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")


def safe_path(relative: str) -> Path:
    path = PurePosixPath(relative)
    if (not relative or path.is_absolute() or ".." in path.parts
            or "\\" in relative or relative.startswith("/")):
        raise ValueError("Unsafe relative path: " + relative)
    return Path(*path.parts)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_snapshot(old: dict) -> None:
    """Refuse to overwrite managed files that someone edited locally."""
    for rel, wanted in old.get("files", {}).items():
        path = ROOT / safe_path(rel)
        if path.is_symlink() or not path.is_file() or sha256(path) != wanted:
            raise RuntimeError(
                "Local drift in mirrored file: " + rel
                + ". Put custom changes in catalog/overrides.yaml or docs/."
            )


def file_pairs(src: Path, dest: Path):
    if src.is_symlink():
        raise RuntimeError("Upstream symlink refused: " + str(src))
    if src.is_file():
        yield src, dest
        return
    if not src.is_dir():
        raise RuntimeError("Missing upstream resource: " + str(src))
    for path in sorted(src.rglob("*")):
        if path.is_symlink():
            raise RuntimeError("Upstream symlink refused: " + str(path))
        if path.is_file():
            yield path, dest / path.relative_to(src)


def remote_sha(repo: str, ref: str) -> str:
    url = "https://github.com/" + repo + ".git"
    output = run("git", "ls-remote", url, "refs/heads/" + ref, "refs/tags/" + ref)
    candidates = [line.split()[0] for line in output.splitlines() if line.strip()]
    if not candidates:
        raise RuntimeError("Remote ref not found: " + repo + "@" + ref)
    return candidates[0]


def checkout(spec: dict, temp: Path) -> tuple[Path, str]:
    repo, ref = spec["repo"], spec["ref"]
    if not REPO_RE.fullmatch(repo) or not REF_RE.fullmatch(ref):
        raise ValueError("Unsafe GitHub repo or ref in manifest")
    target = temp / spec["id"]
    url = "https://github.com/" + repo + ".git"
    run("git", "clone", "--quiet", "--depth", "1", "--filter=blob:none",
        "--sparse", "--branch", ref, url, str(target))
    sparse = list(spec.get("sparse", []))
    if sparse:
        run("git", "-C", str(target), "sparse-checkout", "set", "--cone", *sparse)
    else:
        run("git", "-C", str(target), "sparse-checkout", "disable")
    sha = run("git", "-C", str(target), "rev-parse", "HEAD")
    return target, sha


def collect(spec: dict, checkout_root: Path):
    """Return ordered (source-file, destination-relative-path) pairs and skill records."""
    kind = spec["kind"]
    pairs: list[tuple[Path, str]] = []
    skills: list[dict] = []

    def add(src_rel: str, target: str, skill: bool):
        src = checkout_root / safe_path(src_rel)
        dest = ROOT / "skills" / safe_path(target) if skill else ROOT / safe_path(target)
        if skill:
            if not (src / "SKILL.md").is_file():
                raise RuntimeError("Missing SKILL.md: " + src_rel)
            skills.append({
                "id": target, "source_id": spec["id"], "upstream_path": src_rel,
                "source_repo": spec["repo"], "category": spec["category"],
                "license": spec["license"],
            })
        for origin, target_file in file_pairs(src, dest):
            relative = target_file.relative_to(ROOT).as_posix()
            pairs.append((origin, relative))

    if kind == "collection":
        base = checkout_root / safe_path(spec["base"])
        for child in sorted(base.iterdir()):
            if child.is_dir() and (child / "SKILL.md").is_file():
                add((PurePosixPath(spec["base"]) / child.name).as_posix(), child.name, True)
        if not skills:
            raise RuntimeError("No valid SKILL.md under " + str(base))
    elif kind == "items":
        for item in spec["items"]:
            add(item["path"], item["target"], True)
    elif kind == "root":
        target = spec["target"]
        if not (checkout_root / "SKILL.md").exists():
            raise RuntimeError("Missing root SKILL.md for " + spec["id"])
        skills.append({
            "id": target, "source_id": spec["id"], "upstream_path": ".",
            "source_repo": spec["repo"], "category": spec["category"],
            "license": spec["license"],
        })
        for name in spec["include"]:
            src = checkout_root / safe_path(name)
            dest = ROOT / "skills" / safe_path(target) / safe_path(name)
            for origin, target_file in file_pairs(src, dest):
                pairs.append((origin, target_file.relative_to(ROOT).as_posix()))
    elif kind == "file":
        # Some upstreams expose an ordinary agent Skill under another filename.
        # Mirror its bytes into the standard, installable SKILL.md path.
        origin = checkout_root / safe_path(spec["path"])
        if not origin.is_file() or origin.name.startswith("."):
            raise RuntimeError("Missing source Skill: " + str(origin))
        target = spec["target"]
        skills.append({
            "id": target, "source_id": spec["id"], "upstream_path": spec["path"],
            "source_repo": spec["repo"], "category": spec["category"],
            "license": spec["license"],
        })
        pairs.append((origin, (Path("skills") / target / "SKILL.md").as_posix()))
    elif kind == "resources":
        add(spec["base"], spec["target"], False)
    else:
        raise ValueError("Unknown source kind: " + str(kind))

    # Extra related documentation/code belongs inside the installable Skill.
    # This is also used for upstreams that place their references outside skills/.
    for extra in spec.get("extras", []):
        origin = checkout_root / safe_path(extra["path"])
        dest = ROOT / "skills" / safe_path(spec["target"]) / safe_path(extra["target"])
        for source_file, target_file in file_pairs(origin, dest):
            pairs.append((source_file, target_file.relative_to(ROOT).as_posix()))

    license_path = checkout_root / "LICENSE"
    if not license_path.is_file():
        raise RuntimeError("Missing upstream LICENSE: " + spec["repo"])
    pairs.append((license_path, "LICENSES/" + spec["id"] + "/LICENSE"))

    if spec.get("preview_from"):
        previews = checkout_root / safe_path(spec["preview_from"])
        for origin, target_file in file_pairs(
                previews, ROOT / "previews" / spec["id"]):
            pairs.append((origin, target_file.relative_to(ROOT).as_posix()))

    for preview in spec.get("preview_items", []):
        origin = checkout_root / safe_path(preview["path"])
        dest = ROOT / "previews" / safe_path(spec["id"]) / safe_path(preview["target"])
        for source_file, target_file in file_pairs(origin, dest):
            pairs.append((source_file, target_file.relative_to(ROOT).as_posix()))

    paths = [p for _, p in pairs]
    if len(paths) != len(set(paths)):
        raise RuntimeError("Duplicate destination within source " + spec["id"])
    return pairs, skills


def apply(spec: dict, pairs: list[tuple[Path, str]], old: dict) -> dict:
    old_files = old.get("files", {})
    check_snapshot(old)
    new_files = {}
    for src, rel in pairs:
        if src.stat().st_size > 95 * 1024 * 1024:
            raise RuntimeError("Oversized single file (>95MiB): " + str(src))
        dest = ROOT / safe_path(rel)
        # For relocated Markdown documents only, rebase hyperlinks. The
        # upstream original remains traceable through source commit + path;
        # snapshots record the exact locally stored bytes after rebasing.
        transformed = None
        if src.suffix.lower() == ".md" and spec.get("link_rewrites"):
            content = src.read_text(encoding="utf-8")
            for before, after in spec["link_rewrites"].items():
                content = content.replace(before, after)
            transformed = content.encode("utf-8")
        digest = hashlib.sha256(transformed).hexdigest() if transformed is not None else sha256(src)
        new_files[rel] = digest
        if dest.exists() and rel not in old_files:
            raise RuntimeError("Refusing to overwrite non-managed file: " + rel)
        if dest.exists() and sha256(dest) == digest:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if transformed is not None:
            dest.write_bytes(transformed)
        else:
            shutil.copy2(src, dest)
    for rel in old_files:
        if rel not in new_files:
            (ROOT / safe_path(rel)).unlink(missing_ok=True)
    return new_files


def frontmatter(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8-sig")
    if not raw.startswith("---\n"):
        return {}
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", raw, re.S)
    if not match:
        return {}
    parsed = yaml.safe_load(match.group(1))
    return parsed if isinstance(parsed, dict) else {}


def build_catalog(sources: list[dict], lock: dict) -> None:
    overrides = yaml.safe_load(OVERRIDES_FILE.read_text(encoding="utf-8"))
    overrides = (overrides or {}).get("skills", {})
    entries: list[dict] = []
    presets: list[dict] = []
    for spec in sources:
        snapshot = lock["sources"].get(spec["id"], {})
        for original in snapshot.get("skills", []):
            item = dict(original)
            slug = item["id"]
            root = ROOT / "skills" / slug
            fm = frontmatter(root / "SKILL.md")
            special = {}
            manifest = root / "manifest.json"
            if manifest.exists():
                try:
                    special = json.loads(manifest.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, UnicodeError):
                    pass
            override = overrides.get(slug, {})
            heading = re.search(
                r"(?m)^#\s+(.+)$",
                (root / "SKILL.md").read_text(encoding="utf-8-sig"),
            )
            item.update({
                "title": override.get("zh_name") or special.get("name")
                    or (heading.group(1).strip() if heading else slug),
                "description": fm.get("description", ""),
                "tags": override.get("tags", []),
                "use_cases": override.get("use_cases", []),
                "version": special.get("version", ""),
                "upstream_commit": snapshot.get("commit", ""),
                "path": "skills/" + slug,
                "preview": "",
            })
            if spec["id"] == "wibi-style":
                preview = ROOT / "previews" / "wibi-style" / (slug + ".jpg")
                if preview.is_file():
                    item["preview"] = preview.relative_to(ROOT).as_posix()
            elif spec.get("preview_items"):
                # One representative upstream preview per Skill, not an AI-generated claim.
                preview = ROOT / "previews" / spec["id"] / spec["preview_items"][0]["target"]
                if preview.is_file():
                    item["preview"] = preview.relative_to(ROOT).as_posix()
            entries.append(item)

            # The 80 presets reside INSIDE image-style-transfer, not 80 installable Skills.
            if slug == "image-style-transfer":
                library = root / "references" / "style-library.md"
                if not library.exists():
                    raise RuntimeError("Missing style library")
                data = library.read_text(encoding="utf-8")
                for hit in re.finditer(r"(?m)^###\s+(\d{1,3})\.\s+(.+?)\s*$", data):
                    presets.append({
                        "skill_id": slug, "number": int(hit.group(1)),
                        "title": hit.group(2), "type": "substyle",
                    })
            if slug == "anime-image-restyle":
                registry = root / "references" / "style-registry.md"
                if not registry.exists():
                    raise RuntimeError("Anime style registry missing")
                data = registry.read_text(encoding="utf-8")
                for hit in re.finditer(r"(?m)^-\s+`([a-z0-9-]+)`｜([^｜\n]+)", data):
                    presets.append({"skill_id": slug, "key": hit.group(1),
                                    "title": hit.group(2).strip(), "type": "style-key"})
            if slug == "poster-generator":
                style_dir = root / "references" / "styles"
                for style in sorted(style_dir.glob("*.md")):
                    match = re.search(r"(?m)^#\s+(.+)$", style.read_text(encoding="utf-8"))
                    presets.append({"skill_id": slug, "key": style.stem,
                                    "title": match.group(1).strip() if match else style.stem,
                                    "type": "poster-style"})
            if slug == "photo-editing-craft":
                for recipe in sorted((root / "recipes").glob("*.json")):
                    presets.append({"skill_id": slug, "key": recipe.stem,
                                    "title": recipe.stem.replace("-", " ").title(),
                                    "type": "edit-recipe"})
    entries.sort(key=lambda x: (x["source_id"], x["id"]))
    presets.sort(key=lambda x: (x["skill_id"], x.get("number", 0), x.get("key", "")))
    ids = [e["id"] for e in entries]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Duplicate skill id found across sources")
    write_json(CATALOG_FILE, {"schema_version": 1, "skills": entries})
    write_json(STYLES_FILE, {"schema_version": 1, "presets": presets})


def sync() -> None:
    manifest = yaml.safe_load(SOURCES_FILE.read_text(encoding="utf-8"))
    sources = manifest["sources"]
    if len({s["id"] for s in sources}) != len(sources):
        raise RuntimeError("Duplicate source id")
    old_lock = read_json(LOCK_FILE, {"version": 1, "sources": {}})
    new_lock = {"version": 1, "sources": {}}
    owned = set()
    with tempfile.TemporaryDirectory(prefix="photostyle-sync-") as td:
        temp = Path(td)
        for spec in sources:
            sid = spec["id"]
            old = old_lock.get("sources", {}).get(sid, {})
            check_snapshot(old)
            latest = remote_sha(spec["repo"], spec["ref"])
            if latest == old.get("commit") and old.get("files") and old.get("skills") is not None:
                snapshot = old
                print("UNCHANGED", sid, latest[:12])
            else:
                checkout_root, full_sha = checkout(spec, temp)
                pairs, skills = collect(spec, checkout_root)
                snapshot = {
                    "repo": spec["repo"], "ref": spec["ref"],
                    "commit": full_sha, "skills": skills,
                    "files": apply(spec, pairs, old),
                    "license": spec["license"],
                }
                print("IMPORTED", sid, full_sha[:12], len(skills), "skills", len(pairs), "files")
            for path in snapshot["files"]:
                if path in owned:
                    raise RuntimeError("Two upstream sources own the same path: " + path)
                owned.add(path)
            new_lock["sources"][sid] = snapshot
    write_json(LOCK_FILE, new_lock)
    build_catalog(sources, new_lock)
    print("READY", len(read_json(CATALOG_FILE, {})["skills"]), "installable skills")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Sync all configured sources (default)")
    parser.parse_args()
    sync()
