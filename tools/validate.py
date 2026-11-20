#!/usr/bin/env python3
"""Validate mirrored Skill files, source licenses, image previews and style metadata."""
import json
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def main():
    sources=yaml.safe_load((ROOT/"config/sources.yaml").read_text(encoding="utf-8"))["sources"]
    lock=json.loads((ROOT/"config/upstream-lock.json").read_text(encoding="utf-8"))["sources"]
    catalog=json.loads((ROOT/"catalog/skills.json").read_text(encoding="utf-8"))["skills"]
    presets=json.loads((ROOT/"catalog/styles.json").read_text(encoding="utf-8"))["presets"]
    ids=[x["id"] for x in catalog]
    assert len(ids)==len(set(ids)), "duplicate skill id"
    assert len(catalog)>=80, "incomplete Skill import"
    assert sum(x["source_id"]=="wibi-style" for x in catalog)==51, "Wibi 51 Skills incomplete"
    assert sum(x["source_id"]=="photo-to-poster" for x in catalog)==14, "Photo-to-Poster 14 Skills incomplete"
    assert sum(x["skill_id"]=="image-style-transfer" for x in presets)==80, "80 image styles missing"
    assert sum(x["skill_id"]=="anime-image-restyle" for x in presets)==71, "71 anime styles missing"
    assert sum(x["skill_id"]=="poster-generator" for x in presets)==20, "20 poster styles missing"
    assert sum(x["skill_id"]=="photo-editing-craft" for x in presets)==14, "14 retouch recipes missing"
    assert len(sources)==len(lock), "source lock count differs"
    for x in catalog:
        parent=ROOT/x["path"]
        assert (parent/"SKILL.md").is_file(), "missing Skill: "+x["id"]
        assert x["upstream_commit"], "missing provenance for "+x["id"]
        if x["source_id"]=="wibi-style":
            assert (parent/"LICENSE").is_file(), "Wibi LICENSE missing: "+x["id"]
            assert (parent/"NOTICE").is_file(), "Wibi NOTICE missing: "+x["id"]
            assert x["preview"] and (ROOT/x["preview"]).is_file(), "Wibi preview missing: "+x["id"]
    for s in sources:
        assert (ROOT/"LICENSES"/s["id"]/"LICENSE").is_file(), "upstream LICENSE missing"
    for p in (ROOT/"skills").rglob("*"):
        assert not p.is_symlink(), "symlink not allowed: "+str(p)
    print("OK:",len(catalog),"Skills,",len(presets),"style presets,",len(sources),"sources")

if __name__=="__main__":
    main()
