#!/usr/bin/env python3
"""Comprueba enlaces relativos markdown en todo el repositorio.

Sale 1 si hay archivos destino inexistentes.
Anclas rotas y markdown huérfanos: aviso por defecto.
Usa --strict-anchors o --strict-orphans para fallar también esos casos.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INLINE_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
REF_DEF_RE = re.compile(r"^\[[^\]]+\]:\s+(\S+)", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
# GFM / github-slugger: letras, marcas, dígitos, conectores (_), guion, espacio
SLUG_KEEP_RE = re.compile(r"[^\w\s\-]", re.UNICODE)

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "testdata"}


def is_markdown_doc(path: Path) -> bool:
    name = path.name.lower()
    return path.suffix.lower() == ".md" or name.endswith(".md.template")


def iter_md(root: Path):
    extra = [root / "AGENTS.md.template"]
    for p in extra:
        if p.is_file():
            yield p
    for p in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        # mkdocs/ es tooling, no documentación: mkdocs.yml lo excluye (docs_dir es
        # la raíz del repo), así que el checker tampoco lo recorre.
        if p.relative_to(root).parts[0] == "mkdocs":
            continue
        yield p


def iter_link_sources(root: Path):
    """Devuelve (fuente, carpeta base de los href, destino de un href «#ancla»).

    Los sidecars de handbook/_meta escriben los href relativos al capítulo
    (handbook/), no a _meta/; su «#ancla» apunta al capítulo que describen.
    """
    for md in iter_md(root):
        yield md, md.parent, md
    handbook = root / "handbook"
    meta = handbook / "_meta"
    if meta.is_dir():
        for sidecar in sorted(meta.glob("*.yaml")):
            yield sidecar, handbook, handbook / f"{sidecar.stem}.md"
    index = handbook / "index.yaml"
    if index.is_file():
        yield index, handbook, None


def strip_fence_blocks(text: str) -> str:
    """Quita bloques ``` para no tratar su contenido como headings/enlaces de prose."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "".join(out)


def github_slug(heading: str) -> str:
    text = heading.strip()
    text = re.sub(r"^#+\s*", "", text)
    text = re.sub(r"\s+#+\s*$", "", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = text.lower()
    text = SLUG_KEEP_RE.sub("", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text


def heading_slugs(text: str) -> set[str]:
    slugs: list[str] = []
    counts: dict[str, int] = {}
    for line in strip_fence_blocks(text).splitlines():
        m = HEADING_RE.match(line)
        if not m:
            continue
        base = github_slug(m.group(2))
        n = counts.get(base, 0)
        counts[base] = n + 1
        slugs.append(base if n == 0 else f"{base}-{n}")
    return set(slugs)


def hrefs_in(text: str) -> list[str]:
    body = strip_fence_blocks(text)
    found = INLINE_RE.findall(body)
    found.extend(REF_DEF_RE.findall(body))
    return found


def is_external(href: str) -> bool:
    h = href.strip()
    if h.startswith(("<", "{")):
        return True
    return h.startswith(("http://", "https://", "mailto:", "tel:"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Comprueba enlaces markdown locales.")
    parser.add_argument(
        "--strict-anchors",
        action="store_true",
        help="Sale 1 si hay anclas internas que no coinciden con un heading.",
    )
    parser.add_argument(
        "--strict-orphans",
        action="store_true",
        help="Sale 1 si hay .md nunca enlazados desde otro .md (salvo README raíz).",
    )
    args = parser.parse_args()

    missing: list[str] = []
    bad_anchors: list[str] = []
    incoming: dict[Path, int] = {}
    slug_cache: dict[Path, set[str]] = {}
    md_files = list(iter_md(ROOT))

    for md in md_files:
        incoming.setdefault(md.resolve(), 0)

    for src, base, self_target in iter_link_sources(ROOT):
        text = src.read_text(encoding="utf-8")
        for href in hrefs_in(text):
            href = href.strip().strip("<>")
            if not href or is_external(href):
                continue
            path_part, _, frag = href.partition("#")
            frag = frag.strip()
            if not path_part:
                if self_target is None:
                    continue
                target = self_target.resolve()
            else:
                target = (base / path_part).resolve()
                try:
                    target.relative_to(ROOT.resolve())
                except ValueError:
                    continue
                if not is_markdown_doc(target):
                    if not target.exists():
                        missing.append(f"{src.relative_to(ROOT)} -> {href}")
                    continue
                if not target.exists():
                    missing.append(f"{src.relative_to(ROOT)} -> {href}")
                    continue
                incoming[target] = incoming.get(target, 0) + 1
            if not frag:
                continue
            if target not in slug_cache:
                if not target.exists():
                    continue
                slug_cache[target] = heading_slugs(target.read_text(encoding="utf-8"))
            if frag.lower() not in {s.lower() for s in slug_cache[target]}:
                bad_anchors.append(f"{src.relative_to(ROOT)} -> #{frag} en {target.relative_to(ROOT)}")

    root_readme = (ROOT / "README.md").resolve()
    root_res = ROOT.resolve()

    def skip_orphan(p: Path) -> bool:
        if p == root_readme:
            return True
        try:
            rel = p.relative_to(root_res).as_posix()
        except ValueError:
            return True
        return rel.startswith(".github/") or rel.startswith("scripts/testdata/")

    orphans = [
        p.relative_to(ROOT).as_posix()
        for p, n in sorted(incoming.items(), key=lambda kv: str(kv[0]))
        if n == 0 and not skip_orphan(p)
    ]

    failed = False
    if missing:
        failed = True
        print("Rutas rotas:")
        for m in missing:
            print(f"  - {m}")
    else:
        print(f"OK archivos ({len(md_files)} markdown)")

    if bad_anchors:
        print("Anclas no encontradas:")
        for a in bad_anchors:
            print(f"  - {a}")
        if args.strict_anchors:
            failed = True
    else:
        print("OK anclas internas")

    if orphans:
        print("Huérfanos (ningún otro .md enlaza):")
        for o in orphans:
            print(f"  - {o}")
        if args.strict_orphans:
            failed = True
    else:
        print("OK sin huérfanos")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
