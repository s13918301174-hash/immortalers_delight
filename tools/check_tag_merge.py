#!/usr/bin/env python3
"""Merge item tags from NeoForge + mods like the game, report empty/failed tags."""
from __future__ import annotations

import collections
import json
import pathlib
import re
import zipfile

MODS = pathlib.Path(
    r"E:\MC\01-Clients\qiangutest\.minecraft\versions\1.21.1-NeoForge_21.1.222\mods"
)
NF_ROOT = pathlib.Path(r"E:\MC\01-Clients\qiangutest\.minecraft\libraries\net\neoforged\neoforge")


def main() -> None:
    sources: list[pathlib.Path] = list(NF_ROOT.rglob("*-universal.jar"))[:1]
    sources += sorted(MODS.glob("*.jar"))

    tag_values: dict[str, list] = collections.defaultdict(list)

    def add_from_zip(zpath: pathlib.Path) -> None:
        try:
            z = zipfile.ZipFile(zpath)
        except Exception:
            return
        with z:
            for name in z.namelist():
                m = re.match(r"^data/([^/]+)/tags/items?/(.+)\.json$", name)
                if not m:
                    continue
                ns, path = m.group(1), m.group(2).replace("\\", "/")
                tag_id = f"{ns}:{path}"
                try:
                    data = json.loads(z.read(name).decode("utf-8-sig"))
                except Exception:
                    continue
                if data.get("replace"):
                    tag_values[tag_id] = []
                for v in data.get("values", []):
                    tag_values[tag_id].append(v)

    for s in sources:
        if s.exists():
            add_from_zip(s)

    resolved: dict[str, set[str]] = {}
    resolving: set[str] = set()
    failed: dict[str, str] = {}

    def entry_id(e):
        if isinstance(e, str):
            return e, True
        if isinstance(e, dict):
            return e.get("id"), bool(e.get("required", True))
        return None, True

    def resolve(tag_id: str) -> set[str]:
        if tag_id in resolved:
            return resolved[tag_id]
        if tag_id in resolving:
            return set()
        if tag_id not in tag_values:
            failed[tag_id] = "tag file absent"
            resolved[tag_id] = set()
            return set()
        resolving.add(tag_id)
        items: set[str] = set()
        problems: list[str] = []
        for e in tag_values[tag_id]:
            eid, req = entry_id(e)
            if not eid:
                continue
            if eid.startswith("#"):
                nested = eid[1:]
                nested_items = resolve(nested)
                if req and nested not in tag_values:
                    problems.append(f"required nested missing: {eid}")
                items |= nested_items
            else:
                items.add(eid)
        resolving.discard(tag_id)
        if problems:
            failed[tag_id] = "; ".join(problems)
            resolved[tag_id] = set()
            return set()
        resolved[tag_id] = items
        return items

    check = [
        "c:stones",
        "c:raw_meats",
        "c:foods/raw_meat",
        "c:foods/raw_mutton",
        "c:foods/raw_beef",
        "c:foods/raw_chicken",
        "c:foods/raw_pork",
        "c:salad_ingredients",
        "c:foods/vegetable",
        "forge:raw_meats",
        "forge:stone",
        "forge:raw_mutton",
    ]

    print(f"Loaded {len(tag_values)} item tags from {len(sources)} jars\n")
    print(f"{'tag':40} {'count':>6}  status")
    print("-" * 72)
    for t in check:
        items = resolve(t)
        if t in failed and failed[t] != "tag file absent":
            status = f"FAIL: {failed[t]}"
        elif t not in tag_values:
            status = "ABSENT"
        elif not items:
            status = "EMPTY"
        else:
            status = "OK"
        print(f"{t:40} {len(items):6}  {status}")
        if items:
            sample = ", ".join(sorted(items)[:8])
            more = " ..." if len(items) > 8 else ""
            print(f"   -> {sample}{more}")

    for t in sorted(tag_values):
        if t.startswith(("c:", "forge:", "immortalers_delight:")):
            resolve(t)

    fails = {
        k: v
        for k, v in failed.items()
        if k.startswith(("c:", "forge:", "immortalers_delight:")) and v != "tag file absent"
    }
    print(f"\nFailed tags (required missing nested): {len(fails)}")
    for k, v in sorted(fails.items())[:50]:
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
