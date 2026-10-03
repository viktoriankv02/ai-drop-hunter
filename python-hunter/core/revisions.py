"""Readable source changes, without treating omissions as cancelled requirements."""
import re
from difflib import SequenceMatcher


def compare_materials(previous, current, limit=12):
    def blocks(body):
        text = body.get("text", "")
        # Normalize presentation-only whitespace. Bound each comparison unit.
        return [part.strip() for line in text.splitlines()
                for part in re.findall(r".{1,400}(?:\\s+|$)|.{1,400}", " ".join(line.split()))
                if part.strip()]
    old, new = blocks(previous), blocks(current)
    added, removed = [], []
    matcher = SequenceMatcher(None, old, new, autojunk=False)
    for kind, a, b, c, d in matcher.get_opcodes():
        if kind in ("replace", "insert"):
            added.extend(new[c:d])
        if kind in ("replace", "delete"):
            removed.extend(old[a:b])
    previous_links = {x.get("url") for x in previous.get("links", []) if x.get("url")}
    current_links = {x.get("url") for x in current.get("links", []) if x.get("url")}
    return {"added": added[:limit], "removed": removed[:limit],
            "added_count": len(added), "removed_count": len(removed),
            "added_links": sorted(current_links - previous_links)[:limit],
            "removed_links": sorted(previous_links - current_links)[:limit],
            "truncated": len(added) > limit or len(removed) > limit or
                len(current_links - previous_links) > limit or len(previous_links - current_links) > limit,
            "source_incomplete": bool(previous.get("truncated") or current.get("truncated")),
            "meaning": "source_text_change_not_verified_requirement_change"}
